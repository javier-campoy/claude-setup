---
description: Crea un commit siguiendo Conventional Commits a partir del diff actual
allowed-tools: Read, Edit, Write, Glob, Grep, Skill, Task, Bash(git status), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(python:*), Bash(uv run:*)
argument-hint: "[mensaje opcional o tipo: feat/fix/docs/...]"
---

Pasos:

1. Ejecuta `git status` y `git diff --staged` (si no hay nada en stage, también `git diff`).
2. Si no hay cambios, avisa al usuario y termina.
3. **Gate de calidad de código**: ejecuta `uv run ruff check . && uv run pytest -q`. Si algo falla, **NO** commitees: reporta los fallos y para.
4. **Auditoría de documentación** (Capa 1, determinista + Capa 2, remediación):
   1. Ejecuta el gate de cobertura sobre los módulos que vas a commitear:
      - Si ya hay `src/*.py` en stage: `uv run python .claude/hooks/check_doc_coverage.py --staged`.
      - Si vas a commitear cambios de `src/` aún sin stagear: pásale esas rutas como argumentos, p. ej. `uv run python .claude/hooks/check_doc_coverage.py src/pkg/foo.py`.
   2. Si sale con **código 0**, la documentación está cubierta: pasa al paso 5.
   3. Si sale con **código ≠ 0**, **auto-remedia** los huecos que reporta (no commitees con huecos). El gate los agrupa por tipo; remedia cada tipo con su comando:
      - **Docstrings faltantes** y **`docs/modules/<modulo>.md` faltantes**: invoca la skill `/docs <fichero>` sobre cada módulo afectado (genera docstrings estilo Google en el idioma del codebase y sincroniza su `docs/modules/<modulo>.md`).
      - **`docs/STATE.md` desactualizado** (un módulo con API pública no está referenciado en STATE.md): invoca `/state` para regenerar la sección de arquitectura/módulos y las tablas de specs. NO inventes ADRs ni specs: si detectas código no trivial sin spec, márcalo para decisión humana.
      - **Sección `[No publicado]` del changelog vacía**: invoca `/changelog` (o añade tú la entrada que describa el cambio).
   4. **Re-ejecuta el gate** del paso 4.1. Repite la remediación hasta que salga con código 0 (máximo ~3 iteraciones). Si sigue fallando por algo que requiere criterio humano, **para y repórtalo** sin commitear.
   5. Muestra al usuario un resumen breve de la documentación que generaste o actualizaste.
5. Analiza el diff y propón un mensaje de commit siguiendo Conventional Commits:
   - `feat:` nueva funcionalidad
   - `fix:` corrección de bug
   - `docs:` cambios en documentación
   - `refactor:` refactor sin cambio de comportamiento
   - `test:` añadir o cambiar tests
   - `chore:` tareas de mantenimiento, deps, config
   - `perf:` mejora de rendimiento
6. El mensaje debe tener: `<tipo>(<scope opcional>): <resumen imperativo en una línea ≤72 chars>`. Si los cambios son no triviales, añade un cuerpo explicando el *por qué*.
7. Si el usuario pasó $ARGUMENTS úsalo como guía o tipo.
8. Muestra el mensaje propuesto y pide confirmación. Tras el OK, haz `git add` de los cambios **y de la documentación generada en el paso 4**, y luego `git commit`.

NO hagas push. Eso lo hace el usuario manualmente.
