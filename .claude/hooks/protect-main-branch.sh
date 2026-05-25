#!/usr/bin/env bash
# pre-commit: bloquea commits directos a main/master. Trabaja en ramas feat/..., fix/....
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo ""
    echo "ERROR: commits directos a \"$BRANCH\" no están permitidos."
    echo "  Crea una rama: git checkout -b feat/<nombre>"
    echo ""
    exit 1
fi
