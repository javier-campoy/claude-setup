#!/usr/bin/env python3
"""Gate de consistencia: docs/specs/*.md ↔ docs/STATE.md §5.

Verifica que el frontmatter `status` de cada spec esté reflejado
en la tabla correcta de docs/STATE.md §5:

  Draft / Approved → §5.1 "Activas (Draft / Approved, no implementadas)"
  Implemented      → §5.2 "Implementadas"
  Rejected         → §5.3 "Rechazadas / archivadas"

Sale con código 0 si todo es consistente, 1 si hay discrepancias.

Uso (desde la raíz del repo):
    python .claude/hooks/check_spec_state_sync.py
    uv run python .claude/hooks/check_spec_state_sync.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SPECS_DIR = Path("docs/specs")
STATE_MD = Path("docs/STATE.md")

# La plantilla de muestra no es una spec real.
_EXCLUDED = {"_template.md"}

_STATUS_RE = re.compile(r"^status:\s*(\S+)", re.MULTILINE)
_TABLE_ID_RE = re.compile(r"^\|\s*(\d{4})\s*\|", re.MULTILINE)


def _spec_id(name: str) -> str | None:
    m = re.match(r"^(\d{4})", name)
    return m.group(1) if m else None


def _frontmatter_status(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        return None
    m = _STATUS_RE.search(fm_match.group(1))
    return m.group(1) if m else None


def _extract_section(state_text: str, keyword: str) -> str:
    """Devuelve el cuerpo de la subsección ### que *empieza* con `keyword` hasta la siguiente ### o ##.

    Usa starts-with sin IGNORECASE para evitar que "Implementadas" haga match en
    "### Activas (Draft / Approved, no implementadas)".
    """
    pattern = re.compile(
        r"###\s+" + re.escape(keyword) + r"[^\n]*\n(.*?)(?=\n###|\n##|\Z)",
        re.DOTALL,
    )
    m = pattern.search(state_text)
    return m.group(1) if m else ""


def _ids_in_section(section_text: str) -> set[str]:
    return set(_TABLE_ID_RE.findall(section_text))


def _check_spec(spec_file: Path, active_ids: set[str], impl_ids: set[str]) -> list[str]:
    """Valida una spec individual; devuelve lista de errores (vacía si OK)."""
    spec_id = _spec_id(spec_file.name)
    status = _frontmatter_status(spec_file)
    if spec_id is None or status is None:
        return []

    if status in ("Draft", "Approved"):
        if spec_id not in active_ids:
            hint = " (aparece en §5.2 Implementadas)" if spec_id in impl_ids else ""
            return [
                f"  ❌ {spec_file.name}: status={status} pero no está en STATE §5.1 'Activas'{hint}"
            ]
    elif status == "Implemented":
        if spec_id not in impl_ids:
            hint = " (aparece en §5.1 Activas — falta moverla)" if spec_id in active_ids else ""
            return [
                f"  ❌ {spec_file.name}: status=Implemented pero no está en STATE §5.2 'Implementadas'{hint}"
            ]
    elif status == "Rejected":
        if spec_id in active_ids:
            return [f"  ⚠️  {spec_file.name}: status=Rejected pero sigue en STATE §5.1 'Activas'"]
        if spec_id in impl_ids:
            return [
                f"  ⚠️  {spec_file.name}: status=Rejected pero aparece en STATE §5.2 'Implementadas'"
            ]
    return []


def main() -> int:
    """Punto de entrada del gate de consistencia specs ↔ STATE.md §5."""
    if not STATE_MD.exists():
        print("⚠️  docs/STATE.md no encontrado — gate omitido.", file=sys.stderr)
        return 0
    if not SPECS_DIR.is_dir():
        print("⚠️  docs/specs/ no encontrado — gate omitido.", file=sys.stderr)
        return 0

    state_text = STATE_MD.read_text(encoding="utf-8")
    active_ids = _ids_in_section(_extract_section(state_text, "Activas"))
    impl_ids = _ids_in_section(_extract_section(state_text, "Implementadas"))

    errors: list[str] = []
    for spec_file in sorted(SPECS_DIR.glob("*.md")):
        if spec_file.name not in _EXCLUDED:
            errors.extend(_check_spec(spec_file, active_ids, impl_ids))

    if errors:
        print("❌ Inconsistencia entre docs/specs/ y docs/STATE.md §5:\n", file=sys.stderr)
        for err in errors:
            print(err, file=sys.stderr)
        print(
            "\nCorrige las tablas de STATE.md §5 (mueve las filas a la sección correcta) "
            "antes de commitear.",
            file=sys.stderr,
        )
        return 1

    n_checked = sum(
        1
        for f in SPECS_DIR.glob("*.md")
        if f.name not in _EXCLUDED and _spec_id(f.name) is not None
    )
    print(f"✅ docs/specs/ ↔ STATE.md §5 consistentes ({n_checked} specs verificadas).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
