---
description: Crea una nueva spec en docs/specs/ a partir de una descripción
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Bash(git log:*), Bash(date:*)
argument-hint: "<descripción breve de la feature/cambio>"
---

Crea una spec nueva siguiendo el flujo spec-driven del proyecto.

## Procedimiento

0. **Comprueba la visión (gate)**:
   - Lee `docs/VISION.md`.
   - Si **no existe** o **sigue siendo la plantilla** (frase-norte sin rellenar, secciones con `_[VERIFICAR]_` en Propósito/Visión/Objetivos), **para** y avisa: "No hay una visión del proyecto rellenada. La visión se construye antes de redactar specs: ejecuta `/vision \"describe tu proyecto\"` primero."
   - Si está rellenada, continúa y tenla presente: la spec debe avanzar el norte definido en ella.

1. **Contexto**:
   - Lee `docs/VISION.md` para conocer el norte (objetivos, no-objetivos, principios, temas estratégicos). Localiza también:
     - **§12.1 "Directrices estratégicas vigentes"** (si existe) — tabla de IDs `DV-NN` que la nueva spec debe honrar.
     - **§12.2 "Ideas de specs registradas"** (si existe) — para conocer ideas previas y no duplicar.
     - **§12.3 "Ideas para futuras specs"** (si existe). Si una entrada en `propuesta` describe lo que esta nueva spec cubre, anótalo: en el paso 7.6 propondrás marcarla como `consolidada en NNNN-<slug>` (operación de cierre con confirmación humana, no automática).
   - Lee `docs/STATE.md` para entender el estado actual del repo. Presta atención específica a **§5.5 "Directrices vigentes para próximas specs"** — tabla de IDs `D-NN` (tácticas) que la nueva spec debe honrar o cerrar.
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
     - `vision_refs`: lista de objetivos/temas que avanza, p.ej. `["O2", "T1"]`.
     - `directives_followed`: lista de IDs `D-NN` (STATE §5.5) y/o `DV-NN` (VISION §12.1) que la spec honra. **Rellénala con criterio**: cita las que aplican al ámbito, no todas.
     - `directives_closed`: lista de IDs `D-NN` que esta spec **cierra** (típicamente del backlog).
     - `directives_opened`: lista de IDs propuestos `D-NN` (siguiente número libre tras la última directriz de §5.5) para directrices nuevas que **emergen** de la spec. Vacía si no abre ninguna. `/implement-spec` propondrá añadirlas a §5.5 al cerrar, con confirmación humana.
     - `vision_idea_ref`: déjalo vacío. Lo rellena este propio comando en el paso 7.5 si el usuario confirma registrar la idea en VISION §12.2.
   - Sección 1 (Resumen): 2-4 frases basadas en $ARGUMENTS.
   - Sección 2 (Motivación): infiere casos de uso plausibles. Marca con `_[VERIFICAR]_` lo que no puedas inferir con seguridad.
     - **Subsección "Alineación con la visión"**:
       - Indica qué objetivo(s) y tema(s) estratégico(s) de `docs/VISION.md` avanza esta spec (p.ej. "Avanza O2 dentro del tema T1"). Coordínalo con el frontmatter `vision_refs`.
       - Lista los **objetivos que esta spec cierra completamente** (no solo avanza). `/implement-spec` los usará en el paso 7e para proponer marcarlos `[x]` en VISION §4 con confirmación humana.
       - Si no encaja con ningún objetivo del norte, **dilo explícitamente** y propón al usuario revisar la visión o reconsiderar la spec — no fuerces el encaje.
     - **Subsección "Directrices que esta spec cumple, cierra o abre"**: rellena la tabla del template con las directrices del frontmatter (`directives_followed` → "cumple", `directives_closed` → "cierra", `directives_opened` → "abre (propone)"). Una fila por directriz, con nota breve explicando cómo la honra.
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
   - **Abre directrices nuevas** (frontmatter `directives_opened` no vacío) o **cierra una directriz vigente** que no era de backlog (p.ej. cierra una directriz arquitectónica, derogándola con un ADR nuevo).

   Anota la clasificación y la razón en un par de frases para mostrarla al usuario en el paso 8.

7. **Si la spec es no trivial → encadena `/spec-review` automáticamente**:
   - Avisa al usuario en una línea: "Spec clasificada como no trivial (`<razón>`). Lanzo `/spec-review` (consume Opus) sobre `docs/specs/NNNN-slug.md`."
   - Ejecuta `/spec-review docs/specs/NNNN-slug.md`. Sigue el procedimiento de ese comando íntegro (carga visión + estado + specs relacionadas, invoca al subagente `spec-architect`, muestra el output, pide confirmación para insertarlo en la spec).
   - El veredicto que devuelva (`GO` / `GO-WITH-CHANGES` / `RETHINK`) se traslada al reporte final del paso 8.
   - **No pidas permiso para lanzar `/spec-review` por defecto**: si la heurística marca la spec como no trivial, se ejecuta. La única excepción: si el usuario invocó `/spec` con la cadena literal `--skip-review` en $ARGUMENTS, sáltatelo y avísalo en el reporte.
   - **Si la spec es trivial** (CRUD local, hotfix, refactor cosmético, cambio de mensaje, etc.) → **NO** lances `/spec-review`. Continúa al paso 7.5 directamente. Es importante: `spec-review` consume Opus y no aporta valor en specs triviales.

