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
   - **Identifica las directrices que esta spec dice cumplir/cerrar/abrir**: del frontmatter `directives_followed` / `directives_closed` / `directives_opened`, busca cada ID en `docs/STATE.md` §5.5 (D-NN tácticas) y/o `docs/VISION.md` §12.1 (DV-NN estratégicas), y léelas. **Si una directriz citada no existe**, para y pide al usuario que la aclare.
   - **Identifica los objetivos del roadmap que esta spec dice cerrar**: relee la subsección "Alineación con la visión" de la spec (los objetivos de VISION §4 citados como "que esta spec cierra"). Los necesitarás en el paso 7e para proponer marcarlos `[x]`.
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
   - Localiza la subsección **§12.3 "Ideas para futuras specs"** en `docs/VISION.md`. Si no existe, salta este sub-paso.
   - Escanea la **sección 10 "Decisiones durante la implementación"** de la spec recién implementada buscando menciones a futuras specs ("esto sugiere spec futura X", "queda pendiente para spec Y", "se difiere a spec posterior", "candidata para próxima spec", o patrones equivalentes).
   - Para cada idea detectada, prepara una entrada con este formato:
     ```markdown
     - **`<slug-tentativo>`** _(propuesta por implementación de spec NNNN el YYYY-MM-DD)_ — `<motivación 1 línea>`. Estado: propuesta.
     ```
   - Junta todas las ideas en una sola tanda y pide confirmación al usuario mostrando el bloque literal.
     - Si **sí**: aplica el `Edit` aditivo.
     - Si **no** o **editar**: anota la decisión en el reporte del paso 10.
   - **NUNCA inventes ideas que la sección 10 no mencione**. Si está vacía, salta sin pedir confirmación.

   **7d. Reincorporación de aprendizaje a STATE §5.5 (directrices)**:
   - Para cada `D-NN` en `directives_closed` del frontmatter de la spec:
     - Localiza la fila en `docs/STATE.md` §5.5.
     - Cambia su estado a `cerrada (NNNN, <hash>)`. El hash será "pending" inicialmente; se actualizará tras el commit (paso 8).
     - No borres la fila — queda como histórico.
   - Si el frontmatter tiene `directives_opened` con IDs propuestos, **prepara una propuesta** al usuario para añadirlas a §5.5:
     - Para cada `D-NN` propuesta, redacta una fila completa (Origen, Ámbito, Directriz, Estado=`vigente`).
     - Pide confirmación al usuario mostrando la(s) fila(s) literal(es).
     - Si **sí**: aplica el `Edit` aditivo.
   - Si durante la implementación se descubrió que una directriz **vigente** ya no aplica (queda derogada), **NO la derogues automáticamente**: anótalo y propón al usuario que confirme.

   **7e. Cierre de objetivos en VISION §4 (operación de cierre con confirmación humana)**:
   - Para cada objetivo de VISION §4 citado en la subsección "Alineación con la visión" de la spec como "que esta spec cierra":
     - Localiza el objetivo exacto en `docs/VISION.md` §4 (búsqueda por ID `O-N` y texto literal).
     - Verifica que está en estado `[ ]` (no cerrado todavía). Si ya está `[x]`, sáltalo.
     - Si está `[ ]`, prepara una propuesta: "El objetivo «`<ID y texto>`» de VISION §4 parece cumplido por esta spec. ¿Lo marco `[x]`?".
   - Junta todos los objetivos candidatos y pide **una sola confirmación al usuario** mostrando la lista literal.
   - Aplica solo los confirmados (un `Edit` por objetivo, cambio `[ ]` → `[x]`, sin tocar el texto). Si el usuario quiere añadir nota al cierre (p.ej. "cerrado por spec NNNN en `<hash>`"), respeta su redacción.
   - **NO toques otras secciones de VISION** ni cambies texto que no sea el checkbox del objetivo.
   - **Importante**: solo marca `[x]` objetivos que la spec **cierra completamente**, no los que solo avanza. Si dudas, no marques.

   **7f. Cierre de la entrada en VISION §12.2 (operación de cierre con confirmación humana)**:
   - Si la spec tiene `vision_idea_ref` apuntando a `§12.2 idea NNNN`:
     - Localiza la entrada en `docs/VISION.md` §12.2.
     - Prepara la transformación: cambiar `_(estado: Draft, ...)_` a `_(estado: Implemented, ...)_` y `_Implementada en: pendiente._` a `_Implementada en: <hash>._`.
     - Pide confirmación al usuario mostrando el diff.
     - Si **sí**: aplica el `Edit`.
     - Si la spec **no** tiene `vision_idea_ref`, salta este sub-paso.

   **7g. Detección de divergencia con VISION (estructural)**:
   - Si durante la implementación se descubrió que la spec contradice un principio, un no-objetivo o una decisión estratégica de VISION:
     - **NO lo apliques** silenciosamente ni edites VISION para "arreglarlo".
     - Anota la divergencia en la sección 10 de la spec.
     - Informa al usuario y propón ejecutar `/vision` después del commit.

