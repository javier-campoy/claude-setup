#!/usr/bin/env python3
"""SessionStart de nightshift: da contexto a las sesiones de día.

- Con el modo activo, recuerda la regla de aplazar lo pesado y cuántas tareas hay.
- Con una noche en curso, avisa de que el repo está cerrado a escritura.
- Si hay un informe nocturno que nadie ha visto, pide a Claude que se lo enseñe al
  usuario (una sola vez: luego queda marcado en `last-seen`).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def project_root(start: Path) -> Path | None:
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


def main() -> None:
    if os.environ.get("NIGHTSHIFT_SESSION") == "1":
        return
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    root = project_root(Path(data.get("cwd") or os.getcwd()))
    if root is None:
        return
    sd = root / ".claude" / "nightshift"
    if not sd.is_dir():
        return
    parts: list[str] = []

    lock = sd / "running.json"
    if lock.exists():
        try:
            info = json.loads(lock.read_text())
            alive = b"nightshift" in Path(f"/proc/{int(info['pid'])}/cmdline").read_bytes()
        except (OSError, ValueError, KeyError):
            alive = False
        if alive:
            parts.append(
                f"NIGHTSHIFT: hay una sesión nocturna trabajando en este repo (noche {info.get('night')}, "
                f"desde {info.get('started')}). No escribas en el repo ni en sus worktrees: el hook lo "
                "bloquea. Díselo al usuario al empezar."
            )
        else:
            parts.append(
                "NIGHTSHIFT: hay un cerrojo nocturno huérfano; `nightshift status` y `nightshift unlock`."
            )

    if (sd / "enabled").exists():
        queue = sorted((sd / "queue").glob("*.md")) if (sd / "queue").is_dir() else []
        try:
            cutoff = json.loads((root / ".claude" / "nightshift.json").read_text()).get("day_cutoff", "22:45")
        except (OSError, ValueError):
            cutoff = "22:45"
        parts.append(
            "NIGHTSHIFT ACTIVO en este repo. Todo proceso que tarde más de 20 min y no necesite "
            "interacción humana (builds y ejecuciones del compose, e2e, tests lentos, conversiones "
            "o evaluaciones largas) NO se ejecuta de día en primer plano. Antes de encolarlo, mira "
            "si puede ir en segundo plano ya: estima su duración con margen, comprueba que no choca "
            "con otro proceso pesado ni con su recurso exclusivo (`docker.exe ps`, jobs en marcha, "
            f"`free -g`) y, si acaba antes de las {cutoff}, lánzalo con `run_in_background: true` y "
            "`NIGHTSHIFT_ETA_MIN=<min>` delante, y sigue trabajando en paralelo. Si no cabe o choca, "
            "encólalo con `nightshift new <slug> --title \"...\"` y rellena la tarea entera. El hook "
            "bloquea los casos conocidos; los demás dependen de tu estimación. Las rondas de "
            "implementación y los subagentes del ciclo normal (architect, implementer, reviewer...) "
            "NO cuentan como pesados. Antes de encolar, mira la cola: si otra tarea ya ejecuta lo mismo (mismo build, e2e o commit), amplíala en vez de crear otra; si el resultado ya se conoce y repetirlo no aporta, no lo encoles. Encolar no es esperar: deja el trabajo coherente sin el "
            f"resultado y sigue. Cola actual: {len(queue)} tareas."
        )

    night_dirs = (
        sorted(p for p in (sd / "nights").iterdir() if p.is_dir())
        if (sd / "nights").is_dir()
        else []
    )
    if night_dirs and not lock.exists():
        last = night_dirs[-1]
        report = last / "informe.md"
        seen_file = sd / "last-seen"
        seen = seen_file.read_text().strip() if seen_file.exists() else ""
        if report.exists() and seen != last.name:
            parts.append(
                f"NIGHTSHIFT: hay un informe de la noche {last.name} sin ver: {report}. Léelo y "
                "resume al usuario, en tu primera respuesta, qué se hizo, qué falló y qué decisiones "
                "le tocan."
            )
            seen_file.write_text(last.name + "\n")

    if parts:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": "\n\n".join(parts),
                    }
                }
            )
        )


if __name__ == "__main__":
    main()
