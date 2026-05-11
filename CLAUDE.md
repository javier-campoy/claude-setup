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
- **Documentación viva**: ficheros Markdown en `docs/` (`STATE.md`, `changelog.md`, `specs/`, `modules/`). Sin generación de sitio. Se lee desde el editor o GitHub.
- **Pre-commit**: `pre-commit` con ruff, mypy y aviso de docs viva sin sincronizar.

## Estructura del proyecto

```
.
├── src/<paquete>/        # Código fuente del paquete
├── tests/                # Tests pytest (mirror de src/)
├── docs/                 # Documentación viva del repo
│   ├── index.md          # Mapa de la documentación
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
└── .claude/              # Configuración de Claude Code
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

## Reglas para Claude (importante)

1. **Antes de escribir código**, lee los ficheros relevantes con `Read` y orienta tus cambios al estilo existente.
2. **Cuando edites código**, ejecuta lint/format/tests al terminar (el hook lo hace automáticamente para format).
3. **No instales dependencias** sin pedir confirmación. Si necesitas una nueva dep, propón la línea para `pyproject.toml` y espera aprobación.
4. **No hagas push directo a `main`**. Trabaja siempre en ramas `feat/...`, `fix/...`.
5. **Tests primero cuando arreglemos un bug**: reproduce el bug en un test que falle, luego arregla.
6. **No suprimas warnings** ni bypassees `mypy`/`ruff` con `# type: ignore` o `# noqa` salvo que sea imprescindible y comentado.
7. **Comentarios**: explica el *por qué*, no el *qué*. El código debe ser autoexplicativo.
8. **Si algo es ambiguo, pregunta**. Mejor una pregunta corta que una refactorización equivocada.

## Documentación viva: cómo funciona

La documentación de este repo NO se publica como sitio web. Son ficheros Markdown plano dentro de `docs/`, leídos desde el editor o desde GitHub. Cuatro tipos de contenido:

