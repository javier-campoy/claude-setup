# Changelog

Todos los cambios notables del proyecto se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

> Este fichero lo mantiene Claude automáticamente tras cambios en `src/`. No lo edites a mano salvo para corregir errores.

## [No publicado]

### Añadido
- `.gitignore` con entradas estándar de Python (`.venv/`, `__pycache__/`, cachés de `ruff`/`mypy`/`pytest`, `.coverage`, `dist/`, `build/`, `*.egg-info/`) y de Claude Code (`.claude/.cache/`, `.claude/settings.local.json`).

### Cambiado
- Unificado el nombre del fichero de historial a `changelog.md` (minúsculas) en `docs/index.md`, `CLAUDE.md`, `GUIA_CLAUDE_CODE.md`, `.pre-commit-config.yaml`, `.claude/commands/changelog.md` y plantillas/specs de `docs/specs/`.
- `install.sh` e `install.ps1`: eliminada la lista `EXCLUDE` (y su bloque de borrado) ahora que los ficheros obsoletos ya no existen en el kit fuente.

### Deprecado
- _Pendiente de cambios._

### Eliminado
- Restos del enfoque anterior basado en MkDocs: `mkdocs.yml`, `scripts/gen_ref_pages.py` (y el directorio `scripts/`), `docs/getting-started.md`, `docs/installation.md`, `docs/contributing.md`, `docs/guides/` (con `index.md` y `quickstart.md`), y los slash commands `.claude/commands/docs-build.md`, `docs-serve.md`, `docs-update.md`.
- Nota de aviso sobre ficheros MkDocs obsoletos en `GUIA_CLAUDE_CODE.md`, ya innecesaria.

### Arreglado
- _Pendiente de cambios._

### Seguridad
- _Pendiente de cambios._

---

## [0.1.0] - YYYY-MM-DD

### Añadido
- Primera versión del paquete.
