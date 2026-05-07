---
description: Genera o actualiza docstrings (estilo Google) en funciones y clases, y sincroniza docs/modules/*.md
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
argument-hint: "<ruta/al/fichero.py | directorio | nombre_modulo>"
---

Genera o mejora docstrings en el target indicado en `$ARGUMENTS` (fichero `.py`, directorio, o nombre de módulo).

## Paso 1 — Docstrings en código

Para cada función/método/clase pública (sin underscore prefijo):

- Si **no tiene docstring**, créalo.
- Si **tiene docstring incompleto o desactualizado**, mejóralo.
- Si **el docstring está OK**, déjalo igual.

Formato (Google style), en el idioma dominante del codebase:

```python
def funcion(arg1: int, arg2: str) -> bool:
    """Brief one-line summary (imperative mood).

    Longer explanation if needed. Focus on *why*, not *what*.

    Args:
        arg1: Description.
        arg2: Description.

    Returns:
        What it returns and under what conditions.

    Raises:
        ValueError: When this is raised.
    """
```

Reglas:
- Idioma consistente con el resto del codebase.
- No añadas docstrings triviales que solo repiten el nombre.
- En clases, documenta atributos en la sección `Attributes:` del docstring de clase.
- Para funciones privadas (`_foo`) solo añade docstring si la lógica no es obvia.
- Después ejecuta `uv run ruff format .` para asegurar formato.

## Paso 2 — Actualizar docs/modules/*.md

Tras añadir o mejorar docstrings, actualiza el fichero `docs/modules/` correspondiente al módulo afectado.

**Cómo identificar el fichero de docs:**
- `src/<paquete>/<modulo>.py` → `docs/modules/<modulo>.md`
- `src/<paquete>/<sub>/<modulo>.py` → `docs/modules/<sub>.<modulo>.md`
- Para directorios/subpaquetes: `src/<paquete>/<sub>/` → `docs/modules/<sub>.md`

Para cada módulo afectado:
1. Lee el fichero `docs/modules/<modulo>.md` existente.
2. Regenera la sección `## API pública` con las clases/funciones reales y sus docstrings actualizados.
3. Actualiza `last_updated` en el frontmatter.
4. **PRESERVA** la sección `## Visión general` si contiene texto humano.

Si el fichero `docs/modules/<modulo>.md` no existe, créalo usando la plantilla de `docs/modules/_template.md`.
