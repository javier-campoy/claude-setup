---
description: Orquesta un loop autónomo implementer↔crítico sobre una spec aprobada hasta cumplir sus criterios (v1: una spec)
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash(uv run:*), Bash(git checkout:*), Bash(git switch:*), Bash(git branch:*), Bash(git add:*), Bash(git commit:*), Bash(git status), Bash(git diff:*), Bash(git rev-parse:*), Bash(git log:*), Bash(ls:*), Bash(date:*)
argument-hint: "<ruta a docs/specs/NNNN-slug.md | ruta a docs/plans/NNNN-slug.md>"
---

Eres el **orquestador** de una campaña: el loop autónomo y acotado que alterna el subagente `spec-implementer` (implementa) y el subagente `spec-critic` (critica) sobre una spec aprobada, hasta cumplir sus criterios o tener que escalar. Tú eres el único que orquesta subagentes, decide y escribe el plan; los subagentes no se llaman entre sí.

**Lee primero** `docs/plans/README.md` para el modelo conceptual y `CLAUDE.md` para las convenciones.

## Procedimiento

### 0. Gate de visión

- Lee `docs/VISION.md`. Si no existe o sigue siendo la plantilla → **para**: "Define el norte con `/vision` antes de lanzar una campaña."
- La campaña debe perseguir un objetivo/tema de la visión; lo registrarás en `vision_refs` del plan.

### 1. Resolver el plan de campaña

- Si `$ARGUMENTS` apunta a un **plan** existente (`docs/plans/NNNN-*.md`) → cárgalo (estás reanudando).
- Si apunta a una **spec** → crea el plan:
  - Lee la spec. **Verifica `status: Approved`** (si no, para con el mismo mensaje que `/implement-spec`).
  - Determina el siguiente `NNNN` mirando `ls docs/plans/`.
  - Crea `docs/plans/NNNN-slug.md` desde `docs/plans/_template.md`. Rellena: `vision_refs` (de los de la spec), `specs: ["NNNN"]`, fecha, caps por defecto (3 rondas, 1 spec).
  - **Sección 1 (Directriz)** y **sección 2 (Criterios de "hecho")**: derívalos del objetivo de visión que persigue la spec y de sus criterios de aceptación. Tradúcelos a items **comprobables**. Marca `_[VERIFICAR]_` lo que no puedas inferir.

### 2. Checkpoint inicial (humano)

Antes de cualquier ejecución autónoma, **presenta y pide confirmación**:

- Resumen de la directriz y los **criterios de "hecho"**.
- La **rama** de trabajo: `feature/campaign-<slug>`.
- Los **caps**: rondas por spec y specs (v1 = 1).
- Aviso: a partir de aquí el loop corre solo y **solo se parará al escalar, al tocar ADR/visión, o al terminar**.

Con tu OK:
- Asegúrate de estar en la rama: `git switch -c feature/campaign-<slug>` (o `git switch` si ya existe). **Nunca** trabajes en `main`/`master`.
- Escribe `status: Active` y la `branch` en el frontmatter del plan.

### 3. Loop sobre la spec (v1: una spec)

Repite `ronda r = 1 .. caps.rounds_per_spec`:

1. **Implementer**: lanza el subagente `spec-implementer` (Task) pasándole: ruta de la spec, ruta del plan, número de ronda y, si r > 1, el feedback del crítico de la ronda anterior (de la sección 4 del plan).
2. **Registra la ronda** en la sección 4 del plan (append): ronda, qué hizo, VERIFICAR auto-resueltos, estado del gate. Anota cada VERIFICAR auto-resuelto también en la sección 6.
3. **¿Escalación del implementer?** Si reportó `_[VERIFICAR:humano]_` o un bloqueo que requiere decisión humana → ve al paso **4. Escalar**.
4. **Crítico**: lanza el subagente `spec-critic` (Task) pasándole: ruta de la spec, ruta del plan, número de ronda y el reporte del implementer. Registra su veredicto en la sección 4.
5. **Decide según el veredicto**:
   - **APROBAR** → sal del loop e ir a **Cierre**.
   - **REVISAR** → si `r < cap`, siguiente ronda (el feedback ya está en el log). Si `r == cap` → **Escalar** ("cap de rondas alcanzado sin converger").
   - **ESCALAR** → **Escalar**.

### 4. Escalar (checkpoint humano)

- Escribe en la **sección 5 (cola de escalación)** del plan la(s) pregunta(s) concretas.
- Pon `status: Paused`.
- **Para** y pregúntale al usuario, en claro, qué hay que decidir. No adivines. Cuando responda y actualice la spec, se relanza `/campaign` con la ruta del plan.

### 5. Cierre (tras APROBAR)

- **Verifica los criterios de "hecho"** (sección 2): que todos estén ✅. Si alguno no → vuelve a Escalar.
- Aplica el cierre estándar de una spec (como `/implement-spec` paso 7): `status: Implemented`, mover en `STATE.md` de activas a implementadas, entrada en `changelog.md`, y `docs/modules/<modulo>.md` por cada módulo tocado.
- **Commit en la rama** (no en main): `git add <ficheros>` + `git commit -m "feat: campaign NNNN — <título> (spec MMMM)"`. Registra el hash en el plan.
- Pon `status: Done` en el plan; marca los criterios de "hecho".

### 6. Reporte final

- Resultado contra los **criterios de "hecho"**: cumplidos / pendientes.
- Resumen de rondas y veredictos.
- **VERIFICAR auto-resueltos** (remite a la sección 6 del plan para que el humano los audite en el PR).
- Escalaciones pendientes, si las hay.
- Rama y hash. Sugiere abrir el PR. **NUNCA hagas merge ni push automático**; CI debe estar en verde antes de mergear.

## Guardarraíles (no negociables)

- **Caps**: nunca superes `rounds_per_spec`. v1 procesa **una** spec por campaña.
- **El gate es la verdad de terreno**: el crítico no puede `APROBAR` con `ruff`/`mypy`/`pytest` en rojo.
- **Rama por campaña**; nunca commits en `main`/`master`; nunca push ni merge sin el humano.
- **Checkpoints humanos**: arranque (paso 2), escalaciones (paso 4) y reporte final (paso 6). Entre medias, autónomo.
- **El plan lo escribes solo tú** (orquestador). El implementer toca `src/` y la spec; el crítico es read-only.
- **No conviertas un `ESCALAR` en una decisión propia.** Si el crítico o el implementer piden humano, para.

## Notas

- **Modelos**: `spec-implementer` corre en `sonnet` y `spec-critic` en `opus` (rúbricas distintas → menos rubber-stamp). Respeta los `model` de cada subagente.
- **v2 (futuro)**: secuencia multi-spec replanificable anclada al "hecho" de un objetivo de visión completo. No implementado aún.
