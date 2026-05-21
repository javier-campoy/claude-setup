# Changelog

Todos los cambios notables del proyecto se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

> Este fichero lo mantiene Claude automáticamente tras cambios en `src/`. No lo edites a mano salvo para corregir errores.

## [No publicado]

### Añadido
- `docs/VISION.md`: nuevo documento vivo con el **norte del proyecto** (propósito, visión a futuro, usuarios, objetivos, no-objetivos, principios rectores, métricas, temas estratégicos, restricciones, riesgos e historial de revisiones). Prescriptivo y de propiedad humana; se construye antes de la primera spec y evoluciona deliberadamente.
- `.claude/commands/vision.md`: comando `/vision` para crear (modo CREAR) y evolucionar (modo EVOLUCIONAR, con registro de revisión) la visión del proyecto.
- `docs/specs/_template.md`: subsección "Alineación con la visión" en Motivación y campo de frontmatter `vision_refs` para trazar qué objetivo del norte avanza cada spec.
- `docs/STATE.md`: sección 8 "CI/CD y versioning" con tabla de pipelines, estrategia semver e historial de releases.
- `docs/specs/_template.md`: criterio de aceptación estándar "CI verde" en la sección 6.
- `.github/workflows/ci.yml`: pipeline de CI con ruff check, ruff format, mypy y pytest+cobertura; se ejecuta en cada push/PR a main.
- `.github/workflows/release.yml`: workflow de release automático al hacer push de un tag `v*.*.*`; extrae el changelog, construye el paquete y crea el GitHub Release.
- `.github/dependabot.yml`: actualizaciones mensuales automáticas de versiones de GitHub Actions.
- `.claude/hooks/post-tool-use.sh`: hook PostToolUse que auto-formatea `.py` con ruff y marca los flags de doc-sync.
- `.claude/hooks/pre-stop.sh`: hook Stop que bloquea la sesión si hay cambios en `src/` sin actualizar docs.
- `.claude/commands/release.md`: comando `/release` para preparar y publicar versiones (bump, changelog, tag, push).
- Hooks activados en `.claude/settings.json` (PostToolUse + Stop) apuntando a los scripts en `.claude/hooks/`.
- `.github/` añadido a la lista `INCLUDE` de `install.sh` para distribuirlo en el deploy.

### Cambiado
- `.claude/commands/spec.md`: nuevo paso 0 que **bloquea `/spec` si la visión no está rellenada** (deriva a `/vision`), lee `VISION.md` como contexto y exige declarar la alineación de la spec con el norte.
- `.claude/commands/implement-spec.md`: el contexto ahora carga `docs/VISION.md`; la implementación debe respetar objetivos, no-objetivos y principios.
- `.claude/commands/state.md`: la sección 1 de STATE.md pasa a enlazar a `VISION.md` (sin duplicarla) y se añade la regla de **no tocar nunca `VISION.md`** desde `/state`.
- `.claude/agents/refactorer.md` y `.claude/agents/docs-maintainer.md`: incorporan `docs/VISION.md` como norte estratégico; el refactorer detecta drift contra el norte, el docs-maintainer audita (sin reescribir) la coherencia visión ↔ código/specs.
- `CLAUDE.md`, `GUIA_CLAUDE_CODE.md`, `docs/index.md`, `docs/specs/README.md`, `README.md`: documentado el flujo `/vision → /spec → /implement-spec`, la distinción VISION (futuro) vs STATE (presente) y la visión como nexo de specs y sprints.
- `install.sh`: `docs/VISION.md` añadido a la sustitución de tokens y `/vision` incluido en los pasos finales antes de `/spec`.
- `README.md`: añadida badge de CI, sección de Releases y corrección del número de subagentes (4, no 2).
- `GUIA_CLAUDE_CODE.md`: sección 6 (flujo de trabajo) actualizada con pasos de PR, CI y release integrados; sección 8 reescrita con diagrama del flujo completo.
- `CLAUDE.md`: nueva sección "CI/CD y releases"; sección "Git y commits" con PR workflow; regla 4 ampliada; `/release` en la lista de comandos.
- `.claude/commands/implement-spec.md`: paso 8 verifica rama de feature, push al branch y sugiere PR en lugar de push ciego; paso 9 propone PR con CI reminder; paso 10 orienta el próximo paso (release).
- `docs/specs/_template.md`: criterio CA4 "CI verde" añadido a la plantilla de criterios de aceptación.

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

