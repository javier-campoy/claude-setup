# Guía: empezar con Claude Code para Python

Esta guía explica qué hace cada fichero del kit y cómo desplegarlo en tu proyecto.

---

## 1. Resumen de los ficheros

| Fichero | Para qué sirve |
|---|---|
| `CLAUDE.md` | Memoria principal. Claude lo lee al inicio de cada sesión. Contiene convenciones, comandos y reglas del proyecto. |
| `.claude/settings.json` | Permisos del agente (allow / ask / deny) y definición de hooks. |
| `.claude/hooks/post-tool-use.sh` | Hook PostToolUse: auto-format con ruff + marcado de flags para doc-sync. |
| `.claude/hooks/pre-stop.sh` | Hook Stop: bloquea la sesión si hay cambios en `src/` sin actualizar docs. |
| `.claude/commands/*.md` | Comandos slash personalizados: `/test`, `/lint`, `/commit`, `/review`, `/refactor`, `/audit`, `/docs`, `/vision`, `/spec`, `/state`, `/changelog`, `/implement-spec`, `/release`. |
| `.claude/agents/*.md` | Subagentes especializados: `code-reviewer`, `test-writer`, `docs-maintainer`, `refactorer`. |
| `.mcp.json` | Configuración de servidores MCP (GitHub, context7, filesystem) — todos desactivados por defecto. |
| `.github/workflows/ci.yml` | CI: lint + type-check + tests en cada push/PR a main. |
| `.github/workflows/release.yml` | Release automático al hacer push de un tag `v*.*.*`. |
| `.github/dependabot.yml` | Actualizaciones mensuales de las versiones de GitHub Actions. |
| `pyproject.toml` | Config completa de Python: deps, ruff, mypy estricto, pytest, coverage. |
| `.gitignore` | Ignora cachés, venvs, secrets, `.claude/.cache/` y ficheros locales de Claude. |
| `.python-version` | Pinnea Python 3.12. |
| `.pre-commit-config.yaml` | Hooks de pre-commit: ruff, mypy, gitleaks, conventional-commits, protect-main, docs-sync, quality-gate. |
| `docs/index.md` | Mapa de la documentación. |
| `docs/VISION.md` | El norte del proyecto: dirección a futuro (objetivos, no-objetivos, principios, temas estratégicos). Humano, evoluciona con `/vision`. Se construye antes de la primera spec. |
| `docs/STATE.md` | Estado actual del repo: arquitectura, stack, ADRs, specs. Lo mantiene Claude. |
| `docs/changelog.md` | Historial cronológico (Keep a Changelog). |
| `docs/specs/` | Specs spec-driven: `README.md`, `_template.md` y una `NNNN-slug.md` por cambio. |
| `README.md` | Quick start del proyecto. |
| `install.sh` | Despliega el kit a un proyecto nuevo (Linux/macOS). |

---

## 2. Instalación paso a paso

### Paso 1: instalar Claude Code

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# o vía npm
npm install -g @anthropic-ai/claude-code
```

Luego ejecuta `claude` desde tu proyecto e inicia sesión con tu cuenta.

### Paso 2: instalar uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Paso 3: desplegar el kit a tu proyecto

```bash
# Clona este repo en algún lugar local
git clone https://github.com/usuario/claude-setup ~/claude-setup

# Despliega a tu proyecto (crea la carpeta si no existe)
~/claude-setup/install.sh ~/proyectos/mi-app mi_app \
    --author-name "Tu Nombre" \
    --author-email "tu@email.com" \
    --github-user "tuusuario"
