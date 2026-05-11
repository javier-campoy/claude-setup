#!/usr/bin/env bash
# Stop: bloquea si hay cambios en src/ sin actualizar docs/.
# exit 2 hace que Claude continúe la sesión en lugar de cerrarla.
if [ -f .claude/.cache/src-changed.flag ] && [ ! -f .claude/.cache/docs-touched.flag ]; then
    echo ""
    echo "⚠️  Hay cambios en src/ sin actualizar docs/."
    echo "   Ejecuta /state y /changelog antes de terminar."
    echo ""
    rm -f .claude/.cache/src-changed.flag
    exit 2
fi
rm -f .claude/.cache/src-changed.flag .claude/.cache/docs-touched.flag 2>/dev/null || true
exit 0
