---
description: Refactoriza un fichero respetando las convenciones del proyecto
allowed-tools: Read, Edit, Bash(uv run:*), Bash(git diff:*)
argument-hint: "<ruta/al/fichero.py> [objetivo del refactor]"
---

Refactoriza el fichero indicado en $ARGUMENTS.

Pasos:
1. Lee primero CLAUDE.md para refrescar las convenciones del proyecto.
2. Lee el fichero objetivo y comprende su responsabilidad.
3. Lee los tests asociados (`tests/test_<modulo>.py`). **Si no hay tests, AVISA y propón crearlos antes de refactorizar.**
4. Identifica oportunidades:
   - Funciones demasiado largas → extraer.
   - Duplicación → DRY.
   - Nombres poco claros.
   - Falta de type hints.
   - Lógica acoplada que debería separarse.
   - Código muerto.
5. Propón un plan de refactor antes de tocar nada. Espera aprobación si los cambios son no triviales.
6. Aplica los cambios manteniendo el comportamiento idéntico.
7. Ejecuta `uv run pytest` y `uv run mypy src` para verificar que no rompiste nada.
8. Muestra el `git diff --stat` final.

**Reglas duras:**
- No cambies APIs públicas sin avisar.
- No mezcles refactor con cambios de comportamiento.
- Si los tests fallan, revierte y reporta.
