"""Tests del modo nightshift (dotclaude/nightshift): helper, guard y SessionStart.

Ejecutan los scripts como procesos sobre un repo git temporal. `NIGHTSHIFT_KIT` apunta
a otra copia del kit (p. ej. la instalada en ~/.claude/nightshift) si se quiere probar esa.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

KIT = Path(
    os.environ.get(
        "NIGHTSHIFT_KIT", Path(__file__).resolve().parents[2] / "dotclaude" / "nightshift"
    )
)
CLI = KIT / "bin" / "nightshift"
GUARD = KIT / "hooks" / "guard.py"
SESSION_START = KIT / "hooks" / "session_start.py"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-q", "--allow-empty", "-m", "init"],
        check=True,
        env={
            **os.environ,
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
        },
    )
    return root


@pytest.fixture
def env(tmp_path: Path) -> dict[str, str]:
    e = {
        k: v
        for k, v in os.environ.items()
        if k != "NIGHTSHIFT_SESSION" and not k.startswith("NIGHTSHIFT_NIGHT")
    }
    e["NIGHTSHIFT_HOME"] = str(tmp_path / "home-ns")
    e["NIGHTSHIFT_NO_CRON"] = "1"
    return e


def cli(args: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args], cwd=cwd, env=env, capture_output=True, text=True
    )


def guard(payload: dict, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        env=env,
        capture_output=True,
        text=True,
    )


def bash(cmd: str, cwd: Path, background: bool = False) -> dict:
    tin: dict = {"command": cmd}
    if background:
        tin["run_in_background"] = True
    return {"tool_name": "Bash", "tool_input": tin, "cwd": str(cwd)}


def write(path: Path, cwd: Path) -> dict:
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": str(path), "content": "x"},
        "cwd": str(cwd),
    }


def fake_lock(repo: Path) -> subprocess.Popen[bytes]:
    """Proceso vivo cuyo cmdline contiene 'nightshift', como el del lanzador."""
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)", "nightshift"])
    sd = repo / ".claude" / "nightshift"
    sd.mkdir(parents=True, exist_ok=True)
    (sd / "running.json").write_text(
        json.dumps({"pid": proc.pid, "night": "2026-11-05", "started": "x"})
    )
    return proc


# ------------------------------------------------------------------------- guard


def test_guard_modo_inactivo_deja_pasar_docker(repo: Path, env: dict[str, str]) -> None:
    assert guard(bash("docker.exe compose up -d", repo), env).returncode == 0


@pytest.mark.parametrize(
    "cmd",
    [
        "docker.exe build --target worker -t x .",
        "WITH_CONVERSION=true docker.exe compose --profile app up -d --wait",
        "docker compose build worker",
        "uv run pytest tests/e2e -m 'integration and slow'",
        "cd /x && docker.exe compose --profile app up -d",
        "git pull && docker.exe build .",
    ],
)
def test_guard_modo_activo_bloquea_pesados(repo: Path, env: dict[str, str], cmd: str) -> None:
    cli(["on"], repo, env)
    (repo / ".claude" / "nightshift.json").write_text(
        json.dumps({"heavy_patterns": [r"\btests/e2e\b"]})
    )
    r = guard(bash(cmd, repo), env)
    assert r.returncode == 2
    assert "nightshift new" in r.stderr


@pytest.mark.parametrize(
    "cmd",
    [
        "uv run pytest",
        "docker.exe ps",
        "docker.exe compose logs worker",
        "git status",
        "git commit -m 'docs: e2e con docker compose up y pytest -m slow'",
        "git add x && git commit -q -F - <<'EOF'\nchore: docker.exe build y pytest -m slow\nEOF\ngit log -1",
        "grep -n 'docker compose up' README.md",
    ],
)
def test_guard_modo_activo_deja_pasar_ligeros(repo: Path, env: dict[str, str], cmd: str) -> None:
    cli(["on"], repo, env)
    assert guard(bash(cmd, repo), env).returncode == 0


@pytest.mark.parametrize(
    "cmd,background,cutoff,expected",
    [
        ("NIGHTSHIFT_ETA_MIN=1 docker.exe compose up -d", True, "23:59", 0),
        ("nightshift bg e2e -- 'NIGHTSHIFT_ETA_MIN=1 docker.exe build .'", False, "23:59", 0),
        ("docker.exe compose up -d", True, "23:59", 2),  # sin duración declarada
        ("NIGHTSHIFT_ETA_MIN=1 docker.exe compose up -d", False, "23:59", 2),  # primer plano
        ("NIGHTSHIFT_ETA_MIN=30 docker.exe compose up -d", True, "00:00", 2),  # pasa del corte
    ],
)
def test_guard_pesado_de_dia_en_segundo_plano(
    repo: Path, env: dict[str, str], cmd: str, background: bool, cutoff: str, expected: int
) -> None:
    cli(["on"], repo, env)
    (repo / ".claude" / "nightshift.json").write_text(json.dumps({"day_cutoff": cutoff}))
    r = guard(bash(cmd, repo, background), env)
    assert r.returncode == expected, r.stderr
    if expected:
        assert "segundo plano" in r.stderr and "nightshift new" in r.stderr


def test_guard_bypass_explicito_deja_pasar(repo: Path, env: dict[str, str]) -> None:
    cli(["on"], repo, env)
    assert guard(bash("NIGHTSHIFT_BYPASS=1 docker.exe compose up -d", repo), env).returncode == 0


def test_guard_sesion_nocturna_nunca_se_bloquea(repo: Path, env: dict[str, str]) -> None:
    cli(["on"], repo, env)
    proc = fake_lock(repo)
    try:
        night = {**env, "NIGHTSHIFT_SESSION": "1"}
        assert guard(bash("docker.exe compose up -d", repo), night).returncode == 0
        assert guard(write(repo / "a.py", repo), night).returncode == 0
    finally:
        proc.kill()
        proc.wait()


@pytest.mark.parametrize(
    "cmd,expected",
    [
        ("git status -sb", 0),
        ("git -C /x log --oneline -5", 0),
        ("git branch -a", 0),
        ("git branch -D feat/x", 2),
        ("git worktree list", 0),
        ("git worktree remove x", 2),
        ("git commit -m x", 2),
        ("cat README.md", 0),
        ("cat a > b", 2),
        ("ls; rm -rf x", 2),
        ("find . -name '*.pyc' -delete", 2),
        ("nightshift status", 0),
        ("uv run pytest", 2),
    ],
)
def test_guard_cerrojo_solo_lectura_en_bash(
    repo: Path, env: dict[str, str], cmd: str, expected: int
) -> None:
    proc = fake_lock(repo)
    try:
        assert guard(bash(cmd, repo), env).returncode == expected
    finally:
        proc.kill()
        proc.wait()


def test_guard_cerrojo_bloquea_escritura_pero_no_la_cola(repo: Path, env: dict[str, str]) -> None:
    proc = fake_lock(repo)
    try:
        assert guard(write(repo / "src" / "a.py", repo), env).returncode == 2
        assert (
            guard(write(repo / ".claude" / "nightshift" / "queue" / "t.md", repo), env).returncode
            == 0
        )
    finally:
        proc.kill()
        proc.wait()


def test_guard_cerrojo_alcanza_a_los_worktrees(
    repo: Path, env: dict[str, str], tmp_path: Path
) -> None:
    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add", "-q", str(wt)], check=True)
    proc = fake_lock(repo)
    try:
        assert guard(write(wt / "a.py", wt), env).returncode == 2
    finally:
        proc.kill()
        proc.wait()


def test_guard_cerrojo_huerfano_no_bloquea(repo: Path, env: dict[str, str]) -> None:
    sd = repo / ".claude" / "nightshift"
    sd.mkdir(parents=True)
    (sd / "running.json").write_text(json.dumps({"pid": 999999, "night": "x"}))
    assert guard(write(repo / "a.py", repo), env).returncode == 0


def test_guard_fuera_de_git_no_hace_nada(tmp_path: Path, env: dict[str, str]) -> None:
    assert guard(bash("docker build .", tmp_path), env).returncode == 0


# ----------------------------------------------------------------------- helper


def test_cli_on_new_status_off(repo: Path, env: dict[str, str]) -> None:
    assert cli(["on"], repo, env).returncode == 0
    assert (repo / ".claude" / "nightshift" / "enabled").exists()
    assert str(repo) in (Path(env["NIGHTSHIFT_HOME"]) / "projects.txt").read_text()
    r = cli(["new", "e2e sustituto", "--title", "e2e del sustituto"], repo, env)
    task = Path(r.stdout.strip())
    assert task.parent == repo / ".claude" / "nightshift" / "queue"
    assert task.read_text().startswith("# e2e del sustituto")
    st = cli(["status"], repo, env).stdout
    assert "ACTIVO" in st and "e2e del sustituto" in st
    cli(["off"], repo, env)
    assert not (repo / ".claude" / "nightshift" / "enabled").exists()
    assert task.exists()  # off conserva la cola


def test_cli_new_desde_worktree_va_a_la_copia_principal(
    repo: Path, env: dict[str, str], tmp_path: Path
) -> None:
    wt = tmp_path / "wt2"
    subprocess.run(["git", "-C", str(repo), "worktree", "add", "-q", str(wt)], check=True)
    task = Path(cli(["new", "x"], wt, env).stdout.strip())
    assert task.parent == repo / ".claude" / "nightshift" / "queue"


def test_cli_launch_cola_vacia_no_lanza(repo: Path, env: dict[str, str]) -> None:
    cli(["on"], repo, env)
    r = cli(["launch"], repo, env)
    assert r.returncode == 0 and "cola vacía" in r.stdout
    assert not (repo / ".claude" / "nightshift" / "nights").exists()


def _fake_claude(bin_dir: Path, body: str) -> None:
    bin_dir.mkdir(exist_ok=True)
    f = bin_dir / "claude"
    f.write_text("#!/usr/bin/env bash\n" + body)
    f.chmod(0o755)


def test_cli_launch_congela_cola_y_quita_cerrojo(
    repo: Path, env: dict[str, str], tmp_path: Path
) -> None:
    cli(["on"], repo, env)
    cli(["new", "tarea"], repo, env)
    _fake_claude(
        tmp_path / "bin",
        'cat > /dev/null\necho \'{"type":"system","session_id":"abc"}\'\n'
        '[ "$NIGHTSHIFT_SESSION" = 1 ] || exit 9\n'
        'echo "# Informe" > "$NIGHTSHIFT_NIGHT_DIR/informe.md"; touch "$NIGHTSHIFT_NIGHT_DIR/DONE"\n',
    )
    env = {**env, "PATH": f"{tmp_path / 'bin'}:{env['PATH']}"}
    r = cli(["launch", "--deadline", "23:59"], repo, env)
    assert r.returncode == 0, r.stdout + r.stderr
    sd = repo / ".claude" / "nightshift"
    night = next((sd / "nights").iterdir())
    assert (night / "DONE").exists()
    assert len(list((night / "queue").glob("*.md"))) == 1
    assert not list((sd / "queue").glob("*.md"))
    assert not (sd / "running.json").exists()


def test_cli_launch_reanuda_si_no_hay_done(repo: Path, env: dict[str, str], tmp_path: Path) -> None:
    cli(["on"], repo, env)
    cli(["new", "tarea"], repo, env)
    (repo / ".claude" / "nightshift.json").write_text(
        json.dumps({"retry_wait_minutes": 0, "max_attempts": 3})
    )
    _fake_claude(
        tmp_path / "bin",
        'cat > /dev/null\necho \'{"type":"system","session_id":"abc"}\'\n'
        'echo "$@" >> "$NIGHTSHIFT_NIGHT_DIR/calls"\n'
        'if [[ "$*" == *--resume* ]]; then touch "$NIGHTSHIFT_NIGHT_DIR/DONE"; fi\n',
    )
    env = {**env, "PATH": f"{tmp_path / 'bin'}:{env['PATH']}"}
    cli(["launch", "--deadline", "23:59"], repo, env)
    night = next((repo / ".claude" / "nightshift" / "nights").iterdir())
    calls = (night / "calls").read_text().splitlines()
    assert len(calls) == 2 and "--resume abc" in calls[1]


def test_cli_launch_sin_done_anota_cierre_del_lanzador(
    repo: Path, env: dict[str, str], tmp_path: Path
) -> None:
    cli(["on"], repo, env)
    cli(["new", "tarea"], repo, env)
    (repo / ".claude" / "nightshift.json").write_text(
        json.dumps({"retry_wait_minutes": 0, "max_attempts": 2})
    )
    _fake_claude(tmp_path / "bin", "cat > /dev/null\nexit 1\n")
    env = {**env, "PATH": f"{tmp_path / 'bin'}:{env['PATH']}"}
    cli(["launch", "--deadline", "23:59"], repo, env)
    night = next((repo / ".claude" / "nightshift" / "nights").iterdir())
    assert "sin crear DONE" in (night / "informe.md").read_text()


def test_cli_launch_no_lanza_si_hay_noche_viva(repo: Path, env: dict[str, str]) -> None:
    cli(["new", "tarea"], repo, env)
    proc = fake_lock(repo)
    try:
        assert cli(["launch"], repo, env).returncode == 1
    finally:
        proc.kill()
        proc.wait()


def test_cli_unlock(repo: Path, env: dict[str, str]) -> None:
    proc = fake_lock(repo)
    try:
        assert cli(["unlock"], repo, env).returncode == 1  # viva: no sin --force
    finally:
        proc.kill()
        proc.wait()
    assert cli(["unlock"], repo, env).returncode == 0
    assert not (repo / ".claude" / "nightshift" / "running.json").exists()


def test_cli_bg_y_wait(repo: Path, env: dict[str, str], tmp_path: Path) -> None:
    env = {**env, "NIGHTSHIFT_NIGHT_DIR": str(tmp_path / "night")}
    assert cli(["bg", "ok", "--", "echo hola; exit 0"], repo, env).returncode == 0
    r = cli(["wait", "ok", "--max", "20"], repo, env)
    assert r.returncode == 0 and "hola" in r.stdout
    cli(["bg", "mal", "--", "exit 4"], repo, env)
    assert cli(["wait", "mal", "--max", "20"], repo, env).returncode == 1
    cli(["bg", "largo", "--", "sleep 30"], repo, env)
    t = time.monotonic()
    assert cli(["wait", "largo", "--max", "1"], repo, env).returncode == 3
    assert time.monotonic() - t < 15


# ------------------------------------------------------------------ SessionStart


def session_start(repo: Path, env: dict[str, str]) -> str:
    r = subprocess.run(
        [sys.executable, str(SESSION_START)],
        input=json.dumps({"cwd": str(repo)}),
        env=env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    return (
        json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"] if r.stdout.strip() else ""
    )


def test_session_start_recuerda_el_modo(repo: Path, env: dict[str, str]) -> None:
    assert session_start(repo, env) == ""
    cli(["on"], repo, env)
    assert "NIGHTSHIFT ACTIVO" in session_start(repo, env)


def test_session_start_informe_nuevo_una_sola_vez(repo: Path, env: dict[str, str]) -> None:
    night = repo / ".claude" / "nightshift" / "nights" / "2026-11-05"
    night.mkdir(parents=True)
    (night / "informe.md").write_text("# x")
    assert "informe de la noche 2026-11-05" in session_start(repo, env)
    assert "informe" not in session_start(repo, env)


def test_session_start_avisa_de_noche_en_curso(repo: Path, env: dict[str, str]) -> None:
    proc = fake_lock(repo)
    try:
        assert "sesión nocturna trabajando" in session_start(repo, env)
    finally:
        proc.kill()
        proc.wait()