- **`docs/STATE.md`** — Estado actual del repo: arquitectura, módulos, stack, ADRs (decisiones técnicas) y tabla de specs activas/implementadas. Lo regenera Claude tras cambios en `src/`.
- **`docs/changelog.md`** — Historial cronológico (formato [Keep a Changelog](https://keepachangelog.com/es/1.1.0/)). Sección `[No publicado]` se rellena tras cada cambio.
- **`docs/specs/NNNN-slug.md`** — Una spec por unidad de cambio. Frontmatter con estado: `Draft` → `Approved` → `Implemented` (o `Rejected`). El proyecto es **spec-driven**: cualquier cambio no trivial empieza con una spec aprobada.
- **`docs/modules/<modulo>.md`** — Documentación detallada de cada módulo Python en `src/`: API pública, responsabilidad, dependencias internas y ejemplos de uso. Un fichero por módulo, generado y mantenido automáticamente por Claude.

### Flujo spec-driven (obligatorio para cambios no triviales)

```
1. /spec "qué quieres"          → crea docs/specs/NNNN-slug.md (Draft)
2. revisas, editas, apruebas    → cambias status a Approved
3. /implement-spec docs/specs/NNNN-slug.md
                                 → Claude implementa siguiendo la spec
                                 → marca como Implemented
                                 → actualiza STATE.md + changelog.md
                                 → hace commit y push automáticamente
```

Hotfixes triviales (typos, format, errores obvios de 1-2 líneas) pueden saltarse el spec.

### Hooks que mantienen la doc viva sincronizada

1. **Tras editar `.py` bajo `src/`** → un hook marca un flag interno `.claude/.cache/src-changed.flag`.
2. **Tras editar `docs/STATE.md`, `docs/changelog.md` o cualquier `docs/specs/*.md`** → marca `.claude/.cache/docs-touched.flag`.
3. **Al terminar la respuesta (`Stop` hook)**: si hay flag de src/ pero no de docs/, **el hook bloquea con `exit 2`** y obliga a Claude a continuar y actualizar `STATE.md` + `changelog.md` antes de cerrar la sesión.
4. **Pre-commit `docs-sync-check`**: si commiteas cambios en `src/` sin tocar `docs/`, **bloquea el commit** (exit 1).

### Hooks de control de versiones (pre-commit, commit-msg, pre-push)

Instala los tres tipos con:
```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

| Hook | Cuándo | Qué hace |
|---|---|---|
| `protect-main-branch` | pre-commit | Bloquea commits directos a `main`/`master`. Usa ramas `feat/...`, `fix/...`. |
| `docs-sync-check` | pre-commit | Bloquea si hay cambios en `src/` sin actualizar `docs/`. |
| `gitleaks` | pre-commit | Escanea secrets: tokens, API keys, connection strings, etc. |
| `conventional-commits` | commit-msg | Valida que el mensaje siga el formato `<tipo>[(<scope>)]: <resumen>`. |
| `pre-push-quality-gate` | pre-push | Ejecuta `ruff check` + `mypy src` + `pytest` antes de subir al remoto. |

### Reglas para Claude sobre la doc viva

- Tras CUALQUIER cambio no trivial en `src/`, **debes** actualizar `docs/STATE.md`, `docs/changelog.md` y el `docs/modules/<modulo>.md` afectado ANTES de terminar la sesión. El hook lo va a forzar; mejor hazlo proactivamente.
- Si implementas una spec, marca su frontmatter `status: Implemented` y `implemented_in: <commit>` y muévela en STATE.md de "Activas" a "Implementadas".
- Si tomas una decisión técnica relevante (cambio de librería, cambio de patrón arquitectónico), **propón** un ADR en `STATE.md` sección 4. NO lo añadas sin confirmación humana.
- Si el cambio en `src/` no tiene spec asociada y es no trivial, **propón crear una spec retroactiva** con `/spec`. NO inventes specs sin pedir antes.
- Si creas o renombras un módulo, crea/renombra también su `docs/modules/<modulo>.md` correspondiente.
- Si eliminas un módulo, mueve su doc a un comentario en `docs/modules/README.md` con el commit en que se eliminó (no la borres del todo).
- NUNCA borres ADRs ni specs implementadas. Son histórico.
- NUNCA edites `docs/specs/_template.md` ni `docs/modules/_template.md` salvo que el usuario lo pida.

## Subagentes disponibles

- `code-reviewer` — Revisa cambios buscando bugs, problemas de seguridad y mejoras de diseño.
- `test-writer` — Genera tests pytest exhaustivos para código existente.
- `docs-maintainer` — Audita coherencia código ↔ docs viva. Úsalo cuando sospeches que `STATE.md`, `changelog.md`, las specs o los `modules/*.md` no reflejan la realidad del código.
- `refactorer` — Mantiene el repo coherente con la visión global de `docs/STATE.md` y los ADRs. Detecta drift arquitectónico, deuda estructural, duplicación e inconsistencias. Propone refactors priorizados; aplica los pequeños tras confirmación, sugiere `/spec` para los grandes.

Invócalos con: `Use the code-reviewer subagent to review my recent changes`.

## Comandos slash personalizados

- `/test` — Ejecuta la suite de tests con cobertura.
- `/lint` — Ejecuta ruff y mypy y arregla lo que pueda.
- `/review` — Lanza una revisión de los cambios pendientes.
- `/commit` — Crea un commit siguiendo Conventional Commits a partir del diff.
- `/refactor` — Refactoriza un fichero respetando las convenciones del proyecto.
- `/audit [ámbito]` — Auditoría arquitectónica vía subagente `refactorer`. Compara contra `docs/STATE.md` y los ADRs, propone refactors priorizados.
- `/docs` — Genera/actualiza docstrings en un fichero concreto y sincroniza el `docs/modules/<modulo>.md` correspondiente.
- `/spec <descripción>` — Crea una nueva spec en `docs/specs/` (estado Draft).
- `/state` — Regenera `docs/STATE.md` con la estructura, stack, métricas y specs actuales, y sincroniza los `docs/modules/*.md`.
- `/changelog [rango]` — Añade entradas al `docs/changelog.md` para los cambios recientes.
- `/implement-spec <ruta>` — Implementa una spec aprobada paso a paso, actualizando docs (STATE.md, changelog, modules/), haciendo commit y push al terminar.

## Notas y decisiones de diseño

<!-- Añade aquí decisiones técnicas relevantes que Claude deba conocer -->
- (vacío) — Documenta aquí cualquier decisión arquitectónica importante.
