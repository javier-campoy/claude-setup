---
description: Audita el codebase contra docs/STATE.md y propone refactors (no aplica nada sin confirmación)
allowed-tools: Read, Grep, Glob, Bash(uv run:*), Bash(git log:*), Bash(git diff:*), Bash(rg:*), Bash(find:*), Bash(wc:*)
argument-hint: "[ámbito opcional, p.ej. 'src/parser/' o 'todo']"
---

Lanza una auditoría arquitectónica del codebase usando el subagente `refactorer`.

## Procedimiento

1. **Determina el alcance**:
   - Si $ARGUMENTS es una ruta concreta (p.ej. `src/parser/`), audita solo eso.
   - Si es "todo" o está vacío, audita todo `src/`.

2. **Invoca al subagente `refactorer`** con la instrucción:
   > Audita el código bajo $ARGUMENTS (o todo `src/` si no se especificó). Compara contra `docs/STATE.md` y los ADRs. Genera un informe priorizado con: drift arquitectónico, violaciones de ADRs, deuda estructural, inconsistencias, código muerto, tests desalineados. **No apliques refactors todavía**: solo el informe.

3. **Cuando recibas el informe del subagente**:
   - Muéstraselo al usuario tal cual.
   - Si hay refactors clasificados como "Pequeños y seguros", pregunta al usuario si quiere aplicarlos en esta sesión.
   - Si los aprueba, vuelve a invocar al subagente con la lista concreta de refactors a aplicar.
   - Si hay refactors medianos/grandes, sugiere crear specs con `/spec`.

## Reglas

- NO apliques refactors sin pasar por el subagente y sin confirmación humana.
- Si la auditoría detecta algo crítico (violación de ADR, secret en código, bug evidente), destácalo arriba del informe.
- Si el informe es muy largo (>20 hallazgos), resume y agrupa por módulo.
