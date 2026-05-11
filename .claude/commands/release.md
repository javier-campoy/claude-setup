---
description: Prepara y publica una nueva versión del paquete
allowed-tools: Read, Edit, Bash(git status), Bash(git diff:*), Bash(git log:*), Bash(git tag:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(uv run:*), Bash(date:*)
argument-hint: "<versión> — p.ej. 0.2.0"
---

Prepara y publica la versión $ARGUMENTS siguiendo el flujo de release del proyecto.

## Procedimiento

1. **Valida el entorno**:
   - Si $ARGUMENTS está vacío, pide la versión al usuario y para.
   - Ejecuta `git status` — el working tree debe estar limpio. Si no lo está, para y avisa.
   - Verifica que `v$ARGUMENTS` no sea un tag existente (`git tag | grep "^v$ARGUMENTS$"`). Si existe, para.

2. **Gate de calidad**:
   - `uv run ruff check . && uv run ruff format --check . && uv run mypy src && uv run pytest`
   - Si algo falla, para. No se puede hacer un release con la suite rota.

3. **Bump de versión**:
   - Actualiza el campo `version` en `pyproject.toml` a $ARGUMENTS.

4. **Actualiza el changelog**:
   - Lee `docs/changelog.md`.
   - Renombra `## [No publicado]` → `## [$ARGUMENTS] - <fecha de hoy>`.
   - Añade nueva sección `## [No publicado]` vacía al principio (con subsecciones en blanco).

5. **Commit de release**:
   ```
   git add pyproject.toml docs/changelog.md
   git commit -m "chore: release v$ARGUMENTS"
   ```

6. **Tag anotado**:
   ```
   git tag -a v$ARGUMENTS -m "Release v$ARGUMENTS"
   ```

7. **Push** (pide confirmación explícita antes):
   ```
   git push && git push --tags
   ```
   El workflow `release.yml` de GitHub Actions creará el Release automáticamente.

8. **Reporta**:
   - Versión publicada y hash del commit.
   - Recuerda al usuario revisar que el workflow de release pase en GitHub Actions.

## Reglas

- NUNCA hagas push sin confirmación explícita del usuario.
- NUNCA hagas un release si los tests fallan.
- NUNCA modifiques versiones publicadas anteriores en el changelog.
