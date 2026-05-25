#!/usr/bin/env python3
"""Gate determinista de cobertura de documentación.

Comprueba, sobre los módulos de `src/` indicados, que el código esté
*documentado* (no que el contenido sea correcto: eso lo juzga `docs-maintainer`).
Es la Capa 1 de la auditoría de docs: la invocan tanto la skill `/commit`
(que puede auto-remediar antes de commitear) como el hook `pre-commit`
(backstop para `git commit` manual sin Claude). Comparten este único script
para tener una sola definición de "qué es estar documentado".

Tres comprobaciones:

1. Docstrings: toda función/clase/método público (sin `_` prefijo o listado
   en `__all__`) debe tener docstring.
2. docs/modules/: todo módulo con API pública debe tener su
   `docs/modules/<modulo>.md` (mapeo espejo de CLAUDE.md).
3. changelog: si se tocan módulos de `src/`, la sección `[No publicado]` del
   changelog debe tener al menos una entrada.

Sale con código 0 si todo está cubierto, 1 si hay huecos. Hace no-op (0) si no
existe `src/` o si no hay `.py` relevantes que auditar (p. ej. un repo recién
desplegado por install.sh).

Uso:
    python .claude/hooks/check_doc_coverage.py            # audita todo src/
    python .claude/hooks/check_doc_coverage.py --staged   # solo lo staged
    python .claude/hooks/check_doc_coverage.py a.py b.py  # ficheros concretos
"""

from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from pathlib import Path

SRC_ROOT = Path("src")
MODULES_DOC_ROOT = Path("docs/modules")
CHANGELOG = Path("docs/changelog.md")

# Decoradores que eximen a una función de necesitar docstring propio.
# `overload` declara firmas (la implementación lleva el docstring); los setters
# y deleters de una property documentan en el getter.
_EXEMPT_DECORATORS = {"overload", "typing.overload", "setter", "deleter"}

# Un módulo vive en src/<paquete>/...: mínimo dos partes (paquete + fichero).
_MIN_MODULE_PARTS = 2

_FuncDef = ast.FunctionDef | ast.AsyncFunctionDef


class Gap:
    """Un hueco de documentación detectado, con su ubicación y mensaje."""

    def __init__(self, kind: str, location: str, message: str) -> None:
        self.kind = kind
        self.location = location
        self.message = message


def _decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Devuelve los nombres (dotted) de los decoradores de una función."""
    names: set[str] = set()
    for dec in node.decorator_list:
        target = dec.func if isinstance(dec, ast.Call) else dec
        if isinstance(target, ast.Name):
            names.add(target.id)
        elif isinstance(target, ast.Attribute):
            names.add(target.attr)
    return names


def _is_public(name: str, exported: set[str]) -> bool:
    """Un símbolo es público si no empieza por `_` o está en `__all__`."""
    return not name.startswith("_") or name in exported


def _exported_names(tree: ast.Module) -> set[str]:
    """Extrae los nombres declarados en `__all__` a nivel de módulo."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            continue
        if isinstance(node.value, ast.List | ast.Tuple):
            return {
                elt.value
                for elt in node.value.elts
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
            }
    return set()


def _has_public_api(tree: ast.Module, exported: set[str]) -> bool:
    """Indica si el módulo expone alguna función o clase pública."""
    return any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)
        and _is_public(node.name, exported)
        for node in tree.body
    )


def _func_missing_docstring(node: _FuncDef, exported: set[str]) -> bool:
    """True si la función/método público necesita docstring y no lo tiene."""
    if not _is_public(node.name, exported):
        return False
    if _decorator_names(node) & _EXEMPT_DECORATORS:
        return False
    return ast.get_docstring(node) is None


def _check_docstrings(path: Path, tree: ast.Module, exported: set[str]) -> list[Gap]:
    """Lista los símbolos públicos del módulo que no tienen docstring."""
    gaps: list[Gap] = []

    def report(node: ast.AST, descriptor: str, qualname: str) -> None:
        line = getattr(node, "lineno", 1)
        gaps.append(Gap("docstring", f"{path}:{line}", f"{descriptor} `{qualname}` sin docstring"))

    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            if _func_missing_docstring(node, exported):
                report(node, "función pública", node.name)
        elif isinstance(node, ast.ClassDef) and _is_public(node.name, exported):
            if ast.get_docstring(node) is None:
                report(node, "clase pública", node.name)
            for sub in node.body:
                if isinstance(
                    sub, ast.FunctionDef | ast.AsyncFunctionDef
                ) and _func_missing_docstring(sub, exported):
                    report(sub, "método público", f"{node.name}.{sub.name}")
    return gaps


