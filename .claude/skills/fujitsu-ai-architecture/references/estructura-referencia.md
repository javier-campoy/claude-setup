# Árbol de proyecto de referencia

Adaptación del *Reference Project Tree* de la guía de Fujitsu AI al layout del kit: el código va bajo `src/<paquete>/`, los tests bajo `tests/` y la documentación en `docs/`. El contexto para asistentes de IA (`ai_context/` en la guía original) ya lo cubren `CLAUDE.md` y `.claude/`, así que no se crea una carpeta aparte.

Es una referencia, no una plantilla: crea solo las carpetas que el proyecto use.

```text
proyecto/
├─ src/<paquete>/
│  ├─ app/                    # Application Layer
│  │  ├─ main.py              # Entry point (API / worker)
│  │  ├─ config.py            # Configuración global (modelo, proveedor, umbrales)
│  │  └─ schemas.py           # Modelos de petición / respuesta
│  │
│  ├─ components/             # Componentes de IA reutilizables de bajo nivel
│  │  ├─ retrieval/
│  │  │  ├─ hybrid.py         # Recuperación semántica + palabras clave
│  │  │  └─ ranking.py        # Re-ranking
│  │  ├─ embedding.py
│  │  └─ loaders.py
│  │
│  ├─ services/               # Lógica de negocio y orquestación
│  │  ├─ pipelines/
│  │  │  ├─ inference.py      # Flujo de inferencia extremo a extremo
│  │  │  └─ training.py
│  │  ├─ cache.py
│  │  ├─ memory.py
│  │  ├─ routing.py           # Selección de modelo / proveedor
│  │  └─ rewriting.py         # Reescritura de consultas
│  │
│  ├─ prompts/                # Registro de prompts y políticas
│  │  ├─ templates/
│  │  │  ├─ system.md
│  │  │  ├─ user.md
│  │  │  └─ tools.md
│  │  └─ registry.py          # Versionado y resolución de prompts
│  │
│  ├─ agents/                 # Capa agéntica
│  │  ├─ planners.py
│  │  ├─ graders.py
│  │  ├─ decomposers.py
│  │  ├─ routers.py
│  │  └─ executors.py
│  │
│  ├─ tools/                  # Capacidades externas enchufables
│  │  ├─ search.py
│  │  ├─ database.py
│  │  ├─ apis.py
│  │  └─ filesystem.py
│  │
│  ├─ security/               # Guardarraíles y cumplimiento
│  │  ├─ input_validation.py
│  │  ├─ content_filtering.py
│  │  ├─ output_validation.py
│  │  └─ policy_engine.py
│  │
│  ├─ evaluation/             # Calidad y aseguramiento de la IA
│  │  ├─ offline.py
│  │  ├─ online.py
│  │  └─ metrics.py
│  │
│  └─ observability/          # Monitorización y trazabilidad
│     ├─ tracing.py
│     ├─ logging.py
│     ├─ metrics.py
│     ├─ feedback.py
│     └─ cost_tracking.py
│
├─ data/                      # Fuera de git si es pesado o con licencia
│  ├─ raw/
│  ├─ processed/
│  └─ index_config/
│
├─ evaluation_data/
│  └─ golden.json             # Dataset dorado (sí se versiona)
│
├─ scripts/                   # Scripts operativos y de ciclo de vida
│  ├─ bootstrap.py
│  ├─ migrate.py
│  └─ healthcheck.py
│
├─ frontend/                  # UI opcional, con ciclo de vida propio
│
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  ├─ e2e/
│  └─ conftest.py
│
├─ docs/                      # Documentación viva del kit
│  ├─ VISION.md
│  ├─ STATE.md                # Arquitectura (equivale a architecture.md)
│  ├─ modules/                # Contratos de API por módulo (equivale a api.md)
│  ├─ specs/
│  ├─ deployment.md           # Añadir al ir a producción
│  └─ runbook.md              # Añadir al ir a producción
│
├─ docker-compose.yml
├─ pyproject.toml
├─ .env.example               # Variables necesarias, sin valores reales
├─ CLAUDE.md                  # AI Assistant Context
└─ .claude/                   # AI Assistant Context
```

## Diferencias respecto al árbol original

- **`app/`, `components/`, `services/`, etc.** pasan a `src/<paquete>/` para respetar el layout `src/` y la configuración de `pyproject.toml` del kit.
- **`evaluation/datasets/golden.json`** sale de `src/` a `evaluation_data/`: los datos no forman parte del paquete instalable.
- **`docs/architecture.md` y `docs/api.md`** se corresponden con `docs/STATE.md` y `docs/modules/`, que el kit ya mantiene sincronizados con sus hooks.
- **`ai_context/`** no se crea: su papel lo cumplen `CLAUDE.md` y `.claude/`.
- **`app/Dockerfile`** y **`frontend/Dockerfile`** se omiten del árbol; añádelos cuando el proyecto se contenedorice.