7.5. **Registra la idea en `docs/VISION.md` §12.2 (operación aditiva con confirmación humana)**:
   - Localiza la subsección **§12.2 "Ideas de specs registradas"** en `docs/VISION.md`. Si no existe todavía, informa al usuario: "VISION no tiene §12.2 — ejecuta `/vision` con la propuesta que te paso para crearla, y reintenta `/spec`." y termina aquí.
   - Si existe: prepara una entrada nueva con este formato exacto:
     ```markdown
     - **NNNN — `<slug>`** _(estado: Draft, registrado: YYYY-MM-DD)_ — `<resumen 1 línea desde sección 1 de la spec>`. Avanza: `<lista de vision_refs>`. _Implementada en: pendiente._
     ```
   - **Pide confirmación al usuario** mostrando la entrada literal: "Voy a añadir esta entrada en `docs/VISION.md` §12.2 como registro de la idea. ¿Procedo? (sí / no / editar)".
     - Si **sí**: aplica el `Edit` aditivo (solo añadir una línea al final de la lista de §12.2; no toques nada más). Rellena `vision_idea_ref: "§12.2 idea NNNN"` en el frontmatter de la spec.
     - Si **no**: salta el registro y deja `vision_idea_ref: ""`. Anótalo en el reporte del paso 8.
     - Si **editar**: pide al usuario el texto exacto que prefiera y aplícalo.
   - **NUNCA** edites otras secciones de VISION desde aquí. Si crees que la spec exige un cambio del norte, **NO lo apliques**: informa al usuario y deriva a `/vision`.

7.6. **Captura de ideas para futuras specs en VISION §12.3 (operación aditiva + de cierre con confirmación humana)**:
   - Localiza la subsección **§12.3 "Ideas para futuras specs"** en `docs/VISION.md`. Si no existe, salta este paso e infórmalo al usuario.
   - **a) Consolidación de ideas previas**: si en el paso 1 detectaste alguna entrada en `propuesta` de §12.3 que esta spec cubre, prepara la transformación: `<slug> ... Estado: propuesta.` → `<slug> ... Estado: consolidada en NNNN-<slug>.`. Pide confirmación literal mostrando el diff. Si **sí**, aplica el `Edit`.
   - **b) Extracción de ideas nuevas de la spec recién creada**: escanea las secciones de la spec en este orden:
     - Sección 4 "Alternativas consideradas" (columna "Por qué no") — busca menciones tipo "queda para spec futura", "se difiere a otra spec", "spec posterior".
     - Sección 7 "Compatibilidad y migración" — busca trabajos diferidos a otra spec.
     - Sección 8 "Riesgos y mitigaciones" (columna "Mitigación") — busca mitigaciones que se dejan para "spec futura X".
     - Sección 9 "Notas y enlaces" — busca enlaces a specs no creadas todavía.
   - Para cada idea detectada, prepara una entrada con este formato exacto:
     ```markdown
     - **`<slug-tentativo>`** _(propuesta por spec NNNN el YYYY-MM-DD)_ — `<motivación 1 línea>`. Estado: propuesta.
     ```
   - **Junta todas las ideas detectadas en una sola tanda** y pide confirmación: "Detecté N ideas para futuras specs en esta spec. ¿Las añado a `docs/VISION.md` §12.3? (sí / no / editar lista)". Muestra el bloque literal.
     - Si **sí**: aplica el `Edit` aditivo (añade líneas al final de la lista).
     - Si **no** o **editar**: anótalo en el reporte.
   - **NUNCA inventes ideas que la spec no mencione**. Si la spec no sugiere ninguna futura, salta sin pedir confirmación.

8. **Reporta al usuario**:
   - Ruta del fichero creado.
   - Clasificación de triviality y razón (paso 6).
   - Lista de los `_[VERIFICAR]_` que necesitan revisión humana.
   - **Directrices citadas**: `directives_followed`, `directives_closed`, `directives_opened` con una línea de explicación por cada una.
   - **Registro en VISION**:
     - §12.2: si se añadió entrada, ancla literal (`§12.2 idea NNNN`); si el usuario rechazó el registro, anótalo.
     - §12.3: ideas previas consolidadas (a) y nuevas añadidas (b), o "ninguna detectada / usuario rechazó".
   - Si se ejecutó `/spec-review`: veredicto del subagente y, en caso de `GO-WITH-CHANGES`, recordatorio de revisar los cambios mínimos. En caso de `RETHINK`, **NO** sugieras aprobar la spec.
   - Recordatorio de cambiar `status: Draft` → `status: Approved` cuando esté lista (solo si no hubo `RETHINK`).

## Reglas

- **NO inventes** comportamiento técnico no pedido. Si $ARGUMENTS no especifica algo crítico, marca `_[VERIFICAR]_` en lugar de adivinar.
- **NO implementes** código aquí. Solo se crea la spec.
- **NO invoques al subagente `spec-architect` directamente.** Si la spec es no trivial, encadena `/spec-review`, que es el único punto de entrada autorizado al subagente Opus. Mantiene la traza y el control de coste.
- **NO lances `/spec-review` en specs triviales.** La heurística existe para no quemar Opus. Si dudas, fuerza la clasificación con criterio: "¿este cambio toca contratos entre módulos?". Si la respuesta es no, es trivial.
- Si $ARGUMENTS está vacío, pide al usuario que describa qué quiere especificar.
- **Sin visión no hay spec.** Si `docs/VISION.md` no está rellenada, deriva primero a `/vision` (paso 0). Toda spec debe poder justificarse contra el norte.
- **Edición de VISION**: solo están permitidas las operaciones de los pasos 7.5 (añadir entrada en §12.2) y 7.6 (añadir/consolidar en §12.3) **y solo con confirmación humana explícita**. Cualquier otro cambio en VISION (principios, objetivos, no-objetivos, temas, §12.1 directrices estratégicas) requiere `/vision`.
- **Cita directrices con criterio.** El frontmatter `directives_followed` debe listar las directrices realmente aplicables al ámbito de la spec. Si dudas si una aplica, déjala fuera y anótalo en la subsección.