8. **Commit a la rama de feature**:
   - Verifica que NO estás en `main`/`master`:
     `git branch --show-current`
     Si la rama es `main` o `master`, **para** y avisa: "Estás en main. Crea una rama con `git checkout -b feat/<nombre>` antes de continuar."
   - Haz staging de todos los ficheros modificados (código + docs, **incluyendo `docs/VISION.md` si los pasos 7c.bis/7e/7f aplicaron cambios confirmados**):
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
     (Incluye `docs/VISION.md` solo si tuvo edits confirmados en 7e/7f.)
   - Push a la rama de feature:
     `git push origin <rama-actual>`

9. **Propón el PR** al usuario:
   - Informa: "El código está en `<rama-actual>`. Crea un PR para mergearlo a main."
   - Si `gh` está disponible, sugiere el comando concreto:
     ```
     gh pr create \
       --title "feat: spec NNNN — <título>" \
       --body "Implementa spec NNNN.\n\nCambios:\n- <lista de ficheros clave>\n\n## Criterios de aceptación\n<lista marcada>"
     ```
   - Recuerda: **CI debe pasar** (`ci.yml` en verde) antes de mergear a main.
   - Cuando todos los PRs relacionados estén mergeados, usa `/release X.Y.Z` para publicar.
   - **NO hagas merge ni cierres el PR automáticamente**.

10. **Reporta**:
    - Resumen de lo implementado.
    - Ficheros creados/modificados.
    - Criterios de aceptación: cuáles se cumplen, cuáles no.
    - **Directrices STATE §5.5**:
      - Cerradas en esta implementación (`directives_closed` aplicados).
      - Nuevas añadidas tras confirmación humana (de `directives_opened`).
      - Si alguna propuesta fue rechazada por el usuario, anótalo.
    - **VISION editada**:
      - Objetivos §4 marcados `[x]` (lista literal).
      - Entrada §12.2 actualizada a `Implemented` (sí/no).
      - Ideas añadidas a §12.3 (lista literal, o "ninguna detectada / usuario rechazó").
      - Si se detectó divergencia estratégica (paso 7g), recordatorio de ejecutar `/vision`.
    - Estado del gate de calidad local.
    - Rama y hash del commit de implementación.
    - Próximos pasos: esperar CI verde → mergear PR → `/release` cuando toque.

## Reglas adicionales

- **Sin `_[VERIFICAR]_` no se implementa.** Si la spec conserva marcadores `_[VERIFICAR]_`, son decisiones humanas sin resolver: para y pide que se aclaren. Nunca los rellenes adivinando.
- **No mezcles dos specs en una sesión** salvo que el usuario lo pida explícitamente.
- **No saltes pasos del Plan de implementación** aunque parezcan triviales.
- **Si la spec está mal**, NO la "arregles" silenciosamente: anota el problema en sección 10 y para a discutir.
- **Edición de VISION**: solo están permitidas las operaciones **aditivas** (7c.bis añadir ideas a §12.3) y de **cierre** (7e marcar `[x]` objetivos §4 que la spec cierra completamente; 7f cerrar entrada §12.2). Cualquier cambio estructural (principios, objetivos nuevos, no-objetivos, temas, §12.1 directrices estratégicas) requiere `/vision`. Todas las operaciones de cierre **siempre requieren confirmación humana explícita** antes de aplicar.
- **Cierre de directrices**: solo cierras directrices `vigente` → `cerrada` listadas en `directives_closed` de la spec. NUNCA cierres una directriz que no esté declarada.
