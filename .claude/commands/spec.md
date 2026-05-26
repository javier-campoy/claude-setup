---
description: Crea una nueva spec en docs/specs/ a partir de una descripción
allowed-tools: Read, Write, Glob, Bash(ls:*), Bash(git log:*), Bash(date:*)
argument-hint: "<descripción breve de la feature/cambio>"
---

Crea una spec nueva siguiendo el flujo spec-driven del proyecto.

## Procedimiento

0. **Comprueba la visión (gate)**:
   - Lee `docs/VISION.md`.
   - Si **no existe** o **sigue siendo la plantilla** (frase-norte sin rellenar, secciones con `_[VERIFICAR]_` en Propósito/Visión/Objetivos), **para** y avisa: "No hay una visión del proyecto rellenada. La visión se construye antes de redactar specs: ejecuta `/vision \"describe tu proyecto\"` primero."
   - Si está rellenada, continúa y tenla presente: la spec debe avanzar el norte definido en ella.

1. **Contexto**:
   - Lee `docs/VISION.md` para conocer el norte (objetivos, no-objetivos, principios, temas estratégicos).
   - Lee `docs/STATE.md` para entender el estado actual del repo.
   - Lee `docs/specs/_template.md` para conocer la estructura.
   - Mira `docs/specs/` (con `ls`) para determinar el siguiente número (`NNNN`): el máximo existente + 1, formateado a 4 dígitos.

2. **Slug**:
   - A partir de $ARGUMENTS, deriva un slug corto: minúsculas, palabras separadas por guiones, sin tildes, máximo ~5 palabras.
   - Ejemplo: "Quiero un parser de URLs" → `parser-de-urls`.

3. **Crea el fichero**: `docs/specs/NNNN-slug.md` copiando la plantilla y rellenando:
   - Frontmatter:
     - `id`: NNNN
     - `title`: título descriptivo en una línea
     - `status`: Draft
     - `created` y `updated`: fecha de hoy (`date +%Y-%m-%d`)
     - `author`: si lo conoces, déjalo en blanco si no
   - Sección 1 (Resumen): 2-4 frases basadas en $ARGUMENTS.
   - Sección 2 (Motivación): infiere casos de uso plausibles. Marca con `_[VERIFICAR]_` lo que no puedas inferir con seguridad.
     - **Subsección "Alineación con la visión"**: indica qué objetivo(s) y tema(s) estratégico(s) de `docs/VISION.md` avanza esta spec (p.ej. "Avanza O2 dentro del tema T1"). Si no encaja con ningún objetivo del norte, **dilo explícitamente** y propón al usuario revisar la visión o reconsiderar la spec — no fuerces el encaje.
   - Secciones 3-9: rellena con tu mejor entendimiento, marcando `_[VERIFICAR]_` donde haga falta input humano.
   - Sección 10: déjala vacía (la rellenarás al implementar).

4. **Actualiza el índice** en `docs/specs/README.md`:
   - Añade una fila a la tabla "Índice de specs".

5. **Actualiza `docs/STATE.md`** sección 5 (Specs → Activas).

6. **Clasifica la spec** (trivial vs no trivial) aplicando esta heurística sobre el borrador. Considéralo **no trivial** si se cumple **al menos uno** de estos puntos:
   - Introduce un **módulo nuevo** o reorganiza módulos existentes.
   - Toca **boundaries** entre componentes (responsabilidades cruzadas).
   - Cambia o introduce **API pública**.
   - **Solapa o depende** de otra spec activa (mira `related:` y `docs/STATE.md` sección 5).
   - Toma una decisión de diseño que podría acabar en **ADR**.

   Anota la clasificación y la razón en un par de frases para mostrarla al usuario en el paso 8.

7. **Si la spec es no trivial → encadena `/spec-review` automáticamente**:
   - Avisa al usuario en una línea: "Spec clasificada como no trivial (`<razón>`). Lanzo `/spec-review` (consume Opus) sobre `docs/specs/NNNN-slug.md`."
   - Ejecuta `/spec-review docs/specs/NNNN-slug.md`. Sigue el procedimiento de ese comando íntegro (carga visión + estado + specs relacionadas, invoca al subagente `spec-architect`, muestra el output, pide confirmación para insertarlo en la spec).
   - El veredicto que devuelva (`GO` / `GO-WITH-CHANGES` / `RETHINK`) se traslada al reporte final del paso 8.
   - **No pidas permiso para lanzar `/spec-review` por defecto**: si la heurística marca la spec como no trivial, se ejecuta. La única excepción: si el usuario invocó `/spec` con la cadena literal `--skip-review` en $ARGUMENTS, sáltatelo y avísalo en el reporte.
   - **Si la spec es trivial** (CRUD local, hotfix, refactor cosmético, cambio de mensaje, etc.) → **NO** lances `/spec-review`. Continúa al paso 8 directamente. Es importante: `spec-review` consume Opus y no aporta valor en specs triviales.

8. **Reporta al usuario**:
   - Ruta del fichero creado.
   - Clasificación de triviality y razón (paso 6).
   - Lista de los `_[VERIFICAR]_` que necesitan revisión humana.
   - Si se ejecutó `/spec-review`: veredicto del subagente y, en caso de `GO-WITH-CHANGES`, recordatorio de revisar los cambios mínimos. En caso de `RETHINK`, **NO** sugieras aprobar la spec.
   - Recordatorio de cambiar `status: Draft` → `status: Approved` cuando esté lista (solo si no hubo `RETHINK`).

## Reglas

- **NO inventes** comportamiento técnico no pedido. Si $ARGUMENTS no especifica algo crítico, marca `_[VERIFICAR]_` en lugar de adivinar.
- **NO implementes** código aquí. Solo se crea la spec.
- **NO invoques al subagente `spec-architect` directamente.** Si la spec es no trivial, encadena `/spec-review`, que es el único punto de entrada autorizado al subagente Opus. Mantiene la traza y el control de coste.
- **NO lances `/spec-review` en specs triviales.** La heurística existe para no quemar Opus. Si dudas, fuerza la clasificación con criterio: "¿este cambio toca contratos entre módulos?". Si la respuesta es no, es trivial.
- Si $ARGUMENTS está vacío, pide al usuario que describa qué quiere especificar.
- **Sin visión no hay spec.** Si `docs/VISION.md` no está rellenada, deriva primero a `/vision` (paso 0). Toda spec debe poder justificarse contra el norte.
