# mi-paquete

> Descripción breve del proyecto.

## Requisitos

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/) — instala con `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Instalación rápida

```bash
# Clona el repo
git clone <url-del-repo>
cd mi-paquete

# Sincroniza dependencias (crea .venv automáticamente)
uv sync --all-extras --dev

# Instala los hooks de pre-commit
uv run pre-commit install
```

## Comandos habituales

```bash
uv run pytest                          # Tests
uv run pytest --cov=src                # Tests + cobertura
uv run ruff check . --fix              # Lint + auto-fix
uv run ruff format .                   # Format
uv run mypy src                        # Type checking
uv run pre-commit run --all-files      # Todos los hooks
```

## Documentación

La documentación viva del proyecto está en [`docs/`](docs/):

- [`docs/index.md`](docs/index.md) — Mapa
- [`docs/STATE.md`](docs/STATE.md) — Estado actual del repo (arquitectura, decisiones, specs)
- [`docs/changelog.md`](docs/changelog.md) — Historial de cambios
- [`docs/specs/`](docs/specs/) — Specs (una por cambio significativo)

Es spec-driven: cada cambio no trivial empieza con una spec aprobada. Ver [`docs/specs/README.md`](docs/specs/README.md).

## Trabajar con Claude Code

Este repo está configurado para sacarle el máximo partido a [Claude Code](https://docs.claude.com/en/docs/claude-code/overview):

- `CLAUDE.md` describe convenciones y comandos del proyecto.
- `.claude/settings.json` define permisos seguros y un hook que auto-formatea con ruff tras cada edición.
- `.claude/commands/` contiene comandos slash personalizados: `/test`, `/lint`, `/commit`, `/review`, `/refactor`, `/docs`.
- `.claude/agents/` define dos subagentes: `code-reviewer` y `test-writer`.

Lanza Claude Code en la raíz del repo:

```bash
claude
```

## Estructura

```
.
├── src/mi_paquete/        # Código del paquete
├── tests/                 # Tests pytest
├── docs/                  # Documentación viva (STATE, changelog, specs)
├── pyproject.toml         # Config completa del proyecto
├── CLAUDE.md              # Memoria de Claude Code
└── .claude/               # Comandos, subagentes y settings
```

## Licencia

MIT
