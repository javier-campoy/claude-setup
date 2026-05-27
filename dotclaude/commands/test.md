---
description: Ejecuta la suite de tests con cobertura
allowed-tools: Bash(uv run:*), Read
argument-hint: "[fichero o patrón opcional]"
---

Ejecuta los tests del proyecto.

- Si el usuario pasó un argumento ($ARGUMENTS), ejecútalos así: `uv run pytest $ARGUMENTS -v`.
- Si no hay argumentos, ejecuta la suite completa con cobertura: `uv run pytest --cov=src --cov-report=term-missing`.

Después:
1. Resume el resultado: nº de tests pasados, fallados, skipped.
2. Si hay fallos, lista los tests que fallan con la primera línea relevante del traceback.
3. Si la cobertura baja del 85% en algún módulo, indícalo.
4. No intentes "arreglar" los tests automáticamente, solo reporta. El usuario decidirá.
