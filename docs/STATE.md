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
- **Alternativas**: Solo issues de GitHub, RFCs en una wiki externa, nada formal.
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

---

## 6. Estado del codebase

### Métricas

- **Líneas de código** (src/): _(la rellena Claude con `find src -name '*.py' \| xargs wc -l \| tail -1`)_
- **Cobertura de tests**: _(la rellena Claude con `uv run pytest --cov=src` si está disponible)_
- **Issues conocidos**: _ver `docs/specs/` con estado `Draft` o GitHub Issues._

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

| Workflow | Trigger | Qué hace |
|---|---|---|
| [`ci.yml`](.github/workflows/ci.yml) | Push / PR a `main` | ruff check · ruff format · mypy · pytest + cobertura |
| [`release.yml`](.github/workflows/release.yml) | Tag `v*.*.*` | Gate de calidad · `uv build` · GitHub Release con changelog |

### Estrategia de versioning

[Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

| Tipo | Cuándo |
|---|---|
| `PATCH` | Hotfixes y correcciones sin nueva API pública |
| `MINOR` | Features nuevas, compatibles hacia atrás |
| `MAJOR` | Cambios breaking de API |

**Flujo de release**: specs implementadas y mergeadas a `main` → `/release X.Y.Z` → tag → GitHub Release automático.

### Historial de releases

| Versión | Fecha | Specs incluidas | Notas |
|---|---|---|---|
| _(pendiente)_ | | | Primera release |

<!-- Claude: actualiza esta tabla al ejecutar /release -->
