---
description: Revisión arquitectónica de una spec en Draft vía el subagente spec-architect (Opus). Úsalo solo en specs no triviales antes de aprobarlas.
allowed-tools: Read, Edit, Glob, Grep, Bash(ls:*), Bash(date:*)
argument-hint: "<ruta a docs/specs/NNNN-slug.md>"
---

Lanza una **revisión arquitectónica** sobre la spec indicada. Es el único punto del flujo en que se usa Opus: como árbitro de coherencia estructural, no como redactor.

## Cuándo usar este comando

Sí — antes de aprobar una spec que:

- Introduce un módulo nuevo o reordena módulos existentes.
- Toca boundaries entre componentes (qué responsabilidad vive dónde).
- Cambia o introduce API pública.
- Solapa o depende de otras specs activas.
- Toma una decisión de diseño no obvia (puede acabar en un ADR).

No — para specs que:

- Son CRUD locales, refactors triviales o hotfixes.
- Solo cambian un texto, un valor por defecto, un mensaje de error.
- No alteran contratos entre módulos.

Si dudas, hazlo: es barato y deja traza. Si claramente no aplica, sáltatelo.

## Procedimiento

1. **Carga la spec** indicada en $ARGUMENTS:
   - Si no se pasa ruta, lista las specs en estado `Draft` con `ls docs/specs/` y pide al usuario cuál revisar.
   - Verifica el frontmatter `status`:
     - Si es `Approved` → avisa: "Esta spec ya está aprobada. La revisión arquitectónica está pensada para el estado Draft, antes de aprobar. ¿Quieres revisarla igualmente?" y espera confirmación.
     - Si es `Implemented` o `Rejected` → para. No tiene sentido revisar arquitectura sobre una spec ya cerrada.
     - Si es `Draft` → continúa.

2. **Detecta si ya pasó revisión**:
   - Con Grep, busca la cadena `## Revisión arquitectónica` en la spec.
   - Si ya existe, pregunta al usuario: "Esta spec ya tiene revisión arquitectónica del YYYY-MM-DD con veredicto X. ¿Quieres una nueva pasada (sobrescribe la anterior) o cancelar?"

3. **Lanza el subagente `spec-architect`** con un prompt que le dé exactamente:
   - La ruta de la spec objetivo.
   - La lista de specs activas relevantes (otras specs `Draft` o `Approved` cuyo dominio se solape, detectadas leyendo `docs/STATE.md` sección 5 y los frontmatter `related:`).
   - Instrucción explícita: "Lee `docs/VISION.md`, `docs/STATE.md`, la spec objetivo y las specs relacionadas que te paso. Aplica tu procedimiento y devuelve la subsección 'Revisión arquitectónica' lista para insertar en la spec, con la fecha de hoy."

   Ejemplo de invocación:

   ```
   Use the spec-architect subagent to review docs/specs/0007-foo.md.
   Specs relacionadas a tener en cuenta: docs/specs/0005-bar.md, docs/specs/0006-baz.md.
   ```

4. **Muestra el output del subagente al usuario** y pregunta:
   - "¿Quieres que inserte esta revisión en la spec ahora?" (Sí / No / Editar antes).

5. **Si el usuario aprueba la inserción**:
   - Inserta el bloque devuelto por el subagente **justo antes de** `## 10. Decisiones durante la implementación` en la spec.
   - Actualiza el frontmatter:
     - `updated: <fecha de hoy>` (`date +%Y-%m-%d`).
   - Actualiza `docs/changelog.md` bajo `[No publicado]` con una entrada del tipo: `Revisión arquitectónica añadida a spec NNNN — veredicto: GO|GO-WITH-CHANGES|RETHINK`.

6. **Acción según veredicto**:
   - **GO**: informa al usuario "Spec estructuralmente sana. Puedes cambiar `status` a `Approved` cuando quieras."
   - **GO-WITH-CHANGES**: aplica los cambios mínimos **con criterio**, según el procedimiento de abajo. El objetivo es dejar la spec preparada para que el humano solo tenga que cambiar `status: Draft → Approved`.
   - **RETHINK**: para. Explica la razón al usuario y sugiere conversación humana, posible `/vision` o reformulación de la spec. No avances ni propongas aprobar.

### Procedimiento para `GO-WITH-CHANGES`

El subagente `spec-architect` (Opus) entrega cada cambio mínimo como un patch ejecutable: ubicación + tipo (`insertar | reemplazar | mover | eliminar | REQUIERE-HUMANO`) + texto exacto. Confía en su criterio — las decisiones de bajo nivel (nombrado, dónde encaja una responsabilidad, redacción de un boundary) son suyas, no del humano.

Recorre los cambios en orden:

- **`insertar | reemplazar | mover | eliminar`** → aplícalos con `Edit` usando exactamente el texto que da el subagente. No reinterpretes, no pulas redacción, no añadas adornos. Si el `Original` no se encuentra en la spec, no inventes: márcalo como pendiente con la nota "no localizado en la spec — revisar".
- **`REQUIERE-HUMANO`** → no apliques. El propio subagente reconoce que necesita input externo. Déjalo pendiente con su pregunta tal cual.

Tras procesarlos, **añade al final de la subsección "Revisión arquitectónica"** un bloque así:

```markdown
### Cambios aplicados automáticamente

- _(uno por línea, con referencia a la sección de la spec que se tocó)_

### Pendientes de decisión humana

- _(uno por línea, con la pregunta concreta para el humano)_
```

Si no hay cambios en alguno de los dos cubos, omite esa subsección (no dejes encabezados vacíos).

Reporta al usuario en una línea: "Apliqué N/M cambios mínimos. Quedan K para tu decisión." Si `K == 0`, añade: "La spec está lista para `Approved` cuando la revises."

## Reglas duras

- **Solo Opus aquí.** Este comando es el único punto autorizado para invocar a Opus en el flujo de specs. No lo uses como atajo para "revisar mejor" cualquier cosa.
- **El subagente nunca reescribe la spec.** Quien aplica los cambios mínimos en `GO-WITH-CHANGES` es esta skill (Sonnet), no `spec-architect`. La regla del subagente sigue intacta.
- **No apruebes la spec.** El cambio `Draft → Approved` lo hace el humano, siempre. Tu trabajo termina cuando la revisión queda registrada y los cambios mecánicos aplicados.
- **Si la visión no está rellenada**, el subagente devolverá `RETHINK` apuntando a `/vision`. Reenvía ese mensaje al usuario sin maquillarlo.
- **No invoques a `spec-architect` desde otros comandos sin pasar por aquí.** Punto único de entrada = control de coste.