def module_doc_path(py_path: Path) -> Path | None:
    """Mapea `src/<pkg>/<...>.py` a su `docs/modules/<...>.md` (espejo CLAUDE.md).

    - `src/pkg/foo.py`          -> `docs/modules/foo.md`
    - `src/pkg/sub/bar.py`      -> `docs/modules/sub.bar.md`
    - `src/pkg/sub/__init__.py` -> `docs/modules/sub.md`

    Devuelve None para el `__init__.py` del paquete raíz, que no tiene doc propia.
    """
    try:
        rel = py_path.relative_to(SRC_ROOT)
    except ValueError:
        return None
    parts = list(rel.parts)
    if len(parts) < _MIN_MODULE_PARTS:  # algo directamente bajo src/, sin paquete: ignorar
        return None
    inner = parts[1:]  # se descarta el nombre del paquete de nivel superior
    if inner[-1] == "__init__.py":
        inner = inner[:-1]  # un subpaquete documenta en <sub>.md
    else:
        inner[-1] = inner[-1].removesuffix(".py")
    if not inner:  # era el __init__.py del paquete raíz
        return None
    return MODULES_DOC_ROOT / (".".join(inner) + ".md")


def _check_module_doc(py_path: Path, tree: ast.Module, exported: set[str]) -> list[Gap]:
    """Verifica que un módulo con API pública tenga su docs/modules/<mod>.md."""
    if not _has_public_api(tree, exported):
        return []  # sin API pública (p. ej. __init__ con solo __version__): no exige doc
    doc = module_doc_path(py_path)
    if doc is None or doc.exists():
        return []
    return [Gap("module_doc", str(py_path), f"falta {doc}")]


def _unreleased_has_entries() -> bool:
    """Indica si la sección `[No publicado]` del changelog tiene alguna entrada."""
    if not CHANGELOG.exists():
        return False
    in_section = False
    for raw in CHANGELOG.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            # Entra en la sección al ver su cabecera; sale al llegar a la siguiente.
            in_section = "no publicado" in line.lower() or "unreleased" in line.lower()
            continue
        if in_section and (line.startswith("- ") or line.startswith("* ")):
            return True
    return False


def _staged_src_files() -> list[Path]:
    """Ficheros `src/**/*.py` añadidos/modificados/renombrados en el índice."""
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    files = [Path(line) for line in out.splitlines() if line.strip()]
    return [f for f in files if f.suffix == ".py" and SRC_ROOT in f.parents and f.exists()]


def _all_src_files() -> list[Path]:
    """Todos los `src/**/*.py` del árbol de trabajo."""
    return sorted(p for p in SRC_ROOT.rglob("*.py") if p.is_file())


def _resolve_targets(args: argparse.Namespace) -> list[Path]:
    """Determina el conjunto de módulos a auditar según los argumentos."""
    if args.files:
        return [
            p
            for f in args.files
            if (p := Path(f)).suffix == ".py" and SRC_ROOT in p.parents and p.exists()
        ]
    if args.staged:
        return _staged_src_files()
    return _all_src_files()


def _report(gaps: list[Gap], n_modules: int) -> int:
    """Imprime el resultado y devuelve el código de salida (0 OK, 1 con huecos)."""
    if not gaps:
        print(f"✓ Cobertura de documentación OK ({n_modules} módulo(s) revisado(s)).")
        return 0

    by_kind: dict[str, list[Gap]] = {}
    for gap in gaps:
        by_kind.setdefault(gap.kind, []).append(gap)

    titles = {
        "docstring": "Docstrings faltantes",
        "module_doc": "docs/modules/ faltantes",
        "changelog": "Changelog",
    }
    print(f"\n❌ Cobertura de documentación incompleta ({len(gaps)} problema(s)).\n")
    for kind in ("docstring", "module_doc", "changelog"):
        items = by_kind.get(kind)
        if not items:
            continue
        print(f"{titles[kind]} ({len(items)}):")
        for gap in items:
            print(f"  {gap.location}  {gap.message}")
        print()
    print("Soluciónalo con:")
    print("  /docs <fichero>   docstrings + docs/modules/<modulo>.md")
    print("  /changelog        rellenar la sección [No publicado]")
    print()
    return 1


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada del gate de cobertura de documentación."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--staged", action="store_true", help="auditar solo los src/*.py en el índice"
    )
    parser.add_argument("files", nargs="*", help="ficheros concretos a auditar (opcional)")
    args = parser.parse_args(argv)

    if not SRC_ROOT.is_dir():
        return 0  # repo sin código fuente todavía: nada que auditar

    targets = _resolve_targets(args)
    if not targets:
        return 0  # nada relevante (p. ej. --staged sin src/ en stage)

    gaps: list[Gap] = []
    for path in targets:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, OSError) as exc:
            gaps.append(Gap("docstring", str(path), f"no se pudo analizar: {exc}"))
            continue
        exported = _exported_names(tree)
        gaps.extend(_check_docstrings(path, tree, exported))
        gaps.extend(_check_module_doc(path, tree, exported))

    if not _unreleased_has_entries():
        gaps.append(Gap("changelog", str(CHANGELOG), "la sección [No publicado] no tiene entradas"))

    return _report(gaps, len(targets))


if __name__ == "__main__":
    sys.exit(main())
