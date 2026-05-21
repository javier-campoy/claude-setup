# Planes de campaña

Una **campaña** es un loop autónomo y acotado que persigue un objetivo de la visión ejecutando el flujo spec-driven con dos agentes que se turnan: uno **implementa** y otro **critica**. Lo orquesta el comando [`/campaign`](../../.claude/commands/campaign.md).

> 🧭 La campaña no inventa dirección: se ancla a un objetivo o tema de [`docs/VISION.md`](../VISION.md) y avanza specs aprobadas. Es la capa de *ejecución* sobre el flujo `/vision → /spec → /implement-spec`.

## Para qué sirve

Aclarar de forma razonable los `_[VERIFICAR]_` de bajo riesgo y converger una implementación que cumpla los criterios de aceptación, sin tener al humano vigilando cada paso — pero **parando ante cualquier decisión consecuente**.

## Las piezas

| Pieza | Rol |
|---|---|
| `/campaign` | **Orquestador** (agente principal): planifica, lanza los subagentes, decide y registra. Único que puede orquestar a otros. |
| `spec-implementer` | Subagente que implementa una ronda de una spec, resuelve `_[VERIFICAR]_` de bajo riesgo y corre el gate de calidad. |
| `spec-critic` | Subagente **read-only** que critica de forma adversarial y emite veredicto `APROBAR` / `REVISAR` / `ESCALAR`. Modelo distinto al implementer. |
| `docs/plans/NNNN-slug.md` | Estado durable de la campaña: directriz, criterios de "hecho", log de iteraciones, cola de escalación y decisiones registradas. |

## Los dos tiers de `_[VERIFICAR]_`

| Marcador | Quién lo resuelve |
|---|---|
| `_[VERIFICAR]_` | Bajo riesgo. El implementer **propone** una resolución y el crítico la **valida**; si pasa, se aplica y queda registrada (sección 6 del plan). |
| `_[VERIFICAR:humano]_` | Consecuente (producto, breaking change, ADR, seguridad). **Siempre escala**: va a la cola (sección 5), el loop se pausa y te pregunta. |

> El comando manual `/implement-spec` mantiene su gate **estricto** (bloquea ante cualquier `_[VERIFICAR]_`). La auto-resolución tipada ocurre **solo** dentro de `/campaign`.

## El bucle (v1: una spec)

```
/campaign docs/specs/NNNN-slug.md
 │
 ├─ [checkpoint inicial] el orquestador propone plan + criterios de "hecho" +
 │   rama + caps  → tú confirmas
 │
 └─ ronda r = 1..rounds_per_spec:
      spec-implementer  → implementa / atiende el feedback de la ronda previa,
                          resuelve _[VERIFICAR]_ seguros, corre ruff+mypy+pytest
      spec-critic       → veredicto:
          APROBAR  → commit en la rama, marca la spec Implemented, FIN ✅
          REVISAR  → feedback al log, otra ronda (si r < cap)
          ESCALAR  → cola de escalación, PAUSA, te pregunta
      (cap de rondas alcanzado sin converger → escala)
 │
 └─ FIN: reporte contra los criterios de "hecho". NUNCA merge/push sin ti.
```

## Guardarraíles

- **Rama por campaña** (`feature/campaign-<slug>`); nunca push ni merge sin tu visto bueno.
- **El gate de calidad es la verdad de terreno**: `ruff + mypy + pytest` deben pasar para que el crítico pueda aprobar.
- **Caps** de rondas por spec y de specs por campaña: cortan loops infinitos y coste descontrolado.
- **Checkpoints humanos** en: arranque, escalaciones, cambios de ADR/visión y reporte final.

## Estado del comando

- **v1** (actual): una sola spec aprobada por campaña.
- **v2** (futuro): secuencia multi-spec replanificable, anclada al "hecho" de un objetivo de visión completo.
