#!/usr/bin/env python3
"""PreToolUse de nightshift (Bash|Edit|Write|MultiEdit|NotebookEdit).

1. **Cerrojo**: mientras corre la sesión nocturna de un repo, bloquea a las demás
   sesiones (las de día que se quedaron abiertas, sus subagentes y sus `/loop`) toda
   escritura y todo Bash que no sea de solo lectura en ese repo y sus worktrees. Solo
   se libra lo que escribe en la cola (`.claude/nightshift/queue/`).
2. **Modo activo**: de día, un comando pesado (más de 20 min sin interacción) solo pasa
   si va en segundo plano, declara su duración (`NIGHTSHIFT_ETA_MIN=<min>`) y acaba
   antes del corte (`day_cutoff`, 22:45 por defecto, para no pisar la noche). Si no,
   se bloquea para que Claude lo relance así o lo encole. `NIGHTSHIFT_BYPASS=1` lo deja
   pasar cuando el usuario pide expresamente ejecutarlo ya.

La sesión nocturna lleva `NIGHTSHIFT_SESSION=1` en el entorno y no se bloquea nunca.
Sale con 2 (bloquea y devuelve el motivo a Claude por stderr) o con 0.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

DEFAULT_HEAVY = [
    r"\bdocker(\.exe)?\s+(buildx\s+)?build\b",
    r"\bdocker(\.exe)?\s+compose\b.*\s(up|build|run)\b",
    r"\bdocker-compose\b.*\s(up|build|run)\b",
]
READ_ONLY = {
    "ls",
    "cat",
    "head",
    "tail",
    "grep",
    "rg",
    "find",
    "wc",
    "pwd",
    "stat",
    "file",
    "tree",
    "less",
    "date",
    "echo",
    "which",
    "nightshift",
    "free",
    "df",
    "du",
    "ps",
}
READ_ONLY_GIT = {"status", "log", "diff", "show", "rev-parse", "ls-files", "blame"}
DEFAULT_DAY_CUTOFF = "22:45"
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def project_root(start: Path) -> Path | None:
    while not start.exists() and start != start.parent:
        start = start.parent
    if start.is_file():
        start = start.parent
    try:
        out = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--path-format=absolute", "--git-common-dir"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        ).stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return None
    common = Path(out)
    return common.parent if common.name == ".git" else common


def lock_alive(root: Path) -> dict | None:
    try:
        info = json.loads((root / ".claude" / "nightshift" / "running.json").read_text())
        pid = int(info.get("pid", 0))
        if pid > 0 and b"nightshift" in Path(f"/proc/{pid}/cmdline").read_bytes():
            return info
    except (OSError, ValueError):
        pass
    return None


def heavy_patterns(root: Path) -> list[str]:
    pats = list(DEFAULT_HEAVY)
    try:
        cfg = json.loads((root / ".claude" / "nightshift.json").read_text())
        pats += cfg.get("heavy_patterns", [])
    except (OSError, ValueError):
        pass
    return pats


def is_read_only(command: str) -> bool:
    if re.search(r"[;&|`>]|\$\(", command):
        return False
    try:
        words = shlex.split(command)
    except ValueError:
        return False
    if not words:
        return True
    head = Path(words[0]).name
    if head == "git":
        args = words[1:]
        while args[:1] == ["-C"] or args[:1] == ["--no-pager"]:
            args = args[2:] if args[0] == "-C" else args[1:]
        if not args:
            return False
        sub, rest = args[0], args[1:]
        if sub in READ_ONLY_GIT:
            return True
        if sub == "branch":
            return all(w in {"-a", "-r", "-v", "-vv", "--list", "--show-current", "--all"} for w in rest)
        return sub == "worktree" and rest[:1] == ["list"]
    if head in {"find"}:
        return not any(w in {"-delete", "-exec", "-execdir"} for w in words)
    return head in READ_ONLY


TEXT_ONLY = {"git", "echo", "printf", "cat", "grep", "rg", "sed", "awk", "glab", "gh", "curl", "jq", "less", "head", "tail"}


def executable_text(command: str) -> str:
    """Lo que de verdad se ejecuta: sin cuerpos de heredoc ni tramos que solo manejan
    texto (un `git commit -m "... pytest -m slow ..."` no es un pytest)."""
    no_heredoc = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n.*?\n\s*\1\b", " ", command, flags=re.S)
    keep = []
    for seg in re.split(r"&&|\|\||;|\||\n", no_heredoc):
        words = seg.strip().split()
        while words and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0]):
            words = words[1:]
        if words and Path(words[0]).name in TEXT_ONLY:
            continue
        keep.append(seg)
    return " ; ".join(keep)


def day_cutoff(root: Path) -> dt.datetime:
    """Hora hasta la que puede durar un proceso pesado de día (por defecto 22:45)."""
    value = DEFAULT_DAY_CUTOFF
    try:
        value = json.loads((root / ".claude" / "nightshift.json").read_text()).get("day_cutoff", value)
    except (OSError, ValueError):
        pass
    hh, mm = (int(x) for x in value.split(":"))
    return dt.datetime.now().replace(hour=hh, minute=mm, second=0, microsecond=0)


def day_background_verdict(command: str, tin: dict, cutoff: dt.datetime) -> str | None:
    """None si el pesado puede correr ya de día: en segundo plano, con duración
    declarada (`NIGHTSHIFT_ETA_MIN=<min>`) y terminando antes del corte. Si no, el motivo."""
    background = bool(tin.get("run_in_background")) or re.search(r"\bnightshift\s+bg\b", command)
    m = re.search(r"\bNIGHTSHIFT_ETA_MIN=(\d+)\b", command)
    if not background or not m:
        return "No va en segundo plano con su duración declarada."
    end = dt.datetime.now() + dt.timedelta(minutes=int(m.group(1)))
    if end > cutoff:
        return f"Con {m.group(1)} min acabaría a las {end:%H:%M}, después del corte de las {cutoff:%H:%M}."
    return None


def block(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    if os.environ.get("NIGHTSHIFT_SESSION") == "1":
        sys.exit(0)
    try:
        data = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    tool = data.get("tool_name", "")
    tin = data.get("tool_input") or {}
    cwd = Path(data.get("cwd") or os.getcwd())

    if tool in WRITE_TOOLS:
        target = tin.get("file_path") or tin.get("notebook_path") or ""
        where = Path(target) if target else cwd
        if not where.is_absolute():
            where = cwd / where
    elif tool == "Bash":
        where = cwd
    else:
        sys.exit(0)

    root = project_root(where)
    if root is None:
        sys.exit(0)
    sd = root / ".claude" / "nightshift"

    info = lock_alive(root)
    if info:
        if tool in WRITE_TOOLS:
            try:
                where.resolve().relative_to((sd / "queue").resolve())
                sys.exit(0)
            except ValueError:
                pass
            block(
                f"nightshift: la sesión nocturna está trabajando en {root} (noche {info.get('night')}, "
                f"desde {info.get('started')}). Esta sesión no puede escribir en el repo ni en sus "
                "worktrees hasta que termine. Solo puedes añadir tareas a la cola para otra noche. "
                "Avisa al usuario y para."
            )
        command = tin.get("command", "")
        if not is_read_only(command):
            block(
                f"nightshift: la sesión nocturna está trabajando en {root} (noche {info.get('night')}). "
                "Mientras dure solo se permiten comandos de solo lectura (git status/log/diff, ls, cat...) "
                "y `nightshift`. Avisa al usuario y para."
            )
        sys.exit(0)

    if tool == "Bash" and (sd / "enabled").exists():
        command = tin.get("command", "")
        if "NIGHTSHIFT_BYPASS=1" in command:
            sys.exit(0)
        runnable = executable_text(command)
        pat = next((p for p in heavy_patterns(root) if re.search(p, runnable)), None)
        if pat is None:
            sys.exit(0)
        cutoff = day_cutoff(root)
        verdict = day_background_verdict(command, tin, cutoff)
        if verdict is None:
            sys.exit(0)
        block(
            f"nightshift activo: este comando es pesado (patrón `{pat}`). {verdict}\n"
            "Antes de encolarlo, mira si puede ir de día en segundo plano: (1) estima su duración "
            "con margen; (2) comprueba que no choca con otro proceso pesado en marcha "
            "(`docker.exe ps`, jobs en segundo plano de esta u otras sesiones, `free -g`), ni con "
            "el recurso exclusivo que necesite; (3) si cabe, relánzalo con `run_in_background: true` "
            f"(o `nightshift bg <nombre> -- '<cmd>'`) anteponiendo `NIGHTSHIFT_ETA_MIN=<minutos>`, "
            f"y sigue trabajando en paralelo. Tiene que acabar antes de las {cutoff:%H:%M}, para no "
            "pisar la noche de las 23:00.\n"
            "Si no cabe o choca, encólalo: `nightshift new <slug> --title \"...\"` imprime la ruta "
            "de una tarea nueva; rellénala entera (directorio y commit, comandos exactos, criterio "
            "de éxito, qué hacer si falla y qué hacer después), deja tu trabajo coherente sin el "
            "resultado y sigue. Solo si el usuario pide expresamente ejecutarlo ya en primer "
            "plano, antepón `NIGHTSHIFT_BYPASS=1`."
        )
    sys.exit(0)


if __name__ == "__main__":
    main()
