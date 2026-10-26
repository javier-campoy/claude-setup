# CLAUDE.md

> Este fichero es la "memoria" principal del proyecto. Claude Code lo lee automáticamente al iniciar cualquier sesión. Mantenlo actualizado: cuanto mejor describa tu proyecto, mejores resultados obtendrás.

## Resumen del proyecto

<!-- Reemplaza con la descripción de tu proyecto -->
Proyecto Python (paquete/librería). Stack moderno basado en `uv`, `ruff` y `pytest`.

## Stack y herramientas

- **Python**: 3.12+ (ver `.python-version`)
- **Gestor de paquetes / entorno**: [`uv`](https://docs.astral.sh/uv/)
- **Lint + format**: [`ruff`](https://docs.astral.sh/ruff/) (sustituye a black, isort, flake8)
- **Type checking**: `mypy` (modo estricto)
- **Tests**: `pytest` + `pytest-cov`
- **Documentación viva**: ficheros Markdown en `docs/` (`VISION.md`, `STATE.md`, `changelog.md`, `specs/`, `modules/`). Sin generación de sitio. Se lee desde el editor o GitLab.
- **Pre-commit**: `pre-commit` con ruff, mypy y aviso de docs viva sin sincronizar.

## Estructura del proyecto

```
.
├── src/<paquete>/        # Código fuente del paquete
├── tests/                # Tests pytest (mirror de src/)
├── docs/                 # Documentación viva del repo
│   ├── index.md          # Mapa de la documentación
│   ├── VISION.md         # Norte del proyecto: dirección a futuro (humano, precede a las specs)
│   ├── STATE.md          # Estado actual: arquitectura, stack, ADRs, specs
│   ├── changelog.md      # Historial cronológico (Keep a Changelog)
│   ├── specs/            # Specs (una por cambio significativo)
│   │   ├── README.md
│   │   ├── _template.md
│   │   └── NNNN-slug.md
│   └── modules/          # Documentación por módulo (auto-generada)
│       ├── README.md     # Índice de módulos
│       ├── _template.md  # Plantilla
│       └── <modulo>.md   # Un fichero por módulo en src/
├── pyproject.toml        # Config del proyecto (deps, ruff, pytest, mypy)
├── .python-version       # Versión de Python pinneada
├── .claude/              # Comandos, subagentes, skills, hooks y settings
└── .gitlab-ci.yml        # CI/CD (gate de calidad y release)
```

> Convenciones de espejo:
> - Tests: `tests/test_<modulo>.py` ↔ `src/<paquete>/<modulo>.py`
> - Docs de módulo: `docs/modules/<modulo>.md` ↔ `src/<paquete>/<modulo>.py`
> - Para paquetes anidados: `src/<paquete>/sub/bar.py` → `docs/modules/sub.bar.md`

## Comandos habituales

Ejecuta estos comandos para verificar tu trabajo. Si modificas el flujo, actualiza esta sección.

```bash
# Instalar / sincronizar dependencias
uv sync --all-extras --dev

# Instalar hooks de git (primera vez o tras clonar)
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

# Ejecutar tests
uv run pytest                          # Todos los tests
uv run pytest tests/test_foo.py        # Un fichero
uv run pytest -k "nombre_test"         # Filtrar por nombre
uv run pytest --cov=src --cov-report=term-missing   # Con cobertura

# Lint y format
uv run ruff check .                    # Lint
uv run ruff check . --fix              # Lint + auto-fix
uv run ruff format .                   # Format

# Type checking
uv run mypy src

# Todo lo anterior antes de commit
uv run ruff check . --fix && uv run ruff format . && uv run mypy src && uv run pytest
```

## Convenciones de código

- **Type hints obligatorios** en funciones públicas y firmas de clase. `mypy --strict` debe pasar.
- **Docstrings estilo Google** en todo lo que sea API pública.
- **Imports**: ordenados por ruff (isort integrado). Imports absolutos desde `src/<paquete>`.
- **Nombres**: `snake_case` para funciones/variables, `PascalCase` para clases, `SCREAMING_SNAKE` para constantes.
- **Errores**: usa excepciones específicas; nunca `except:` o `except Exception:` sin logging.
- **Logging**: usar `logging.getLogger(__name__)`, nunca `print()` en código de producción.
- **Funciones pequeñas y puras** siempre que sea posible. Si una función supera ~50 líneas, considera dividirla.

## Convenciones de tests

- Todo cambio de código debe ir acompañado de tests.
- Usar `pytest` con fixtures, parametrize y marcadores apropiados.
- Tests rápidos y aislados. Mockear I/O externo (red, FS, DB).
- Cobertura objetivo: **≥85%** en `src/`.
- Nombres descriptivos: `test_<funcion>_<escenario>_<resultado_esperado>`.

## Git y commits

- **Conventional Commits**: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `perf:`.
- Una unidad lógica por commit; mensajes en imperativo y en español o inglés (consistente).
- Rebase preferido sobre merge para mantener el historial lineal.
- **Nunca commitees sin haber pasado**: `ruff check . && ruff format . && mypy src && pytest`.
- **`develop`** es la rama de integración. **`main`** queda reservada para releases (el hook `protect-main-branch` bloquea commits directos a `main`/`master`).
- **Dos modos de trabajo válidos**, según el tamaño del cambio:
  - **Directo en `develop`** — para hotfixes, typos y cambios pequeños. Commit en `develop`, `push` a `origin/develop`, CI en verde.
  - **Worktree por rama** — para specs, features grandes o trabajo paralelo. Cada cambio vive en su propio worktree sobre una rama `feat/...` o `fix/...` que parte de `develop` limpio (`baseRef: fresh` en `.claude/settings.json`).
- **Flujo worktree** (recomendado para specs):
  1. `EnterWorktree` (o `claude --worktree`) crea un árbol aislado en una rama nueva partiendo de `origin/develop`. `.venv` y las cachés se symlinkean desde el repo principal — no se duplican.
  2. Trabajo aislado en ese worktree: commits, lint, tests, push de la rama si quieres CI/backup remoto.
  3. **Al cerrar la rama**: merge a `develop` desde el repo principal (`git merge --no-ff feat/<slug>` o merge request si lo prefieres), borra la rama local y remota, sal del worktree con `ExitWorktree` (que limpia el árbol).
  4. `develop` → `main` sólo en `/release <versión>`.
- Múltiples worktrees pueden coexistir (uno por spec/feature en marcha). Cada uno tiene su rama; sólo se mergean a `develop` cuando se cierran.

## CI/CD y releases

- **CI** (`.gitlab-ci.yml`, job `quality`): ruff + mypy + pytest en cada push a `develop`/`main` (y en cualquier merge request).
- **Releases**: cuando `develop` está estable se integra en `main` y se publica con `/release <versión>` sobre `main`:
  - Bump en `pyproject.toml` + rename `[No publicado]` → `[X.Y.Z]` en changelog.
  - `git tag vX.Y.Z` → el pipeline de GitLab construye el paquete y crea el GitLab Release con el contenido del changelog.
- **Forja**: GitLab (`code.mahitahi.global.fujitsu.com`). Para issues, merge requests y pipelines usa `glab` si está instalado, o el MCP `gitlab` de `.mcp.json`. No uses `gh`.
- **Versionado semántico** (`MAJOR.MINOR.PATCH`):
  - `PATCH` — hotfixes y correcciones sin nueva API pública.
  - `MINOR` — features nuevas, compatibles hacia atrás.
  - `MAJOR` — cambios breaking de API.

## Reglas para Claude (importante)

1. **Antes de escribir código**, lee los ficheros relevantes con `Read` y orienta tus cambios al estilo existente.
2. **Cuando edites código**, ejecuta lint/format/tests al terminar (el hook lo hace automáticamente para format).
3. **No instales dependencias** sin pedir confirmación. Si necesitas una nueva dep, propón la línea para `pyproject.toml` y espera aprobación.
4. **Elige el modo de trabajo según el cambio**: cambios pequeños van directos a `develop` (commit + push a `origin/develop`); specs y features grandes van en su propio worktree sobre una rama `feat/...`/`fix/...` (parte de `origin/develop` limpio vía `baseRef: fresh`) y se mergean a `develop` al cerrar. **Nunca commitees ni hagas push a `main`/`master`** (reservadas para releases; el hook `protect-main-branch` las bloquea).
5. **Tests primero cuando arreglemos un bug**: reproduce el bug en un test que falle, luego arregla.
6. **No suprimas warnings** ni bypassees `mypy`/`ruff` con `# type: ignore` o `# noqa` salvo que sea imprescindible y comentado.
7. **Comentarios**: explica el *por qué*, no el *qué*. El código debe ser autoexplicativo.
8. **Si algo es ambiguo, pregunta**. Mejor una pregunta corta que una refactorización equivocada.
9. **Toda spec se crea con `/spec`, sin excepciones.** Nunca redactes una spec a mano en `docs/specs/` ni "pegues" texto directamente en un fichero `NNNN-slug.md`. Si el usuario te pide una spec, lanza `/spec "<descripción>"`. El comando se encarga de la numeración, el frontmatter, la verificación de la visión, la clasificación de trivialidad y el encadenamiento automático de `/spec-review` cuando toca. Si el usuario te describe un cambio no trivial sin decir explícitamente "spec", **propónle crearla con `/spec`** antes de tocar código.

## Documentación viva: cómo funciona

La documentación de este repo NO se publica como sitio web. Son ficheros Markdown plano dentro de `docs/`, leídos desde el editor o desde GitLab. Cinco tipos de contenido:

- **`docs/VISION.md`** — El **norte del proyecto**: hacia dónde vamos y por qué (propósito, objetivos, no-objetivos, principios rectores, temas estratégicos). Es **prescriptivo y de propiedad humana**, evoluciona deliberadamente (con `/vision`) y se construye **antes** de la primera spec. No lo regenera `/state`. A diferencia de `STATE.md` (presente, autogenerado), `VISION.md` define el futuro y es la referencia contra la que se justifica toda spec.
- **`docs/STATE.md`** — Estado actual del repo: arquitectura, módulos, stack, ADRs (decisiones técnicas), tabla de specs activas/implementadas y **§5.5 "Directrices vigentes para próximas specs"** (tabla de IDs `D-NN` citables que cada nueva spec debe honrar). Lo regenera Claude tras cambios en `src/`, **excepto §5.5 que se preserva** (es contenido humano-curado + auto-añadidos por `/implement-spec` con confirmación). Su sección 1 enlaza a `VISION.md` (no la duplica).
- **`docs/changelog.md`** — Historial cronológico (formato [Keep a Changelog](https://keepachangelog.com/es/1.1.0/)). Sección `[No publicado]` se rellena tras cada cambio.
- **`docs/specs/NNNN-slug.md`** — Una spec por unidad de cambio. Frontmatter con estado: `Draft` → `Approved` → `Implemented` (o `Rejected`). El proyecto es **spec-driven**: cualquier cambio no trivial empieza con una spec aprobada.
- **`docs/modules/<modulo>.md`** — Documentación detallada de cada módulo Python en `src/`: API pública, responsabilidad, dependencias internas y ejemplos de uso. Un fichero por módulo, generado y mantenido automáticamente por Claude.

### Flujo spec-driven (obligatorio para cambios no triviales)

```
0. /vision "describe el proyecto"   (una vez, antes de la primera spec)
                                 → crea/rellena docs/VISION.md (el norte)
                                 → la revisas y ajustas; evoluciona luego con /vision
1. /spec "qué quieres"          → verifica que la visión existe (si no, te manda a /vision)
                                 → lee VISION (§4 objetivos + §12.1 directrices estratégicas
                                   + §12.2 ideas registradas + §12.3 ideas futuras)
                                   y STATE (§5.5 directrices tácticas)
                                 → crea docs/specs/NNNN-slug.md (Draft), alineada con el norte
                                 → en la spec: cita directrices D-NN / DV-NN que cumple/cierra/abre
                                   y objetivos de VISION §4 que cierra
                                 → clasifica la spec (trivial vs no trivial)
                                 → si es no trivial, encadena AUTOMÁTICAMENTE /spec-review
                                   (Opus, subagente spec-architect)
                                       · NO reescribe la spec: detecta incoherencias con
                                         la visión, choques con ADRs, boundaries mal
                                         trazados, conflictos con otras specs activas
                                       · inserta subsección "Revisión arquitectónica"
                                       · veredicto: GO | GO-WITH-CHANGES | RETHINK
                                 → si es trivial, no consume Opus
                                 → opt-out: pasar `--skip-review` en el argumento de /spec
                                 → propone (con confirmación humana) añadir entrada en
                                   VISION §12.2 "Ideas de specs registradas"
                                 → propone (con confirmación humana) consolidar ideas
                                   previas de §12.3 que cubre + extraer ideas nuevas
                                   para futuras specs (secciones 4/7/8/9 de la spec)
2. revisas, editas, apruebas    → cambias status a Approved
                                 (no apruebes si el veredicto fue RETHINK)
3. /implement-spec docs/specs/NNNN-slug.md
                                 → Claude implementa siguiendo la spec (en Sonnet)
                                 → marca como Implemented
                                 → actualiza STATE.md + changelog.md + modules/
                                 → cierra directrices D-NN declaradas; propone nuevas con confirmación
                                 → propone (con confirmación humana) marcar [x] los objetivos
                                   de VISION §4 que la spec cierra y mover la entrada de
                                   §12.2 a Implemented (operaciones de cierre, nunca estructurales)
                                 → propone (con confirmación humana) añadir a §12.3 las
                                   ideas para futuras specs detectadas en sección 10
                                 → hace commit y push automáticamente
```

> Nota: `/spec-review` también puede invocarse a mano sobre una spec ya existente (p.ej. revisión adicional tras editarla). Pero en el flujo normal, lo dispara `/spec` automáticamente.

La **visión es el nexo**: precede a las specs y se toma de referencia en sprints, specs y decisiones técnicas. No es inmutable — evoluciona con `/vision` conforme el proyecto aprende.

Hotfixes triviales (typos, format, errores obvios de 1-2 líneas) pueden saltarse el spec.

### Cuándo usar Opus (gate de arquitectura)

El flujo usa **Sonnet por defecto** (generar e implementar) y **Opus como árbitro** en los dos puntos de revisión (arquitectura de specs y revisión de código):

- **Generación de specs**: Sonnet (`/spec`).
- **Validación arquitectónica de specs no triviales**: Opus (`/spec-review`, subagente `spec-architect`). Se dispara **automáticamente** desde `/spec` cuando la heurística de trivialidad lo marca; también puede invocarse a mano sobre una spec ya creada.
- **Implementación**: Sonnet (`/implement-spec`).
- **Revisión de código**: Opus (subagente `code-reviewer`).
- **Refactor y mantenimiento de docs**: Sonnet (subagentes `refactorer`, `docs-maintainer`).

`/spec-review` se ejecuta (automática o manualmente) cuando la spec:

- Introduce un módulo nuevo o reorganiza módulos existentes.
- Toca boundaries entre componentes (responsabilidades cruzadas).
- Cambia o introduce API pública.
- Solapa o depende de otra spec activa.
- Toma una decisión de diseño que podría acabar en ADR.

**No** se ejecuta para CRUD locales, hotfixes, refactors cosméticos o specs que no alteran contratos entre módulos: el coste no se justifica. La heurística vive en `/spec`.

Para forzar saltar la revisión en una spec que la heurística marcaría como no trivial, pasa `--skip-review` en el argumento de `/spec`. Úsalo con criterio.

Reglas duras:

- El subagente `spec-architect` **nunca reescribe** specs ni genera código. Es validador.
- `/spec-review` es el **único punto de entrada** autorizado para invocar `spec-architect`. `/spec` lo encadena; ningún otro comando llama al subagente directamente.
- `/implement-spec` **advierte** si una spec parece no trivial y no pasó por `/spec-review` (caso típico: specs antiguas o creadas con `--skip-review`); **no bloquea** salvo que la revisión existente tenga veredicto `RETHINK`.
- Si `spec-architect` devuelve veredicto `RETHINK`, **no apruebes la spec** ni la implementes hasta resolver la conversación pendiente.

### Hooks que mantienen la doc viva sincronizada

Los hooks están en `.claude/hooks/` y configurados en `.claude/settings.json`:

1. **Auto-format** (`PostToolUse`): si Claude edita un `.py`, ejecuta `ruff format` + `ruff check --fix` automáticamente.
2. **Tras editar `.py` bajo `src/`** → marca `.claude/.cache/src-changed.flag`.
3. **Tras editar `docs/STATE.md`, `docs/changelog.md` o `docs/specs/*.md`** → marca `.claude/.cache/docs-touched.flag`.
4. **Al terminar la respuesta (`Stop` hook)**: si hay flag de src/ pero no de docs/, **bloquea con `exit 2`** y obliga a Claude a actualizar docs antes de cerrar la sesión.
5. **Pre-commit `docs-sync-check`**: si commiteas cambios en `src/` sin tocar `docs/`, **bloquea el commit** (exit 1). Es una heurística de *presencia* (¿se tocó algún doc?).
6. **Cobertura de documentación** (`.claude/hooks/check_doc_coverage.py`): gate determinista que comprueba *contenido*, no solo presencia. Sobre los `src/*.py` que vas a commitear verifica que (a) toda función/clase/método público tenga docstring, (b) cada módulo con API pública tenga su `docs/modules/<modulo>.md`, (c) cada módulo con API pública esté referenciado en `docs/STATE.md` (captura el módulo nuevo/renombrado que no llega al estado del repo), y (d) la sección `[No publicado]` del changelog tenga entradas. Lo usan dos capas:
   - La skill `/commit`, que lo ejecuta y **auto-remedia** los huecos (vía `/docs`, `/state` y `/changelog`) antes de commitear.
   - El hook `pre-commit doc-coverage`, que es el backstop determinista para `git commit` manual (bloquea con exit 1).
7. **Gate de consistencia specs ↔ STATE §5** (`.claude/hooks/check_spec_state_sync.py`): verifica que el `status` de cada spec (Draft/Approved/Implemented/Rejected) coincida con la tabla en la que aparece en `docs/STATE.md` §5. Lo ejecuta `/implement-spec` en su paso 7h antes de commitear; sale con código 1 si hay discrepancias.

### Hooks de control de versiones (pre-commit, commit-msg, pre-push)

Instala los tres tipos con:
```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

| Hook | Cuándo | Qué hace |
|---|---|---|
| `protect-main-branch` | pre-commit | Bloquea commits directos a `main`/`master`. El desarrollo va en `develop` o en ramas `feat/...`/`fix/...`. |
| `docs-sync-check` | pre-commit | Bloquea si hay cambios en `src/` sin actualizar `docs/` (presencia). |
| `doc-coverage` | pre-commit | Bloquea si el código staged no está documentado: docstrings públicos, `docs/modules/<modulo>.md`, referencia en `docs/STATE.md` y changelog `[No publicado]` (contenido). |
| `gitleaks` | pre-commit | Escanea secrets: tokens, API keys, connection strings, etc. |
| `conventional-commits` | commit-msg | Valida que el mensaje siga el formato `<tipo>[(<scope>)]: <resumen>`. |
| `pre-push-quality-gate` | pre-push | Ejecuta `ruff check` + `mypy src` + `pytest` antes de subir al remoto. |

### Reglas para Claude sobre la doc viva

- **La visión (`docs/VISION.md`) es el norte.** Toda spec debe poder justificarse contra ella. `/spec` exige que esté rellenada; si no lo está, deriva al usuario a `/vision` antes de crear specs.
- **VISION es de propiedad humana — pero tiene excepciones acotadas.** La regla general sigue siendo: ningún comando edita VISION libremente. Solo se admiten estas operaciones automatizadas, **todas con confirmación humana explícita** antes de aplicar:
  - **Aditiva a §12.2 (`/spec` paso 7.5)**: añadir entrada en `§12.2 "Ideas de specs registradas"` con id, slug, fecha y resumen 1-línea de la spec recién creada.
  - **Aditiva + de cierre en §12.3 (`/spec` paso 7.6 y `/implement-spec` paso 7c.bis)**: añadir ideas para futuras specs en `§12.3 "Ideas para futuras specs"` extraídas de la spec actual. `/spec` también puede **marcar como `consolidada en NNNN-<slug>`** una idea propuesta que la nueva spec cubre.
  - **De cierre en §4/§12.2 (`/implement-spec` pasos 7e/7f)**: marcar como `[x]` los objetivos del roadmap `§4` que la spec implementada cierra completamente (no solo avanza) y cambiar la entrada correspondiente de `§12.2` a `Implemented` con el hash del commit. Solo cambia los checkboxes y la nota de implementación, nunca el texto del objetivo.
  - **Cualquier otro cambio en VISION** (principios, objetivos nuevos, no-objetivos, temas estratégicos, §12.1 directrices estratégicas) **requiere `/vision`** y revisión humana. `/state` no edita VISION nunca.
- Si detectas que el código o una spec contradicen la visión (persiguen un no-objetivo, violan un principio), **NO lo resuelvas en silencio**: avisa y sugiere `/vision` para actualizar el norte o replantear el trabajo.
- **Directrices vigentes para próximas specs** (`docs/STATE.md` §5.5):
  - Cada nueva spec debe declarar en su frontmatter (`directives_followed`, `directives_closed`, `directives_opened`) y en su subsección "Directrices que esta spec cumple, cierra o abre" qué directrices `D-NN` (de §5.5) y/o `DV-NN` (de VISION §12.1) honra, cierra o propone añadir.
  - `/spec` exige citas; `/implement-spec` cierra las declaradas y propone (con confirmación) añadir las nuevas.
  - `/state` **preserva** §5.5 íntegra — no la regenera ni reordena.
  - Las directrices **estratégicas** (norte) viven en VISION §12.1 con prefijo `DV-NN` y solo se editan con `/vision`. Las **tácticas** (arquitectura, calidad, producto, backlog) viven en STATE §5.5 con prefijo `D-NN`.
- Tras CUALQUIER cambio no trivial en `src/`, **debes** actualizar `docs/STATE.md`, `docs/changelog.md` y el `docs/modules/<modulo>.md` afectado ANTES de terminar la sesión. El hook lo va a forzar; mejor hazlo proactivamente.
- Si implementas una spec, marca su frontmatter `status: Implemented` y `implemented_in: <commit>` y muévela en STATE.md de "Activas" a "Implementadas".
- Si tomas una decisión técnica relevante (cambio de librería, cambio de patrón arquitectónico), **propón** un ADR en `STATE.md` sección 4. NO lo añadas sin confirmación humana.
- Si el cambio en `src/` no tiene spec asociada y es no trivial, **propón crear una spec retroactiva** con `/spec`. NO inventes specs sin pedir antes.
- Si creas o renombras un módulo, crea/renombra también su `docs/modules/<modulo>.md` correspondiente.
- Si eliminas un módulo, mueve su doc a un comentario en `docs/modules/README.md` con el commit en que se eliminó (no la borres del todo).
- NUNCA borres ADRs ni specs implementadas. Son histórico.
- NUNCA edites `docs/specs/_template.md` ni `docs/modules/_template.md` salvo que el usuario lo pida.

## Subagentes disponibles

- `code-reviewer` — Revisa cambios buscando bugs, problemas de seguridad y mejoras de diseño. (Opus)
- `test-writer` — Genera tests pytest exhaustivos para código existente. (Sonnet)
- `docs-maintainer` — Audita coherencia código ↔ docs viva. Úsalo cuando sospeches que `STATE.md`, `changelog.md`, las specs o los `modules/*.md` no reflejan la realidad del código. (Sonnet)
- `refactorer` — Mantiene el repo coherente con el norte de `docs/VISION.md` y la arquitectura/ADRs de `docs/STATE.md`. Detecta drift respecto al norte, drift arquitectónico, deuda estructural, duplicación e inconsistencias. Propone refactors priorizados; aplica los pequeños tras confirmación, sugiere `/spec` para los grandes. (Sonnet)
- `spec-architect` — **Árbitro de arquitectura** para specs en `Draft`. NO genera ni reescribe specs: valida coherencia estructural contra `VISION.md`, `STATE.md`, ADRs y otras specs activas. También detecta **specs gordas** (mezclan varios cambios conceptuales, tocan demasiados módulos, fases desacopladas, criterios de aceptación independientes) y propone trocearlas en sub-specs atómicas con nombres concretos y orden de implementación — una spec demasiado grande dispara el coste de `/implement-spec` (más contexto cargado, más iteraciones, más cuota quemada). Devuelve un veredicto (`GO` / `GO-WITH-CHANGES` / `RETHINK`) y un diff conceptual mínimo. **Opus; úsalo solo vía `/spec-review`** y solo en specs no triviales.

Invócalos con: `Use the code-reviewer subagent to review my recent changes`. La excepción es `spec-architect`: se lanza siempre a través de `/spec-review`, nunca directamente.

## Skills disponibles

Las skills viven en `.claude/skills/<nombre>/SKILL.md` y Claude las carga solo cuando el tema aparece, así que no ocupan contexto en el resto de sesiones.

- `fujitsu-ai-architecture` — Arquitectura de referencia de Fujitsu AI para aplicaciones de IA en producción: cinco principios obligatorios, mapa de módulos, guardarraíles, observabilidad y evaluación. **Cárgala siempre** que diseñes, especifiques, implementes o revises código que llame a un modelo o LLM, haga RAG u orqueste agentes. `/spec`, `/review`, `code-reviewer` y `spec-architect` la usan en esos casos.

## Comandos slash personalizados

- `/test` — Ejecuta la suite de tests con cobertura.
- `/lint` — Ejecuta ruff y mypy y arregla lo que pueda.
- `/review` — Lanza una revisión de los cambios pendientes.
- `/commit` — Crea un commit siguiendo Conventional Commits a partir del diff. Antes de commitear corre el gate de calidad (ruff + pytest) y la auditoría de cobertura de documentación, auto-remediando docstrings y `docs/modules/` que falten.
- `/refactor` — Refactoriza un fichero respetando las convenciones del proyecto.
- `/audit [ámbito]` — Auditoría arquitectónica vía subagente `refactorer`. Compara contra `docs/STATE.md` y los ADRs, propone refactors priorizados.
- `/docs` — Genera/actualiza docstrings en un fichero concreto y sincroniza el `docs/modules/<modulo>.md` correspondiente.
- `/vision [descripción]` — Crea o evoluciona `docs/VISION.md`, el norte del proyecto. Se usa una vez antes de la primera spec, y luego cuando cambia la dirección (registrando la revisión).
- `/spec <descripción> [--skip-review]` — Crea una nueva spec en `docs/specs/` (estado Draft). Exige que la visión esté rellenada. Clasifica la spec como trivial o no trivial y, si es no trivial, **encadena automáticamente `/spec-review`** sobre el draft. Pasa `--skip-review` para saltarte esa pasada por Opus.
- `/spec-review <ruta-spec>` — Revisión arquitectónica de una spec por el subagente `spec-architect` (Opus). Único punto donde se usa Opus en el flujo. Se invoca automáticamente desde `/spec` para specs no triviales; también puede ejecutarse a mano sobre una spec ya creada (p.ej. tras editarla manualmente). Inserta una subsección "Revisión arquitectónica" en la spec con veredicto y cambios mínimos.
- `/state` — Regenera `docs/STATE.md` con la estructura, stack, métricas y specs actuales, y sincroniza los `docs/modules/*.md`.
- `/changelog [rango]` — Añade entradas al `docs/changelog.md` para los cambios recientes.
- `/implement-spec <ruta>` — Implementa una spec aprobada paso a paso, actualizando docs (STATE.md, changelog, modules/), haciendo commit y push al terminar.
- `/release <versión>` — Prepara y publica una nueva versión: bump en `pyproject.toml`, actualiza changelog, crea tag `vX.Y.Z` y hace push (el pipeline de GitLab crea el Release).

## Notas y decisiones de diseño

<!-- Añade aquí decisiones técnicas relevantes que Claude deba conocer -->
- (vacío) — Documenta aquí cualquier decisión arquitectónica importante.
