#!/usr/bin/env bash
# ============================================================================
# install.sh — Despliega el kit de Claude Code a un proyecto Python
# ============================================================================
# Uso:
#   ./install.sh <ruta_destino> <nombre_paquete> [nombre_proyecto]
# Ejemplos:
#   ./install.sh ~/proyectos/mi-app mi_app
#   ./install.sh ~/proyectos/foo-tools foo_tools foo-tools
# ============================================================================

set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Uso: $0 <ruta_destino> <nombre_paquete> [nombre_proyecto]"
    echo "  nombre_paquete:  con underscores, ej. mi_app"
    echo "  nombre_proyecto: con guiones (PyPI), ej. mi-app (default: deriva del paquete)"
    exit 1
fi

TARGET_DIR="$1"
PACKAGE_NAME="$2"
PROJECT_NAME="${3:-${PACKAGE_NAME//_/-}}"
KIT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=============================================="
echo " Despliegue del kit Claude Code para Python"
echo "=============================================="
echo "Origen (kit): $KIT_DIR"
echo "Destino:      $TARGET_DIR"
echo "Paquete:      $PACKAGE_NAME (Python con underscores)"
echo "Proyecto:     $PROJECT_NAME (PyPI con guiones)"
echo ""

mkdir -p "$TARGET_DIR"

# Items útiles a copiar
INCLUDE=(
    "CLAUDE.md"
    "README.md"
    "GUIA_CLAUDE_CODE.md"
    "pyproject.toml"
    ".gitignore"
    ".python-version"
    ".pre-commit-config.yaml"
    ".mcp.json"
    ".claude"
    "docs"
)

# Items obsoletos a excluir
EXCLUDE=(
    "mkdocs.yml"
    "scripts"
    "docs/getting-started.md"
    "docs/installation.md"
    "docs/contributing.md"
    "docs/guides"
    ".claude/commands/docs-build.md"
    ".claude/commands/docs-serve.md"
    ".claude/commands/docs-update.md"
)

echo "Copiando ficheros..."
for item in "${INCLUDE[@]}"; do
    src="$KIT_DIR/$item"
    dst="$TARGET_DIR/$item"
    if [ ! -e "$src" ]; then
        echo "  · $item (no existe en kit, salto)"
        continue
    fi
    if [ -d "$src" ]; then
        mkdir -p "$dst"
        cp -r "$src/." "$dst/"
    else
        cp "$src" "$dst"
    fi
    echo "  · $item"
done

echo ""
echo "Eliminando ficheros obsoletos..."
for item in "${EXCLUDE[@]}"; do
    if [ -e "$TARGET_DIR/$item" ]; then
        rm -rf "$TARGET_DIR/$item"
        echo "  · borrado: $item"
    fi
done

echo ""
echo "Creando estructura del paquete..."
mkdir -p "$TARGET_DIR/src/$PACKAGE_NAME" "$TARGET_DIR/tests"
cat > "$TARGET_DIR/src/$PACKAGE_NAME/__init__.py" <<EOF
"""$PACKAGE_NAME paquete."""

__version__ = "0.1.0"
EOF
: > "$TARGET_DIR/tests/__init__.py"
echo "  · src/$PACKAGE_NAME/__init__.py"
echo "  · tests/__init__.py"

echo ""
echo "Personalizando nombres..."
FILES_CUSTOMIZE=(
    "pyproject.toml"
    "CLAUDE.md"
    "README.md"
    "docs/index.md"
    "docs/STATE.md"
    "docs/specs/README.md"
    "docs/specs/_template.md"
    "docs/specs/0001-ejemplo.md"
)
for f in "${FILES_CUSTOMIZE[@]}"; do
    path="$TARGET_DIR/$f"
    if [ -f "$path" ]; then
        # sed -i compatible con macOS y Linux
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/mi_paquete/$PACKAGE_NAME/g; s/mi-paquete/$PROJECT_NAME/g" "$path"
        else
            sed -i "s/mi_paquete/$PACKAGE_NAME/g; s/mi-paquete/$PROJECT_NAME/g" "$path"
        fi
        echo "  · $f"
    fi
done

echo ""
echo "Inicializando git..."
cd "$TARGET_DIR"
if [ ! -d ".git" ]; then
    git init -q
    echo "  · git init OK"
else
    echo "  · ya existe .git, salto"
fi

echo ""
echo "Instalando dependencias con uv..."
if uv sync --all-extras --dev; then
    echo "  · uv sync OK"
else
    echo "  · uv sync falló. Ejecuta manualmente: uv sync --all-extras --dev"
fi

echo ""
echo "Instalando hooks de pre-commit..."
if uv run pre-commit install; then
    echo "  · pre-commit install OK"
else
    echo "  · pre-commit install falló. Ejecuta manualmente: uv run pre-commit install"
fi

echo ""
echo "=============================================="
echo " ✅ Instalación completa"
echo "=============================================="
echo ""
echo "Siguientes pasos:"
echo "  1. cd $TARGET_DIR"
echo "  2. claude                    # Lanza Claude Code"
echo "  3. /spec \"primera feature\"   # Crea tu primera spec"
echo ""
echo "Lee docs/index.md y GUIA_CLAUDE_CODE.md para conocer el flujo."
