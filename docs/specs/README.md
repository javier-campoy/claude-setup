# Specs

Cada cambio significativo del proyecto empieza con una **spec**: un documento Markdown que describe el problema, la solución propuesta y los criterios de aceptación. Las specs se aprueban **antes** de implementar.

> 🧭 **Antes de la primera spec, define el norte en [`docs/VISION.md`](../VISION.md).** Toda spec debe poder justificarse contra la visión (objetivos, no-objetivos, principios). El comando `/spec` lo exige: si la visión no está rellenada, te derivará a `/vision`. Cada spec declara en su frontmatter (`vision_refs`) y en su sección "Alineación con la visión" qué objetivo(s) del norte avanza.

## Convenciones

- **Nombre**: `NNNN-slug-corto.md` donde `NNNN` es un número secuencial de 4 dígitos.
  - Ejemplo: `0001-parser-de-urls.md`, `0002-cache-en-memoria.md`.
- **Estado**: en el frontmatter de cada spec: `Draft` → `Approved` → `Implemented` (o `Rejected`).
- **Una spec por unidad de cambio coherente**. Si tocas tres cosas no relacionadas, son tres specs.

### Marcadores `_[VERIFICAR]_` (dos tiers)

`/spec` siembra `_[VERIFICAR]_` allí donde no puede inferir algo con seguridad. Hay dos niveles según quién puede resolverlos:

| Marcador | Significado | Quién lo resuelve |
|---|---|---|
| `_[VERIFICAR]_` | Detalle de bajo riesgo (no toca producto, API pública, seguridad ni dirección). | Tú al revisar la spec; o, dentro de una campaña `/campaign`, el `spec-implementer` proponiéndolo y el `spec-critic` validándolo. |
| `_[VERIFICAR:humano]_` | Decisión consecuente (producto, breaking change, ADR, seguridad, trade-off estratégico). | **Solo tú.** Nunca lo resuelve un agente. |

`/implement-spec` (manual) **bloquea ante cualquier `_[VERIFICAR]_`**: espera una spec ya aclarada. La auto-resolución tipada de los de bajo riesgo ocurre **solo** dentro de `/campaign` (ver [`docs/plans/`](../plans/)).

## Ciclo de vida

```
  (VISION.md como norte de fondo)
       │
┌─────────┐     /spec    ┌───────────┐   revisión    ┌──────────┐  /implement-spec  ┌─────────────┐
│  idea   │  ─────────▶  │   Draft   │  ──────────▶  │ Approved │  ──────────────▶  │ Implemented │
└─────────┘              └───────────┘               └──────────┘                   └─────────────┘
                                │
                                │ rechazo
                                ▼
                          ┌───────────┐
                          │ Rejected  │
                          └───────────┘
```

## Crear una spec

```
/spec "descripción breve de lo que quieres"
```

Claude:
1. Lee `STATE.md` para entender el contexto del repo.
2. Asigna el siguiente número (`NNNN`).
3. Crea `docs/specs/NNNN-slug.md` usando la plantilla en `_template.md`.
4. Estado inicial: `Draft`.

Tú revisas, editas, y cuando estás conforme cambias el campo `status` a `Approved`.

## Implementar una spec

```
/implement-spec docs/specs/NNNN-slug.md
```

Claude:
1. Lee la spec.
2. Verifica que su estado es `Approved`. Si no, para.
3. Implementa los cambios siguiendo la spec **al pie de la letra**.
4. Si en mitad encuentra algo que no encaja con la spec, **NO improvisa**: para y lo discute.
5. Al terminar:
   - Marca la spec como `Implemented` con commit/PR de referencia.
   - Actualiza `docs/STATE.md` (movida de Active → Implemented).
   - Añade entrada en `docs/changelog.md`.

## Plantilla

Ver [`_template.md`](_template.md). Cópialo y rellénalo cuando quieras escribir una spec a mano.

## Índice de specs

> Esta tabla la mantiene Claude. La fuente de verdad sigue siendo el frontmatter de cada fichero.

| ID | Título | Estado | Owner | Última actualización |
|---|---|---|---|---|
| _(vacío)_ | | | | |
