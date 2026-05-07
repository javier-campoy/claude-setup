---
description: Crea un commit siguiendo Conventional Commits a partir del diff actual
allowed-tools: Bash(git status), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*)
argument-hint: "[mensaje opcional o tipo: feat/fix/docs/...]"
---

Pasos:

1. Ejecuta `git status` y `git diff --staged` (si hay nada en stage, también `git diff`).
2. Si no hay cambios, avisa al usuario y termina.
3. Antes de commitear, ejecuta el gate de calidad mínimo: `uv run ruff check . && uv run pytest -q`. Si algo falla, **NO** commitees: reporta los fallos y para.
4. Analiza el diff y propón un mensaje de commit siguiendo Conventional Commits:
   - `feat:` nueva funcionalidad
   - `fix:` corrección de bug
   - `docs:` cambios en documentación
   - `refactor:` refactor sin cambio de comportamiento
   - `test:` añadir o cambiar tests
   - `chore:` tareas de mantenimiento, deps, config
   - `perf:` mejora de rendimiento
5. El mensaje debe tener: `<tipo>(<scope opcional>): <resumen imperativo en una línea ≤72 chars>`. Si los cambios son no triviales, añade un cuerpo explicando el *por qué*.
6. Si el usuario pasó $ARGUMENTS úsalo como guía o tipo.
7. Muestra el mensaje propuesto y pide confirmación antes de ejecutar `git add` y `git commit`.

NO hagas push. Eso lo hace el usuario manualmente.
