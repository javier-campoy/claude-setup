# Estado del repositorio

> Documento vivo: refleja el estado actual del repo en cualquier momento. Lo mantiene Claude automáticamente tras cada cambio en `src/`. **No lo edites a mano salvo correcciones puntuales** — tu próxima ejecución de `/state` o el hook automático lo regenerará.
>
> **Última actualización**: _(la rellena Claude)_
> **Commit base**: _(la rellena Claude — `git rev-parse --short HEAD`)_

---

## 1. Visión general

_Resumen del proyecto en 3-5 líneas: qué hace, para quién, qué problema resuelve (estado actual)._

> 🧭 **La dirección a futuro vive en [`VISION.md`](VISION.md)** — el norte del proyecto (objetivos, no-objetivos, principios, temas estratégicos). Este apartado solo resume el presente; no dupliques la visión aquí.

---

## 2. Arquitectura y módulos

### Diagrama mental

```
src/mi_paquete/
├── __init__.py           # API pública del paquete
├── ...                   # (Claude rellena con la estructura real)
```

### Módulos

| Módulo | Responsabilidad | Depende de | Lo consumen |
|---|---|---|---|
| `mi_paquete.foo` | _qué hace_ | `bar`, `baz` | tests, CLI |

### Flujos clave

_Diagramas mentales de los flujos principales (request → handler → DB, etc.)._

---

## 3. Stack y dependencias

### Runtime

| Tecnología | Versión | Motivo |
|---|---|---|
| Python | 3.12+ | Type hints completos, mejor performance |

### Desarrollo

| Herramienta | Versión | Motivo |
|---|---|---|
| uv | latest | Gestor de paquetes rápido y reproducible |
| ruff | >=0.6 | Lint + format en una sola herramienta |
| mypy | >=1.11 | Type checking estricto |
| pytest | >=8.0 | Tests |
| pre-commit | >=3.7 | Gates de calidad antes de commit |

---

## 4. Decisiones técnicas (ADRs inline)

> Cada decisión importante se documenta aquí con: contexto, decisión, alternativas consideradas, consecuencias.

### ADR-001: Adopción de uv como gestor de paquetes

- **Fecha**: YYYY-MM-DD
- **Estado**: Aceptada
- **Contexto**: Necesitamos un gestor de paquetes rápido y reproducible.
- **Decisión**: Usar `uv` en lugar de pip o poetry.
- **Alternativas**: pip + pip-tools, poetry, pdm.
- **Consecuencias**: Builds más rápidos. Lock file (`uv.lock`) en git.

### ADR-002: Documentación spec-driven

- **Fecha**: YYYY-MM-DD
- **Estado**: Aceptada
- **Contexto**: Necesitamos trazabilidad de los cambios y un mecanismo para alinear con Claude antes de implementar.
- **Decisión**: Cada cambio no trivial empieza con una spec en `docs/specs/` que se aprueba antes de tocar código.
- **Alternativas**: Solo issues de GitLab, RFCs en una wiki externa, nada formal.
- **Consecuencias**: Más overhead inicial pero mucho mejor alineamiento humano-IA y mejor histórico.

<!-- Claude: añade aquí nuevas ADRs cuando se tomen decisiones técnicas relevantes. Numéralas secuencialmente. -->

---

## 5. Specs

### Activas (Draft / Approved, no implementadas)

| ID | Título | Estado | Fichero |
|---|---|---|---|
| _(vacío)_ | | | |

### Implementadas

| ID | Título | Implementada en | Fichero |
|---|---|---|---|
| _(vacío)_ | | | |

### Rechazadas / archivadas

| ID | Título | Motivo | Fichero |
|---|---|---|---|
| _(vacío)_ | | | |

### Directrices vigentes para próximas specs

> **Qué son**: reglas tácticas que las nuevas specs deben honrar para mantener coherencia con la arquitectura, los ADRs vigentes y las decisiones de producto. Cada directriz tiene un **ID citable** (`D-NN`) que las specs declaran en su frontmatter (`directives_followed` / `directives_closed`) y en la subsección "Directrices que esta spec cumple, cierra o abre".
>
> **Cómo se mantiene**: `/spec` exige que la nueva spec cite las directrices que honra. `/implement-spec` propone en el cierre qué directrices quedan cerradas (las puntuales) y qué directrices nuevas emergen (con confirmación humana antes de añadirlas). `/state` **preserva** esta tabla — no la regenera. Las directrices estratégicas (norte del proyecto) viven en `VISION.md` §12.1 con prefijo `DV-NN` y solo se editan con `/vision`.
>
> **Estado**: `vigente` (debe cumplirse) · `cerrada` (cumplida por la spec X; queda como histórico) · `derogada` (superseded por ADR / spec posterior; ver nota).
>
> **Cómo rellenar esta tabla**: ve añadiendo directrices conforme tomes decisiones técnicas (cada nuevo ADR suele abrir una directriz `D-NN` derivada), conforme cierres specs (las del backlog se cierran al implementarse) y conforme `/implement-spec` proponga directrices emergentes. Empieza con pocas, focalízalas en lo realmente vinculante.

| ID | Origen | Ámbito | Directriz | Estado |
|---|---|---|---|---|
| _(vacío — añade tu primera directriz cuando tomes la primera decisión técnica vinculante)_ | | | | |

---

## 6. Estado del codebase

### Métricas

- **Líneas de código** (src/): _(la rellena Claude con `find src -name '*.py' \| xargs wc -l \| tail -1`)_
- **Cobertura de tests**: _(la rellena Claude con `uv run pytest --cov=src` si está disponible)_
- **Issues conocidos**: _ver `docs/specs/` con estado `Draft` o los issues de GitLab._

### Salud

- ✅ / ❌ Lint (`ruff check .`)
- ✅ / ❌ Types (`mypy src`)
- ✅ / ❌ Tests (`pytest`)

---

## 7. Roadmap inmediato

_Qué viene a continuación. Suele ser un resumen de las specs en estado `Approved`._

- [ ] (vacío)

---

## 8. CI/CD y versioning

### Pipelines

Definidos en [`.gitlab-ci.yml`](../.gitlab-ci.yml):

| Job | Trigger | Qué hace |
|---|---|---|
| `quality` | Merge request · push a `develop`/`main` · tag `v*.*.*` | ruff check · ruff format · mypy · pytest + cobertura |
| `build` | Tag `v*.*.*` | `uv build` (artefactos en `dist/`) |
| `release` | Tag `v*.*.*` | GitLab Release con la sección del changelog |

### Estrategia de versioning

[Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

| Tipo | Cuándo |
|---|---|
| `PATCH` | Hotfixes y correcciones sin nueva API pública |
| `MINOR` | Features nuevas, compatibles hacia atrás |
| `MAJOR` | Cambios breaking de API |

**Flujo de release**: specs implementadas y mergeadas a `main` → `/release X.Y.Z` → tag → GitLab Release automático.

### Historial de releases

| Versión | Fecha | Specs incluidas | Notas |
|---|---|---|---|
| _(pendiente)_ | | | Primera release |

<!-- Claude: actualiza esta tabla al ejecutar /release -->
