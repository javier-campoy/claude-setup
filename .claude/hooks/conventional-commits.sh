#!/usr/bin/env bash
# commit-msg: valida que el mensaje siga Conventional Commits. $1 = fichero del mensaje.
# Formato: <tipo>[(<scope>)][!]: <resumen>  (max 72 chars)
# Tipos:   feat fix docs refactor test chore perf ci build revert
MSG=$(head -1 "$1")
if echo "$MSG" | grep -qE "^(Merge |Revert |Initial commit)"; then
    exit 0
fi
if ! echo "$MSG" | grep -qE "^(feat|fix|docs|refactor|test|chore|perf|ci|build|revert)(\(.+\))?(!)?: .{1,72}"; then
    echo ""
    echo "ERROR: el mensaje de commit no sigue Conventional Commits."
    echo "  Formato : <tipo>[(<scope>)][!]: <resumen>  (max 72 chars)"
    echo "  Tipos   : feat fix docs refactor test chore perf ci build revert"
    echo "  Ejemplo : feat(auth): añadir soporte para login social"
    echo ""
    exit 1
fi