```

El script copia todos los ficheros, sustituye los tokens (`mi_paquete`, `Tu Nombre`, etc.), inicializa git, ejecuta `uv sync` e instala los hooks de pre-commit.

### Paso 3 (alternativo): copiar a mano

Si prefieres copiar ficheros tú mismo, la estructura final debe ser:

```
mi-proyecto/
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── .gitignore
├── .python-version
├── .pre-commit-config.yaml
├── .mcp.json
├── src/
│   └── mi_paquete/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── docs/
│   ├── index.md
│   ├── VISION.md
│   ├── STATE.md
│   ├── changelog.md
│   └── specs/
│       ├── README.md
│       ├── _template.md
│       └── 0001-ejemplo.md
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── release.yml
│   └── dependabot.yml
└── .claude/
    ├── settings.json
    ├── hooks/
    │   ├── post-tool-use.sh
    │   └── pre-stop.sh
    ├── commands/
    │   ├── test.md
    │   ├── lint.md
    │   ├── commit.md
    │   ├── review.md
    │   ├── refactor.md
    │   ├── audit.md
    │   ├── docs.md
    │   ├── vision.md
    │   ├── spec.md
    │   ├── state.md
    │   ├── changelog.md
    │   ├── implement-spec.md
    │   └── release.md
    └── agents/
        ├── code-reviewer.md
        ├── test-writer.md
        ├── docs-maintainer.md
        └── refactorer.md
