#!/usr/bin/env bash
# ============================================================================
# install.sh — Despliega el kit de Claude Code a un proyecto Python
# ============================================================================
# Uso:
#   ./install.sh <ruta_destino> <nombre_paquete> [nombre_proyecto] [opciones]
#
# Posicionales:
#   ruta_destino     Directorio donde desplegar el kit (se crea si no existe).
#   nombre_paquete   Nombre Python del paquete, con underscores. Ej: mi_app
#   nombre_proyecto  Nombre PyPI del proyecto, con guiones. Default: deriva del paquete.
#
# Opciones (si no se pasan, se preguntan interactivamente):
#   --author-name "<nombre>"     Nombre del autor para pyproject.toml
#   --author-email "<email>"     Email del autor para pyproject.toml
#   --github-user "<usuario>"    Owner de GitHub para los URLs Homepage/Issues
#   --no-prompt                  No preguntar; usar defaults para los flags faltantes.
#
# Ejemplos:
#   ./install.sh ~/proyectos/mi-app mi_app
#   ./install.sh ~/proyectos/foo foo_tools foo-tools \
#       --author-name "Ada Lovelace" --author-email ada@example.com --github-user ada
# ============================================================================

set -euo pipefail

usage() {
    sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'
    exit "${1:-1}"
}

# --- Parseo de argumentos ----------------------------------------------------
POSITIONAL=()
AUTHOR_NAME=""
AUTHOR_EMAIL=""
GITHUB_USER=""
NO_PROMPT=0

while [ $# -gt 0 ]; do
    case "$1" in
        --author-name)  AUTHOR_NAME="${2:-}"; shift 2 ;;
        --author-email) AUTHOR_EMAIL="${2:-}"; shift 2 ;;
        --github-user)  GITHUB_USER="${2:-}"; shift 2 ;;
        --no-prompt)    NO_PROMPT=1; shift ;;
        -h|--help)      usage 0 ;;
        --) shift; while [ $# -gt 0 ]; do POSITIONAL+=("$1"); shift; done ;;
        -*) echo "Opción desconocida: $1" >&2; usage 1 ;;
        *)  POSITIONAL+=("$1"); shift ;;
    esac
done

if [ "${#POSITIONAL[@]}" -lt 2 ]; then
    usage 1
fi

TARGET_DIR="${POSITIONAL[0]}"
PACKAGE_NAME="${POSITIONAL[1]}"
PROJECT_NAME="${POSITIONAL[2]:-${PACKAGE_NAME//_/-}}"
KIT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# --- Prompts interactivos para campos no proporcionados ----------------------
prompt_default() {
    local var_name="$1" prompt="$2" default="$3" answer
    if [ -n "${!var_name}" ]; then return; fi
    if [ "$NO_PROMPT" -eq 1 ] || [ ! -t 0 ]; then
        printf -v "$var_name" '%s' "$default"
        return
    fi
    read -r -p "$prompt [$default]: " answer || answer=""
    printf -v "$var_name" '%s' "${answer:-$default}"
}

prompt_default AUTHOR_NAME  "Autor (nombre)"     "Tu Nombre"
prompt_default AUTHOR_EMAIL "Autor (email)"      "tu@email.com"
prompt_default GITHUB_USER  "Usuario de GitHub"  "usuario"

echo "=============================================="
echo " Despliegue del kit Claude Code para Python"
echo "=============================================="
echo "Origen (kit):   $KIT_DIR"
echo "Destino:        $TARGET_DIR"
echo "Paquete:        $PACKAGE_NAME (Python con underscores)"
echo "Proyecto:       $PROJECT_NAME (PyPI con guiones)"
echo "Autor:          $AUTHOR_NAME <$AUTHOR_EMAIL>"
echo "GitHub user:    $GITHUB_USER"
echo ""

mkdir -p "$TARGET_DIR"

# --- Copia de items ----------------------------------------------------------
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

# settings.local.json es per-developer: nunca debe llegar al destino.
rm -f "$TARGET_DIR/.claude/settings.local.json"

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

# --- Sustituciones de tokens en ficheros copiados ----------------------------
echo ""
echo "Personalizando nombres y metadatos..."
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

# Escapado para sed (delimitador '|')
sed_escape() { printf '%s' "$1" | sed -e 's/[\\|&]/\\&/g'; }
ESC_PKG=$(sed_escape "$PACKAGE_NAME")
ESC_PRJ=$(sed_escape "$PROJECT_NAME")
ESC_AUTHOR=$(sed_escape "$AUTHOR_NAME")
ESC_EMAIL=$(sed_escape "$AUTHOR_EMAIL")
ESC_GH=$(sed_escape "$GITHUB_USER")

# El orden importa: 'mi_paquete' antes que 'mi-paquete' (no hay solape, pero
# 'usuario' debe sustituirse antes que cualquier ocurrencia accidental).
SED_SCRIPT="
s|mi_paquete|$ESC_PKG|g
s|mi-paquete|$ESC_PRJ|g
s|github.com/usuario/|github.com/$ESC_GH/|g
s|Tu Nombre|$ESC_AUTHOR|g
s|tu@email.com|$ESC_EMAIL|g
"

for f in "${FILES_CUSTOMIZE[@]}"; do
    path="$TARGET_DIR/$f"
    if [ -f "$path" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' -e "$SED_SCRIPT" "$path"
        else
            sed -i -e "$SED_SCRIPT" "$path"
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
if uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push; then
    echo "  · pre-commit install OK (pre-commit + commit-msg + pre-push)"
else
    echo "  · pre-commit install falló. Ejecuta manualmente:"
    echo "    uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push"
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
