#!/usr/bin/env bash
# PostToolUse: auto-format Python y marcado de flags para doc-sync.
# Recibe el resultado del tool como JSON en stdin.
set -euo pipefail

INPUT=$(cat)

FILE=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', '') or '')
except Exception:
    print('')
" 2>/dev/null) || FILE=""

[ -z "$FILE" ] && exit 0

# Auto-format: ruff format + ruff check --fix
if [[ "$FILE" == *.py ]]; then
    uv run ruff format "$FILE" 2>/dev/null || true
    uv run ruff check --fix --quiet "$FILE" 2>/dev/null || true
fi

# Flag: cambios en src/ pendientes de sync de docs
if [[ "$FILE" == */src/*.py ]]; then
    mkdir -p .claude/.cache
    touch .claude/.cache/src-changed.flag
fi

# Flag: docs tocadas (STATE, changelog, specs)
if [[ "$FILE" == */docs/STATE.md ]] \
   || [[ "$FILE" == */docs/changelog.md ]] \
   || [[ "$FILE" =~ /docs/specs/[^/]+\.md$ ]]; then
    mkdir -p .claude/.cache
    touch .claude/.cache/docs-touched.flag
fi

exit 0
