#!/usr/bin/env bash
# pre-commit: bloquea si hay cambios en src/ sin actualizar docs/ (heurística de presencia).
STAGED=$(git diff --cached --name-only)
SRC=$(echo "$STAGED" | grep -E "^src/.*\.py$" | head -1)
DOCS=$(echo "$STAGED" | grep -E "^docs/(STATE|changelog|specs/.*)\.md$" | head -1)
if [ -n "$SRC" ] && [ -z "$DOCS" ]; then
    echo ""
    echo "ERROR: hay cambios en src/ sin actualizar docs/."
    echo "  Ejecuta /state y /changelog antes de commitear."
    echo ""
    exit 1
fi
