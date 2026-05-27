---
description: Regenera docs/STATE.md y docs/modules/*.md a partir del estado actual del código
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(git rev-parse:*), Bash(git log:*), Bash(date:*), Bash(find:*), Bash(uv run:*), Bash(wc:*)
---

Regenera `docs/STATE.md` y los ficheros `docs/modules/*.md` para reflejar el estado actual del repo.

## Parte 1 — Regenerar docs/STATE.md

1. **Lee** el `docs/STATE.md` actual para preservar contenido humano (decisiones técnicas, visión general, roadmap).

2. **Recopila datos del repo**:
   - Estructura de `src/`: con `find src -type f -name '*.py' | sort`.
   - Lista de specs en `docs/specs/`: lee el frontmatter de cada una para extraer `id`, `title`, `status`, `implemented_in`.
   - Métricas básicas:
     - Líneas de código: `find src -name '*.py' | xargs wc -l | tail -1`.
     - Cobertura: si hay `.coverage`, parsearla. Si no, dejar el valor anterior con nota "(stale)".
   - Estado de salud:
     - `uv run ruff check . > /dev/null 2>&1 && echo "✅" || echo "❌"`
     - `uv run mypy src > /dev/null 2>&1 && echo "✅" || echo "❌"`
     - `uv run pytest --co -q > /dev/null 2>&1 && echo "✅" || echo "❌"`
   - Commit base: `git rev-parse --short HEAD`.
   - Fecha: `date +%Y-%m-%d`.

3. **Reescribe `docs/STATE.md`**:
   - **Sección 1 (Visión general)**: resumen corto del presente (qué es el repo HOY) + enlace a `docs/VISION.md` como fuente autoritativa de la dirección a futuro. PRESERVAR la versión humana; no dupliques el contenido de la visión aquí, solo apunta a ella.
   - **Sección 2 (Arquitectura y módulos)**: REGENERAR con la estructura real de `src/`. Para cada módulo, infiere su responsabilidad del docstring del `__init__.py` o del módulo. Si no hay docstring, marca `_[describir]_`. Incluye enlace a `docs/modules/<nombre>.md` si existe.
   - **Sección 3 (Stack y dependencias)**: leer `pyproject.toml`, listar deps de runtime y dev/docs.
   - **Sección 4 (ADRs inline)**: PRESERVAR. NUNCA borres ADRs existentes. Solo añade nuevas si has tomado decisiones técnicas relevantes en este turno (raro).
   - **Sección 5 (Specs)**: REGENERAR las tres tablas (Activas, Implementadas, Rechazadas) leyendo el frontmatter de cada spec.
   - **Sección 6 (Estado del codebase)**: REGENERAR con las métricas y salud actuales.
   - **Sección 7 (Roadmap)**: derivado de las specs `Approved` no implementadas. PRESERVAR notas humanas adicionales.

4. **Actualiza la cabecera** con `Última actualización` y `Commit base`.

## Parte 2 — Regenerar docs/modules/*.md

Para cada módulo bajo `src/`, infiere el mapeo automáticamente:
- `src/<paquete>/<modulo>.py` → `docs/modules/<modulo>.md`
- `src/<paquete>/<sub>/` (subpaquete) → `docs/modules/<sub>.md`

Ejecuta `find src -type f -name '*.py' | sort` para listar todos los módulos y derivar el mapeo completo.

Para cada fichero de módulo:
1. Lee el fichero existente (si existe) para preservar `## Visión general`.
2. Lee los `.py` del módulo correspondiente.
3. Extrae todas las clases y funciones públicas (sin prefijo `_`) con sus docstrings y firmas.
4. Regenera la sección `## API pública` con la información actual.
5. Regenera la sección `## Dependencias` analizando los imports.
6. Actualiza `last_updated` en el frontmatter.
7. Si el fichero no existe, créalo desde `docs/modules/_template.md`.

## Parte 3 — Reportar

```
## /state completado

**Fecha**: YYYY-MM-DD | **Commit**: abc1234

### STATE.md
- Sección 2: X módulos listados.
- Sección 3: Y dependencias runtime, Z dev.
- Sección 5: N specs (A activas, B implementadas, C rechazadas).
- Sección 6: ruff ✅ mypy ✅ pytest ✅ | LOC: XXXX

### docs/modules/ actualizados
- <modulo>.md: X clases, Y funciones públicas
- ...

### Pendiente de decisión humana
- ⚠️ <lista de items que necesitan confirmación>
```

## Reglas

- **NUNCA toques `docs/VISION.md`**. La visión es prescriptiva y de propiedad humana; se edita con `/vision`, no con `/state`. `/state` solo la lee para mantener alineada la sección 1 de STATE.md. Si detectas que el código contradice el norte, NO edites la visión: márcalo con `<!-- TODO: posible desalineación con VISION.md: ... -->` y avisa al usuario.
- **NUNCA borres ADRs**. Son histórico, solo se añaden.
- **NUNCA cambies decisiones de diseño** ya documentadas; si crees que hay que cambiarlas, abre una spec nueva.
- **PRESERVA** la sección `## Visión general` de cada `docs/modules/*.md`.
- Si una sección humana (Visión general, Roadmap) parece desactualizada respecto al código, NO la edites: marca con un comentario HTML `<!-- TODO: revisar, parece desactualizado tras cambios en X -->`.
