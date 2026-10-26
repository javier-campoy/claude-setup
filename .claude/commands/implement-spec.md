---
description: Implementa una spec aprobada paso a paso, actualizando docs viva al terminar
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(uv run:*), Bash(git diff:*), Bash(git status), Bash(git log:*), Bash(git rev-parse:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(date:*)
argument-hint: "<ruta a docs/specs/NNNN-slug.md>"
---

Implementa la spec indicada en $ARGUMENTS siguiendo el flujo spec-driven.

## Procedimiento

1. **Carga la spec**:
   - Lee el fichero indicado en $ARGUMENTS.
   - Si no se ha indicado ruta, lista las specs en estado `Approved` con `ls docs/specs/` y pide al usuario cuál implementar.
   - **Verifica el frontmatter `status`**:
     - Si es `Draft` → para. Mensaje: "La spec está en Draft. Apruébala primero (cambia status a Approved)."
     - Si es `Implemented` → para. Mensaje: "Esta spec ya está implementada en commit X."
     - Si es `Rejected` → para. Mensaje: "Esta spec fue rechazada."
     - Si es `Approved` → continúa.
   - **Verifica que no queden marcadores `_[VERIFICAR]_` sin resolver**:
     - Con Grep, busca `[VERIFICAR]` en la spec.
     - Si aparece alguno → **para**. Una spec aprobada no debería tener huecos sin aclarar: cada `_[VERIFICAR]_` es una decisión humana pendiente que NO debes adivinar. Mensaje: "La spec tiene N marcadores `_[VERIFICAR]_` sin resolver (líneas X, Y, …). Acláralos en la spec antes de implementar y vuelve a ejecutar /implement-spec." Lista las líneas concretas.
     - Si no hay ninguno → continúa.
   - **Advertencia (no bloqueante) sobre revisión arquitectónica**:
     - Con Grep, busca `## Revisión arquitectónica` en la spec.
     - Si **no aparece**, evalúa rápidamente si la spec es no trivial: introduce módulo nuevo, toca boundaries, cambia API pública, depende de otra spec activa, o toma una decisión de diseño que podría acabar en ADR.
     - Si parece no trivial → **avisa al usuario** (no bloquees): "Esta spec parece no trivial y no consta `## Revisión arquitectónica`. Recomendado pasar `/spec-review docs/specs/NNNN-…md` antes de implementarla. ¿Continúo igualmente?" y espera confirmación explícita.
     - Si el usuario confirma "sí, sigue" → continúa. Si el usuario decide ejecutar `/spec-review` primero → para y devuelve el control. Si te dice que la spec es trivial → continúa sin más.
     - Si la spec sí tiene revisión y el veredicto fue `RETHINK` → **para**. Mensaje: "La spec tiene revisión arquitectónica con veredicto RETHINK. Resuélvelo antes de implementar."

2. **Contexto**:
   - Lee `CLAUDE.md`, `docs/VISION.md` y `docs/STATE.md`.
   - Lee specs `related` mencionadas en el frontmatter.
   - **Identifica las directrices que esta spec dice cumplir/cerrar/abrir**: del frontmatter `directives_followed` / `directives_closed` / `directives_opened`, busca cada `D-NN` en `docs/STATE.md` §5.5 y léelas. **Si una directriz citada no existe**, para y pide al usuario que la aclare (puede ser una errata o un cambio en STATE post-redacción de la spec).
   - **Identifica los bullets del roadmap que esta spec dice cumplir**: relee la subsección "Alineación con la visión" de la spec (los bullets de VISION §4 Fase N citados con texto literal). Los necesitarás en el paso 7e para proponer marcarlos `[x]`.
   - **Identifica la entrada de §12.2**: lee `vision_idea_ref` del frontmatter (si la spec se creó con `/spec` post-convención, apuntará a `§12.2 idea NNNN`). La necesitarás en el paso 7f.
   - Ten presente el norte (`docs/VISION.md`): la implementación debe avanzar los objetivos y respetar los no-objetivos y principios. Si durante la implementación detectas que la spec contradice la visión, anótalo en la sección 10 y para a discutir (no la "corrijas" en silencio).

3. **Plan de ataque**:
   - Resume al usuario tu interpretación de la spec en 5-10 líneas.
   - Pide confirmación explícita antes de empezar a tocar código.

4. **Implementación**:
   - Ejecuta el "Plan de implementación" (sección 5) de la spec, paso a paso.
   - Por cada paso completado, marca el checkbox `[ ]` → `[x]` en la propia spec.
   - **Reglas duras**:
     - Si encuentras algo que **no encaja con la spec**, NO improvises: para, anota en la sección 10 ("Decisiones durante la implementación") la pregunta concreta y espera respuesta.
     - Si la spec especifica una API, respétala. Si crees que debería ser diferente, anota el feedback en sección 10 pero implementa lo que dice la spec.
     - Tests de cada paso ANTES de avanzar al siguiente cuando sea posible (TDD-friendly).

5. **Verifica criterios de aceptación**:
   - Recorre la sección 6 de la spec.
   - Marca `[x]` cada criterio cuando lo verifiques.
   - Si alguno no se cumple, **NO marques la spec como Implemented**.

6. **Gate de calidad**:
   - `uv run ruff check . --fix && uv run ruff format .`
   - `uv run mypy src`
   - `uv run pytest`
   - Si algo falla, arréglalo antes de continuar.

7. **Cierre**:

   **7a. Frontmatter de la spec**:
   - `status: Implemented`
   - `implemented_in: "pending"` (se actualizará con el hash real tras el commit)
   - `updated: <fecha de hoy>`

   **7b. Tablas de specs en STATE**:
   - Mueve la fila correspondiente en `docs/STATE.md` §5 de "Specs activas" a "Specs implementadas".

   **7c. Documentación viva**:
   - Añade entrada en `docs/changelog.md` bajo `[No publicado]` referenciando la spec y citando las directrices cerradas (si las hay).
   - Por cada módulo Python creado o modificado en `src/`, actualiza (o crea) su `docs/modules/<modulo>.md` correspondiente.
   - Si se tomaron decisiones técnicas relevantes durante la implementación, propón añadir un ADR a `docs/STATE.md` sección 4 (NO lo añadas sin confirmación).

   **7c.bis. Captura de ideas para futuras specs en VISION §12.3 (operación aditiva con confirmación humana)**:
   - Localiza la subsección **§12.3 "Ideas para futuras specs (sin spec asociada todavía)"** en `docs/VISION.md`. Si no existe, salta este sub-paso e infórmalo al usuario.
   - Escanea la **sección 10 "Decisiones durante la implementación"** de la spec recién implementada buscando menciones a futuras specs:
     - "esto sugiere spec futura X"
     - "queda pendiente para spec Y"
     - "sería una spec futura"
     - "se difiere a spec posterior"
     - "candidata para próxima spec"
     - Cualquier patrón equivalente que indique trabajo identificado pero **fuera del alcance** de la spec actual.
   - Para cada idea detectada, prepara una entrada con este formato exacto:
     ```markdown
     - **`<slug-tentativo>`** _(fase: §4 Fase N, propuesta por implementación de spec NNNN el YYYY-MM-DD)_ — `<motivación 1 línea>`. Estado: propuesta.
     ```
   - Junta todas las ideas detectadas en una sola tanda y pide confirmación al usuario mostrando el bloque literal: "Durante la implementación detecté N ideas para futuras specs. ¿Las añado a VISION §12.3? (sí / no / editar)".
     - Si **sí**: aplica el `Edit` aditivo a §12.3 (solo añade líneas al final de la lista; no toques las existentes).
     - Si **no** o **editar**: anota la decisión en el reporte del paso 10.
   - **NUNCA inventes ideas que la sección 10 no mencione**. Si está vacía o solo contiene apuntes que no proponen spec futura, salta sin pedir confirmación.

   **7d. Reincorporación de aprendizaje a STATE §5.5 (directrices)**:
   - Para cada `D-NN` en `directives_closed` del frontmatter de la spec:
     - Localiza la fila en `docs/STATE.md` §5.5 "Directrices vigentes para próximas specs".
     - Cambia su estado a `cerrada (NNNN, <hash>)`. El hash será "pending" inicialmente; se actualizará tras el commit (paso 8) al mismo tiempo que `implemented_in`.
     - No borres la fila — queda como histórico.
   - Si el frontmatter tiene `directives_opened` con IDs propuestos, **prepara una propuesta** al usuario para añadirlas a §5.5:
     - Para cada `D-NN` propuesta, redacta una fila completa (Origen, Ámbito, Directriz, Estado=`vigente`).
     - Pide confirmación al usuario mostrando la(s) fila(s) literal(es): "Voy a añadir estas directrices nuevas en STATE §5.5. ¿Procedo? (sí / no / editar)".
     - Si **sí**: aplica el `Edit` aditivo (solo añade filas al final de la tabla; no toques las existentes).
     - Si **no** o **editar**: anota la decisión en el reporte final.
   - Si durante la implementación se descubrió que una directriz **vigente** ya no aplica (queda derogada por la propia spec, p.ej. por sustituir un ADR), **NO la derogues automáticamente**: anótalo y propón al usuario que confirme la derogación con su justificación. Lo mismo si una directriz **vigente** entra en conflicto con la implementación elegida.

   **7e. Cierre de bullets del roadmap en VISION §4 (operación de cierre con confirmación humana)**:
   - Para cada bullet de VISION §4 Fase N citado en la subsección "Alineación con la visión" de la spec:
     - Localiza el bullet exacto en `docs/VISION.md` (búsqueda por texto literal).
     - Verifica que está en estado `[ ]` (no cumplido todavía). Si ya está `[x]`, sáltalo.
     - Si está `[ ]`, prepara una propuesta: "El bullet «`<texto>`» de VISION §4 Fase N parece cumplido por esta spec. ¿Lo marco `[x]`?".
   - Junta todos los bullets candidatos y pide **una sola confirmación al usuario** mostrando la lista literal (no uno por uno).
   - Aplica solo los confirmados (un `Edit` por bullet, cambio `[ ]` → `[x]`, sin tocar el texto ni el contexto). Si el usuario quiere añadir nota al cierre (p.ej. "cumplido por spec 0011 en `<hash>`"), respeta su redacción.
   - **NO toques otras secciones de VISION** ni cambies texto que no sea el checkbox del bullet (y la nota si el usuario la pide).

   **7f. Cierre de la entrada en VISION §12.2 (operación de cierre con confirmación humana)**:
   - Si la spec tiene `vision_idea_ref` apuntando a `§12.2 idea NNNN`:
     - Localiza la entrada en `docs/VISION.md` §12.2.
     - Prepara la transformación: cambiar `_(estado: Draft, ...)_` a `_(estado: Implemented, ...)_` y `_Implementada en: pendiente._` a `_Implementada en: <hash>._` (el hash será "pending" inicialmente y se actualizará tras el commit del paso 8).
     - Pide confirmación al usuario mostrando el diff propuesto: "Voy a marcar la entrada §12.2 idea NNNN como Implemented. ¿Procedo?".
     - Si **sí**: aplica el `Edit` (solo ese campo, no toques el resto de la entrada).
     - Si la spec **no** tiene `vision_idea_ref` (creada antes de la convención de §12.2), salta este sub-paso.

   **7g. Detección de divergencia con VISION (estructural)**:
   - Si durante la implementación se descubrió que la spec contradice un principio, un no-objetivo o una decisión estratégica de VISION:
     - **NO lo apliques** silenciosamente ni edites VISION para "arreglarlo".
     - Anota la divergencia en la sección 10 de la spec ("Decisiones durante la implementación").
     - Informa al usuario y propón ejecutar `/vision` después del commit, dejándole por escrito qué partes de VISION crees que deberían revisarse.

   **7h. Gate de consistencia specs ↔ STATE §5 (pre-commit)**:
   - Ejecuta el check determinista desde la raíz del repo:
     `uv run python .claude/hooks/check_spec_state_sync.py`
   - Si sale con código **0**: la tabla de STATE §5 es consistente con los frontmatters — continúa al paso 8.
   - Si sale con código **1**: hay specs cuyo `status` no coincide con su posición en las tablas de STATE §5. Lee el informe, corrige las filas en STATE §5 (mueve la fila de la spec recién implementada de "Activas" a "Implementadas") y vuelve a ejecutar el check.
   - **NO avances al paso 8** hasta que el check salga con código 0.

8. **Commit a la rama `develop`**:
   - Verifica que estás en `develop` (nunca en `main`/`master`):
     `git branch --show-current`
     Si la rama es `main` o `master`, **para** y avisa: "Estás en main/master. Cámbiate a develop con `git checkout develop` antes de continuar."
   - Haz staging de todos los ficheros modificados (código + docs, **incluyendo `docs/VISION.md` si los pasos 7e/7f aplicaron cambios confirmados**):
     `git add <lista explícita de ficheros modificados>`
   - Crea el commit con mensaje Conventional Commits:
     `feat: implement spec NNNN — <título de la spec>`
   - Obtén el hash del commit recién creado:
     `git rev-parse --short HEAD`
   - **Reemplaza todos los `pending` por el hash real** en una sola pasada (un commit, no varios):
     - `implemented_in: <hash>` en el frontmatter de la spec.
     - En STATE §5.5: cada `cerrada (NNNN, pending)` añadido en el paso 7d → `cerrada (NNNN, <hash>)`.
     - En VISION §12.2 (si se editó en 7f): `_Implementada en: pendiente._` → `_Implementada en: <hash>._`.
     - En STATE §5 "Specs implementadas": añade el hash en la columna correspondiente.
   - Crea un segundo commit mínimo para registrar el hash:
     `git add docs/specs/NNNN-*.md docs/STATE.md docs/VISION.md && git commit -m "chore: record implemented_in for spec NNNN"`
     (Incluye `docs/VISION.md` en el `git add` solo si tuvo edits confirmados en 7e/7f.)
   - Push a develop:
     `git push origin develop`

9. **Cierra el ciclo**:
   - Informa: "El código está commiteado y pusheado en `develop`."
   - Recuerda: **CI debe pasar** (pipeline de `.gitlab-ci.yml` en verde) en ese push a `develop`.
   - Cuando la unidad de release esté completa, se integra `develop` en `main` y se usa `/release X.Y.Z` para publicar.
   - **NO integres en `main` ni publiques automáticamente**: lo decide el usuario.
   - _Alternativa (si en el futuro se vuelve al flujo de merge requests): push a una rama `feat/...` y `glab mr create --target-branch develop`._

10. **Reporta**:
    - Resumen de lo implementado.
    - Ficheros creados/modificados.
    - Criterios de aceptación: cuáles se cumplen, cuáles no.
    - **Directrices STATE §5.5**:
      - Cerradas en esta implementación (`directives_closed` aplicados).
      - Nuevas añadidas tras confirmación humana (de `directives_opened`).
      - Si alguna propuesta de cierre o apertura fue rechazada por el usuario, anótalo.
    - **VISION editada**:
      - Bullets §4 marcados `[x]` (lista literal).
      - Entrada §12.2 actualizada a `Implemented` (sí/no).
      - Ideas añadidas a §12.3 (lista literal de las propuestas confirmadas, o "ninguna detectada / usuario rechazó").
      - Si se detectó divergencia estratégica (paso 7g), recordatorio de ejecutar `/vision` con el resumen redactado.
    - Estado del gate de calidad local.
    - Rama (`develop`) y hash del commit de implementación.
    - Próximos pasos: CI verde en `develop` → integrar en `main` → `/release` cuando toque.

## Reglas adicionales

- **Sin `_[VERIFICAR]_` no se implementa.** Si la spec conserva marcadores `_[VERIFICAR]_`, son decisiones humanas sin resolver: para y pide que se aclaren. Nunca los rellenes adivinando.
- **No mezcles dos specs en una sesión** salvo que el usuario lo pida explícitamente.
- **No saltes pasos del Plan de implementación** aunque parezcan triviales.
- **Si la spec está mal**, NO la "arregles" silenciosamente: anota el problema en sección 10 y para a discutir.
- **Edición de VISION**: solo están permitidas las operaciones **aditivas** (no aplican aquí) y de **cierre** (marcar `[x]` un bullet de §4 cumplido por la spec; marcar §12.2 entrada como `Implemented`). Cualquier cambio estructural (principios, fases, no-objetivos, stack, ADRs estratégicos) requiere `/vision`. Las operaciones de cierre **siempre requieren confirmación humana explícita** antes de aplicar — Claude propone, humano confirma.
- **Cierre de directrices**: solo cierras directrices `vigente` → `cerrada` listadas en `directives_closed` de la spec. NUNCA cierres una directriz que no esté declarada. Si crees que una directriz vigente queda derogada por la implementación, anótalo y pide confirmación.
