---
description: Ejecuta ruff y mypy y arregla lo que sea posible
allowed-tools: Bash(uv run:*), Read, Edit
---

Ejecuta el flujo completo de calidad de código:

1. `uv run ruff format .` — Formatea todo.
2. `uv run ruff check . --fix` — Lint + auto-fix.
3. `uv run mypy src` — Type checking en modo estricto.

Reporta:
- Cuántos ficheros se reformatearon.
- Cuántos issues de lint quedan sin resolver (los que ruff no ha podido auto-fix). Lístalos.
- Errores de mypy: lístalos con fichero:línea y el mensaje.

Si quedan errores de ruff o mypy que requieran cambios manuales, propón los cambios mínimos necesarios pero no los apliques sin confirmación si afectan a la lógica del código.
