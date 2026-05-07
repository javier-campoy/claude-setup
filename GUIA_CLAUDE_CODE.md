# Guía: empezar con Claude Code para Python

Esta guía explica qué hace cada fichero del kit y cómo desplegarlo en tu proyecto.

---

## 1. Resumen de los ficheros

| Fichero | Para qué sirve |
|---|---|
| `CLAUDE.md` | Memoria principal. Claude lo lee al inicio de cada sesión. Contiene convenciones, comandos y reglas del proyecto. |
| `.claude/settings.json` | Permisos del agente (allow / ask / deny) y hooks: auto-format con ruff + auto-actualización **bloqueante** de docs viva tras cambios en `src/`. |
| `.claude/commands/*.md` | Comandos slash personalizados: `/test`, `/lint`, `/commit`, `/review`, `/refactor`, `/audit`, `/docs`, `/spec`, `/state`, `/changelog`, `/implement-spec`. |
| `.claude/agents/*.md` | Subagentes especializados: `code-reviewer`, `test-writer`, `docs-maintainer`, `refactorer`. |
| `.mcp.json` | Configuración de servidores MCP (GitHub, context7, filesystem) — todos desactivados por defecto. |
| `pyproject.toml` | Config completa de Python: deps, ruff, mypy estricto, pytest, coverage. |
| `.gitignore` | Ignora cachés, venvs, secrets, `.claude/.cache/` y ficheros locales de Claude. |
| `.python-version` | Pinnea Python 3.12. |
| `.pre-commit-config.yaml` | Hooks de pre-commit: ruff, mypy y aviso de docs viva sin sincronizar. |
| `docs/index.md` | Mapa de la documentación. |
| `docs/STATE.md` | Estado actual del repo: arquitectura, stack, ADRs, specs. Lo mantiene Claude. |
| `docs/changelog.md` | Historial cronológico (Keep a Changelog). |
| `docs/specs/` | Specs spec-driven: `README.md`, `_template.md` y una `NNNN-slug.md` por cambio. |
| `README.md` | Quick start del proyecto. |

> ⚠ Si en `outputs/` ves ficheros `mkdocs.yml`, `scripts/gen_ref_pages.py`, `docs/getting-started.md`, `docs/installation.md`, `docs/contributing.md`, `docs/guides/` o los comandos `docs-build.md`/`docs-serve.md`/`docs-update.md`: **ignóralos**. Pertenecen a un enfoque anterior (MkDocs) descartado. Quedan vacíos con un comentario "OBSOLETO".

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

### Paso 3: copiar los ficheros a tu repo

Copia todos los ficheros de este kit a la raíz de tu proyecto Python. La estructura final debe ser:

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
│   ├── STATE.md
│   ├── changelog.md
│   └── specs/
│       ├── README.md
│       ├── _template.md
│       └── 0001-ejemplo.md
└── .claude/
    ├── settings.json
    ├── commands/
    │   ├── test.md
    │   ├── lint.md
    │   ├── commit.md
    │   ├── review.md
    │   ├── refactor.md
    │   ├── audit.md
    │   ├── docs.md
    │   ├── spec.md
    │   ├── state.md
    │   ├── changelog.md
    │   └── implement-spec.md
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
| `/spec <descripción>` | Crea una nueva spec en `docs/specs/NNNN-slug.md` con estado `Draft`. Tú la apruebas. |
| `/state` | Regenera `docs/STATE.md` con la estructura, stack, métricas y specs actuales. Preserva ADRs y contenido humano. |
| `/changelog [rango]` | Añade entradas al `docs/changelog.md` para los cambios recientes. |
| `/implement-spec <ruta>` | Implementa una spec aprobada paso a paso. Marca como Implemented y actualiza docs al terminar. |

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

`.claude/settings.json` configura cuatro hooks que mantienen el repo limpio y la documentación viva sincronizada:

1. **Auto-format Python** (`PostToolUse`): si Claude edita un `.py`, ejecuta `ruff format` y `ruff check --fix`. Cero esfuerzo de formato.

2. **Flag de cambios en `src/`** (`PostToolUse`): si Claude edita un `.py` bajo `src/`, crea `.claude/.cache/src-changed.flag`.

3. **Flag de docs tocadas** (`PostToolUse`): si Claude edita `docs/STATE.md`, `docs/changelog.md` o cualquier `docs/specs/*.md`, crea `.claude/.cache/docs-touched.flag`.

4. **Auto-actualización agresiva al terminar respuesta** (`Stop`): si existe `src-changed.flag` pero NO `docs-touched.flag`, **el hook bloquea con `exit 2`** y manda a Claude un mensaje obligando a:
   - Ejecutar `/state` para regenerar `docs/STATE.md`.
   - Ejecutar `/changelog` para añadir entradas.
   - Si implementó una spec, marcar el frontmatter como `Implemented`.

   Claude no puede cerrar la sesión hasta que las docs estén sincronizadas.

Para desactivar uno temporalmente, edita `.claude/settings.json` y comenta el bloque correspondiente.

**Si quieres saltarte la auto-actualización en una sesión puntual** (por ejemplo, estás haciendo un experimento sin importancia): borra el flag a mano antes de cerrar:
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

La documentación NO es un sitio web. Son ficheros Markdown plano dentro de `docs/`, leídos directamente desde el editor o GitHub. Tres tipos de contenido:

```
docs/
├── index.md         # Mapa de la documentación
├── STATE.md         # Estado actual del repo (auto-actualizado por Claude)
├── changelog.md     # Historial cronológico (Keep a Changelog)
└── specs/
    ├── README.md            # Índice + cómo funciona el flujo
    ├── _template.md         # Plantilla para nuevas specs
    └── NNNN-slug.md         # Specs individuales con frontmatter
```

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

### CHANGELOG.md: el histórico

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
# Crear una spec nueva
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

### Para una feature nueva (flujo spec-driven)

```
1. git checkout -b feat/nombre
2. claude
3. /spec "descripción de lo que quieres hacer"
4. (Claude crea docs/specs/NNNN-slug.md en estado Draft)
5. Revisas, editas, ajustas — y cuando estás conforme, cambias status a Approved.
6. /implement-spec docs/specs/NNNN-slug.md
7. (Claude implementa siguiendo la spec, marca como Implemented y actualiza STATE.md + changelog.md automáticamente)
8. /lint
9. /test
10. Use the code-reviewer subagent
11. /commit
12. git push origin feat/nombre  (manual)
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

## 8. Errores comunes

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

## 9. Próximos pasos

Cuando ya tengas soltura:

- Considera añadir CI con GitHub Actions ejecutando ruff + mypy + pytest en cada PR.
- Activa el MCP de GitHub para que Claude pueda leer y comentar en PRs.
- Configura Dependabot/Renovate para mantener deps al día.
- Si trabajas en equipo, comparte `CLAUDE.md` y revísalo en code reviews igual que el código.

¡Buen código!