```

### Paso 4: personalizar

Edita `pyproject.toml` y `CLAUDE.md`:

- En `pyproject.toml`: cambia `name`, `description`, `authors`, y la línea `packages = ["src/mi_paquete"]` para que apunte al nombre real de tu paquete.
- En `CLAUDE.md`: rellena la sección "Resumen del proyecto" y "Notas y decisiones de diseño" con info real.
- Renombra `src/mi_paquete/` al nombre que uses (snake_case del nombre del paquete).

### Paso 5: inicializar el proyecto

```bash
cd mi-proyecto
git init
uv sync --all-extras --dev          # Crea .venv e instala todo
uv run pre-commit install           # Activa los hooks de git
```

### Paso 6: lanzar Claude Code

```bash
claude
```

La primera vez te pedirá aprobar los permisos de `.claude/settings.json`.

---

## 3. Cómo usar lo que hay configurado

### Comandos slash

Dentro de la sesión de `claude`, escribe `/` y verás los comandos disponibles:

| Comando | Qué hace |
|---|---|
| `/test [args]` | Ejecuta pytest. Sin args, corre la suite con cobertura. Con args (`/test tests/test_foo.py::test_bar`), corre solo eso. |
| `/lint` | Ejecuta `ruff format`, `ruff check --fix` y `mypy`. Reporta lo que no se ha podido auto-arreglar. |
| `/review [rama-base]` | Hace una revisión de los cambios pendientes contra la rama base (default: `main`). |
| `/commit [tipo]` | Genera un commit message siguiendo Conventional Commits a partir del diff actual. Pasa por gate de calidad antes. |
| `/refactor <fichero>` | Refactoriza un fichero respetando convenciones. Verifica con tests al terminar. |
| `/audit [ámbito]` | Auditoría arquitectónica del codebase. Compara contra `STATE.md` y ADRs vía subagente `refactorer`. Propone refactors priorizados, no aplica nada sin confirmación. |
| `/docs <fichero>` | Añade o mejora docstrings (estilo Google) en un fichero concreto. |
| `/vision [descripción]` | Crea o evoluciona `docs/VISION.md`, el norte del proyecto. Úsalo una vez antes de la primera spec; luego cuando cambie la dirección. Registra cada cambio en el historial de revisiones. |
| `/spec <descripción>` | Crea una nueva spec en `docs/specs/NNNN-slug.md` con estado `Draft`. Exige que la visión esté rellenada; si no, te deriva a `/vision`. Tú la apruebas. |
| `/state` | Regenera `docs/STATE.md` con la estructura, stack, métricas y specs actuales. Preserva ADRs y contenido humano. |
| `/changelog [rango]` | Añade entradas al `docs/changelog.md` para los cambios recientes. |
| `/implement-spec <ruta>` | Implementa una spec aprobada paso a paso. Marca como Implemented y actualiza docs al terminar. |
| `/release <versión>` | Prepara y publica una nueva versión: bump, changelog, tag `vX.Y.Z` y push. GitHub Actions crea el Release. |

### Subagentes

Para invocar un subagente, dile a Claude algo como:

```
Use the code-reviewer subagent to review my changes since main.
```

```
Use the test-writer subagent to add tests for src/mi_paquete/parser.py
```

```
Use the docs-maintainer subagent to audit code/docs coherence.
```

```
Use the refactorer subagent to audit src/parser/ for drift against STATE.md.
```

Los subagentes corren en su propio contexto, así que no contaminan el contexto principal con todos los ficheros que leen. Útil para tareas grandes y aisladas.

### Hooks automáticos

La lógica de los hooks vive en `.claude/hooks/` (scripts shell) y se activa desde `.claude/settings.json`. Hay dos tipos:

**`PostToolUse` → `.claude/hooks/post-tool-use.sh`** (se dispara tras cada Edit/Write):

1. **Auto-format Python**: si Claude edita un `.py`, ejecuta `ruff format` + `ruff check --fix`. Cero esfuerzo de formato.
2. **Flag de cambios en `src/`**: si el fichero editado está bajo `src/`, crea `.claude/.cache/src-changed.flag`.
3. **Flag de docs tocadas**: si Claude edita `docs/STATE.md`, `docs/changelog.md` o `docs/specs/*.md`, crea `.claude/.cache/docs-touched.flag`.

**`Stop` → `.claude/hooks/pre-stop.sh`** (se dispara al terminar cada respuesta):

4. Si existe `src-changed.flag` pero **NO** `docs-touched.flag`, **el hook bloquea con `exit 2`** y obliga a Claude a continuar y actualizar docs antes de cerrar la sesión.

Para desactivar un hook temporalmente, edita `.claude/settings.json` y comenta el bloque correspondiente.

**Si quieres saltarte la auto-actualización en una sesión puntual**:
```bash
rm -f .claude/.cache/src-changed.flag
```

### Permisos

`.claude/settings.json` tiene tres listas:

- **allow**: Claude ejecuta sin preguntar (lectura, ruff, pytest, git status/diff/log/commit, etc.).
- **ask**: Claude pregunta antes (git push, git reset, instalar/eliminar deps, rm).
- **deny**: Claude no puede (curl, wget, leer `.env`, leer claves privadas).

Ajústalo a tu nivel de comodidad. Lo más habitual: añadir más cosas a `allow` cuando confíes más en el agente.

---

## 4. Documentación viva (spec-driven)

### Cómo está montado

La documentación NO es un sitio web. Son ficheros Markdown plano dentro de `docs/`, leídos directamente desde el editor o GitHub. Cuatro tipos de contenido:

```
docs/
├── index.md         # Mapa de la documentación
├── VISION.md        # El norte del proyecto (dirección a futuro, humano)
├── STATE.md         # Estado actual del repo (auto-actualizado por Claude)
├── changelog.md     # Historial cronológico (Keep a Changelog)
└── specs/
    ├── README.md            # Índice + cómo funciona el flujo
    ├── _template.md         # Plantilla para nuevas specs
    └── NNNN-slug.md         # Specs individuales con frontmatter
```

### VISION.md: el norte (vs STATE.md: el presente)

`docs/VISION.md` y `docs/STATE.md` son complementarios y conviene no confundirlos:

| | `VISION.md` | `STATE.md` |
|---|---|---|
| **Pregunta** | ¿A dónde vamos? | ¿Dónde estamos ahora? |
| **Naturaleza** | Prescriptivo, direccional | Descriptivo, foto del presente |
| **Propiedad** | Humana (Claude ayuda con `/vision`) | Claude (regenera con `/state` y hooks) |
| **Estabilidad** | Estable, cambia poco y a propósito | Volátil, cambia con cada cambio de `src/` |
| **Contenido** | Propósito, objetivos, no-objetivos, principios, temas estratégicos | Arquitectura, módulos, stack, ADRs, specs, métricas |

La visión **se construye antes de la primera spec** (`/vision "describe tu proyecto"`) y **evoluciona deliberadamente**: cuando cambia el rumbo, `/vision` ajusta las secciones afectadas y registra una entrada en su Historial de revisiones (nunca se borra histórico). Es el nexo que specs, sprints y decisiones técnicas toman de referencia. `/spec` la exige rellenada; cada spec declara qué objetivo del norte avanza (`vision_refs` + sección "Alineación con la visión"). `/state` **nunca** la toca.

### STATE.md: el estado vivo

`docs/STATE.md` tiene siete secciones:

1. **Visión general** — qué hace el proyecto (humano).
2. **Arquitectura y módulos** — estructura de `src/` y responsabilidades (auto).
3. **Stack y dependencias** — leídas de `pyproject.toml` (auto).
4. **Decisiones técnicas (ADRs inline)** — uno por decisión importante (humano + propuestas de Claude).
5. **Specs** — tres tablas: activas, implementadas, rechazadas (auto desde frontmatter).
6. **Estado del codebase** — métricas y salud (auto).
7. **Roadmap inmediato** — siguientes specs aprobadas (auto + notas humanas).

Lo regenera `/state` o el hook de auto-actualización cuando Claude termina una sesión que tocó `src/`.

### changelog.md: el histórico

Formato [Keep a Changelog](https://keepachangelog.com/es/1.1.0/). Sección `[No publicado]` con seis subsecciones:

- **Añadido** — funcionalidad nueva.
- **Cambiado** — comportamiento existente que cambia.
- **Deprecado** — APIs que desaparecerán.
- **Eliminado** — APIs quitadas.
- **Arreglado** — bugs.
- **Seguridad** — vulnerabilidades.

Cuando releases, mueves `[No publicado]` → `[X.Y.Z] - YYYY-MM-DD`.

### Specs: el flujo spec-driven

Cualquier cambio no trivial empieza con una spec. Una spec es un Markdown en `docs/specs/NNNN-slug.md` con frontmatter:

```yaml
---
id: NNNN
title: "Título corto"
status: Draft           # Draft | Approved | Implemented | Rejected
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "Quien la escribió"
implemented_in: ""      # commit hash cuando esté Implemented
related: []
---
```

Y diez secciones (resumen, motivación, propuesta, alternativas, plan de implementación, criterios de aceptación, compatibilidad, riesgos, notas, decisiones durante implementación). Ver [`docs/specs/_template.md`](#) y el ejemplo [`docs/specs/0001-ejemplo.md`](#).

**Ciclo de vida:**

```
┌─────────┐  /spec    ┌───────┐  revisión  ┌──────────┐  /implement-spec  ┌─────────────┐
│  idea   │ ───────▶  │ Draft │ ────────▶  │ Approved │ ──────────────▶   │ Implemented │
└─────────┘           └───────┘            └──────────┘                   └─────────────┘
```

### Comandos clave

```bash
# Definir o evolucionar el norte del proyecto (antes de la primera spec)
/vision "describe tu proyecto: problema, usuarios, objetivos, qué NO hará"

# Crear una spec nueva (exige que la visión esté rellenada)
/spec "quiero un parser de URLs con validación estricta"

# (revisas el draft, lo apruebas: cambias status a Approved en el frontmatter)

# Implementar una spec aprobada
/implement-spec docs/specs/0001-parser-de-urls.md

# Regenerar STATE.md tras cambios manuales o si está desactualizado
/state

# Añadir entradas al changelog para los cambios recientes
/changelog

# Auditoría profunda de coherencia código ↔ docs
Use the docs-maintainer subagent to audit code/docs coherence.
```

### Auto-actualización: cómo se mantiene viva

Cuatro mecanismos colaboran:

1. **Hook `PostToolUse`**: cuando Claude edita un `.py` bajo `src/`, marca `.claude/.cache/src-changed.flag`.
2. **Hook `PostToolUse`**: cuando Claude edita `docs/STATE.md`, `docs/changelog.md` o `docs/specs/*.md`, marca `.claude/.cache/docs-touched.flag`.
3. **Hook `Stop`**: si hay flag de src/ pero NO flag de docs/, **bloquea con `exit 2`** y obliga a Claude a continuar y actualizar docs antes de terminar.
4. **Pre-commit hook**: WARNING si commiteas cambios en `src/` sin tocar `docs/`. No bloquea.

El resultado: tras cualquier sesión que toque `src/`, las docs viva quedan sincronizadas. No tienes que acordarte.

### Reglas mentales para usarlo bien

- **Una spec por unidad de cambio coherente**. Tres cambios no relacionados → tres specs.
- **No implementes nada complejo sin spec aprobada**. La spec es el contrato.
- **STATE.md y changelog.md no se editan a mano** salvo correcciones. Los gestiona Claude.
- **NUNCA borres ADRs** ni specs implementadas. Son histórico.
- **Hotfixes triviales** (typos, format, errores obvios de 1-2 líneas) pueden saltarse el flujo spec.

---

## 5. Memoria de Claude: cómo funciona

Claude Code carga jerárquicamente:

1. `CLAUDE.md` global (`~/.claude/CLAUDE.md`) — tus preferencias personales.
2. `CLAUDE.md` del proyecto — el del repo, compartido con el equipo.
3. `CLAUDE.local.md` — local al proyecto pero NO commiteado (en `.gitignore`).

Dentro de cualquier `CLAUDE.md` puedes hacer `@otro_fichero.md` para incluir otro fichero. Útil para mantener la memoria modular.

**Trucos:**

- Cuando notes que Claude se olvida de algo recurrente, añádelo a `CLAUDE.md`.
- Usa `#` al principio de un mensaje para que Claude lo añada automáticamente a memoria. Ejemplo: escribe `# Siempre usa pathlib en lugar de os.path` y Claude te preguntará a qué fichero de memoria añadirlo.
- Mantén `CLAUDE.md` ≤ 200 líneas. Si crece más, divídelo y usa `@imports`.

---

## 6. Flujo de trabajo recomendado

### Antes de empezar: define el norte (una vez)

```
claude
/vision "describe tu proyecto: qué problema resuelve, para quién, cómo se ve el éxito"
# Claude crea/rellena docs/VISION.md. Revísalo, ajústalo, complétalo.
# Es el norte: a partir de aquí, toda spec se justifica contra él.
# Vuelve a /vision cuando cambie la dirección (queda registrado en el historial).
```

### Para una feature nueva (flujo spec-driven)

```
1. git checkout -b feat/nombre
2. claude
3. /spec "descripción de lo que quieres hacer"
   (si la visión no está rellenada, /spec te derivará a /vision primero)
4. (Claude crea docs/specs/NNNN-slug.md en estado Draft)
5. Revisas, editas, ajustas — cuando estás conforme, cambias status a Approved.
6. /implement-spec docs/specs/NNNN-slug.md
7. (Claude implementa siguiendo la spec, marca como Implemented,
   actualiza STATE.md + changelog.md, hace push a la rama y sugiere el PR)
8. Creas el PR — manualmente o con el comando gh que Claude sugiere.
9. CI pasa (ci.yml en verde) → mergeas el PR a main.
10. Si la feature completa una unidad de release:
    git checkout main && git pull
    /release 0.2.0
    (Claude actualiza pyproject.toml + changelog, crea el tag, hace push;
     GitHub Actions crea el Release automáticamente)
```

### Para arreglar un bug

```
1. claude
2. "Hay un bug: <descripción>. Reprodúcelo con un test que falle."
3. Use the test-writer subagent to reproduce this bug.
4. (Claude/subagente añade un test que falla.)
5. "Ahora arregla el bug manteniendo el test verde."
6. /test
7. /commit  (con tipo fix:)
```

### Para refactorizar

```
1. /refactor src/mi_paquete/foo.py "extraer la lógica de validación a su propio módulo"
2. (Revisa el diff.)
3. /test
4. /commit  (con tipo refactor:)
```

---

## 7. Personalizaciones útiles

### Añadir un comando slash propio

Crea `.claude/commands/<nombre>.md`:

```markdown
---
description: Lo que hace
allowed-tools: Bash(uv run:*), Read, Edit
argument-hint: "<args opcionales>"
---

Instrucciones para Claude. Puedes usar $ARGUMENTS para los argumentos.
```

Reinicia la sesión y aparecerá como `/<nombre>`.

### Añadir un subagente propio

Crea `.claude/agents/<nombre>.md`:

```markdown
---
name: <nombre>
description: Cuándo invocarlo (sé específico para que Claude lo use cuando toca).
tools: Read, Grep, Glob, Bash
model: sonnet
---

System prompt completo del subagente.
```

### Activar MCPs

Edita `.mcp.json`, quita el prefijo `_` de la clave del servidor que quieras (p.ej. `_github` → `github`), y exporta los tokens necesarios:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_...
```

Reinicia `claude`.

---

## 8. CI/CD y releases

### Cómo encaja en el flujo de trabajo

CI y releases no son pasos adicionales: son la salida natural del flujo spec-driven.

```
spec aprobada
    ↓
/implement-spec          ← Claude implementa, testea localmente y hace push a feature branch
    ↓
PR abierto               ← Claude sugiere el comando gh pr create
    ↓
ci.yml en verde          ← GitHub ejecuta ruff + mypy + pytest automáticamente
    ↓
merge a main             ← Tú decides cuándo, con CI verde
    ↓
/release X.Y.Z           ← Cuando la unidad de release está completa
    ↓
release.yml              ← GitHub crea el Release con el contenido de changelog.md
```

### CI (`ci.yml`)

Se ejecuta en cada push y en cada PR. Hace: ruff check → ruff format → mypy → pytest con cobertura. **Un PR no se mergea con CI rojo.**

La cobertura se sube opcionalmente a Codecov (configura el secret `CODECOV_TOKEN` en el repo de GitHub si quieres activarlo).

### Release (`release.yml`)

Se dispara al hacer push de un tag `v*.*.*`. Hace:
1. Gate de calidad completo (igual que CI).
2. Extrae la sección `[X.Y.Z]` de `docs/changelog.md`.
3. Construye el paquete (`uv build`).
4. Crea el GitHub Release con las notas del changelog y los artefactos en `dist/`.

Para publicar también en PyPI, configura un **Trusted Publisher** en pypi.org y descomenta el paso `uv publish` en el workflow.

### Release con `/release`

```bash
# Desde main, con los PRs ya mergeados:
/release 0.2.0
```

Claude hace: bump en `pyproject.toml` → rename `[No publicado]` → `[0.2.0]` en changelog → commit → tag anotado → push. El tag dispara `release.yml` automáticamente.

### Dependabot

`.github/dependabot.yml` abre PRs mensuales para actualizar versiones de GitHub Actions (`actions/checkout`, `astral-sh/setup-uv`, etc.). Mergeables con un clic cuando CI pase.

## 9. Errores comunes

- **"No se aplica el hook de format"** → Comprueba que `uv` está en el PATH y que el proyecto tiene `.venv` con ruff instalado (`uv sync --dev`).
- **"Claude no usa los comandos slash"** → Verifica que existen en `.claude/commands/` y reinicia la sesión.
- **"mypy se queja de cosas absurdas"** → `disallow_untyped_defs = false` para tests ya está puesto. Si aún molesta en algún módulo concreto, añade `[[tool.mypy.overrides]]` específico.
- **"ruff es demasiado estricto"** → Quita reglas del bloque `select` en `pyproject.toml`. Las más controvertidas son `S` (bandit) y `PL` (pylint).
- **"Claude no me deja terminar la sesión y me pide actualizar docs"** → Es el hook `Stop` haciendo su trabajo. Ejecuta `/state` y `/changelog` (o pídeselo en lenguaje natural). Si quieres saltártelo en una sesión puntual: `rm -f .claude/.cache/src-changed.flag`.
- **"He hecho un cambio trivial y aun así me pide actualizar docs"** → El hook detecta cualquier cambio en `src/*.py`. Si fue verdaderamente trivial, dile a Claude "el cambio es trivial, marca el flag como completado" y borrará el flag.
- **"Quiero implementar algo sin pasar por una spec"** → Adelante para hotfixes y cambios pequeños. Para cambios significativos, el spec-driven está pensado para que el alineamiento humano-IA sea explícito y trazable; si lo saltas, perderás esa trazabilidad.
- **"Mi spec se quedó a medio implementar"** → Vuelve a invocar `/implement-spec` con la misma ruta. Claude verá los checkboxes ya marcados y continuará donde se quedó.
- **"Quiero saltarme el pre-commit en un commit puntual"** → `git commit --no-verify` (úsalo con cabeza).

---

## 10. Próximos pasos

Cuando ya tengas soltura:

- Considera añadir CI con GitHub Actions ejecutando ruff + mypy + pytest en cada PR.
- Activa el MCP de GitHub para que Claude pueda leer y comentar en PRs.
- Configura Dependabot/Renovate para mantener deps al día.
- Si trabajas en equipo, comparte `CLAUDE.md` y revísalo en code reviews igual que el código.

¡Buen código!
