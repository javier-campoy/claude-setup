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

2. **Contexto**:
   - Lee `CLAUDE.md`, `docs/VISION.md` y `docs/STATE.md`.
   - Lee specs `related` mencionadas en el frontmatter.
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
   - Actualiza el frontmatter de la spec:
     - `status: Implemented`
     - `implemented_in: "pending"` (se actualizará con el hash real tras el commit)
     - `updated: <fecha de hoy>`
   - Mueve la fila correspondiente en `docs/STATE.md` de "Specs activas" a "Specs implementadas".
   - Añade entrada en `docs/changelog.md` bajo `[No publicado]` referenciando la spec.
   - Por cada módulo Python creado o modificado en `src/`, actualiza (o crea) su `docs/modules/<modulo>.md` correspondiente.
   - Si se tomaron decisiones técnicas relevantes durante la implementación, propón añadir un ADR a `docs/STATE.md` sección 4 (NO lo añadas sin confirmación).

8. **Commit a la rama de feature**:
   - Verifica que NO estás en `main`/`master`:
     `git branch --show-current`
     Si la rama es `main` o `master`, **para** y avisa: "Estás en main. Crea una rama con `git checkout -b feat/<nombre>` antes de continuar."
   - Haz staging de todos los ficheros modificados (código + docs):
     `git add <lista explícita de ficheros modificados>`
   - Crea el commit con mensaje Conventional Commits:
     `feat: implement spec NNNN — <título de la spec>`
   - Obtén el hash del commit recién creado:
     `git rev-parse --short HEAD`
   - Actualiza `implemented_in: <hash>` en el frontmatter de la spec.
   - Crea un segundo commit mínimo para registrar el hash:
     `git add docs/specs/NNNN-*.md && git commit -m "chore: record implemented_in for spec NNNN"`
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
    - Estado del gate de calidad local.
    - Rama y hash del commit de implementación.
    - Próximos pasos: esperar CI verde → mergear PR → `/release` cuando toque.

## Reglas adicionales

- **Sin `_[VERIFICAR]_` no se implementa.** Si la spec conserva marcadores `_[VERIFICAR]_`, son decisiones humanas sin resolver: para y pide que se aclaren. Nunca los rellenes adivinando.
- **No mezcles dos specs en una sesión** salvo que el usuario lo pida explícitamente.
- **No saltes pasos del Plan de implementación** aunque parezcan triviales.
- **Si la spec está mal**, NO la "arregles" silenciosamente: anota el problema en sección 10 y para a discutir.
