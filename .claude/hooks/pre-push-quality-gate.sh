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
uv run pytest -q || {
    echo "  pytest FALLÓ"
    exit 1
}
echo "✓ Gate superado."
echo ""
