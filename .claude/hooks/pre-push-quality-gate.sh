#!/usr/bin/env bash
# pre-push: ruff + mypy + pytest deben pasar antes de subir al remoto.
# Usa --no-verify solo en emergencias justificadas.
echo ""
echo "▶ Gate de calidad pre-push..."
uv run ruff check . || {
    echo "  ruff FALLÓ"
    exit 1
}
uv run mypy src || {
    echo "  mypy FALLÓ"
    exit 1
}
uv run pytest -q
status=$?
# 5 = pytest no ha encontrado tests (proyecto recién desplegado): avisa, no bloquea.
if [ "$status" -eq 5 ]; then
    echo "  pytest: todavía no hay tests (aviso, no bloquea)"
elif [ "$status" -ne 0 ]; then
    echo "  pytest FALLÓ"
    exit 1
fi
echo "✓ Gate superado."
echo ""
