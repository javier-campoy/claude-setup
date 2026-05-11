# Changelog

Todos los cambios notables del proyecto se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

> Este fichero lo mantiene Claude automáticamente tras cambios en `src/`. No lo edites a mano salvo para corregir errores.

## [No publicado]

### Añadido
- `.github/workflows/ci.yml`: pipeline de CI con ruff check, ruff format, mypy y pytest+cobertura; se ejecuta en cada push/PR a main.
- `.github/workflows/release.yml`: workflow de release automático al hacer push de un tag `v*.*.*`; extrae el changelog, construye el paquete y crea el GitHub Release.
- `.github/dependabot.yml`: actualizaciones mensuales automáticas de versiones de GitHub Actions.
- `.claude/hooks/post-tool-use.sh`: hook PostToolUse que auto-formatea `.py` con ruff y marca los flags de doc-sync.
- `.claude/hooks/pre-stop.sh`: hook Stop que bloquea la sesión si hay cambios en `src/` sin actualizar docs.
- `.claude/commands/release.md`: comando `/release` para preparar y publicar versiones (bump, changelog, tag, push).
- Hooks activados en `.claude/settings.json` (PostToolUse + Stop) apuntando a los scripts en `.claude/hooks/`.
- `.github/` añadido a la lista `INCLUDE` de `install.sh` para distribuirlo en el deploy.

### Cambiado
- `README.md`: añadida badge de CI, sección de Releases y corrección del número de subagentes (4, no 2).
- `GUIA_CLAUDE_CODE.md`: sección de ficheros actualizada con `.claude/hooks/` y `.github/`; sección de hooks reescrita apuntando a los scripts shell; nueva sección "CI/CD y releases" (sección 8); comandos slash actualizados con `/release`.
- `CLAUDE.md`: sección de hooks actualizada; `/release` añadido a la lista de comandos.

### Eliminado
- `install.ps1` — el kit es solo para Linux/macOS.

### Arreglado
- Hooks de doc-sync que habían sido movidos a settings de usuario y dejado de funcionar; ahora viven en `.claude/hooks/` y se distribuyen con el kit.
- `install.ps1` instalaba solo el hook tipo `pre-commit`; ahora eliminado (solo Linux/macOS).

---

## [0.1.0] — Histórico previo

### Añadido
- `.gitignore` con entradas estándar de Python (`.venv/`, `__pycache__/`, cachés de `ruff`/`mypy`/`pytest`, `.coverage`, `dist/`, `build/`, `*.egg-info/`) y de Claude Code (`.claude/.cache/`, `.claude/settings.local.json`).

### Cambiado
- Unificado el nombre del fichero de historial a `changelog.md` (minúsculas).
- `install.sh`: setup agnóstico de usuario y proyecto con flags `--author-name`, `--author-email`, `--github-user`.

### Eliminado
- Restos del enfoque anterior basado en MkDocs: `mkdocs.yml`, `scripts/`, `docs/getting-started.md`, `docs/installation.md`, `docs/contributing.md`, `docs/guides/`, slash commands `docs-build.md`, `docs-serve.md`, `docs-update.md`.

### Seguridad
- `.claude/settings.local.json` destrackeado de git.

