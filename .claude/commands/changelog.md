---
description: Añade entradas al docs/CHANGELOG.md a partir de los cambios recientes
allowed-tools: Read, Edit, Bash(git diff:*), Bash(git log:*), Bash(git status), Bash(date:*)
argument-hint: "[rango git, p.ej. 'desde HEAD~3' o 'desde main']"
---

Actualiza `docs/changelog.md` con entradas para los cambios recientes.

## Procedimiento

1. **Determina el rango**:
   - Si $ARGUMENTS contiene un rango git, úsalo.
   - Si no, usa los cambios pendientes (`git status` + `git diff --staged` + `git diff`).
   - Si no hay cambios y no hay rango, avisa al usuario y termina.

2. **Lee `docs/changelog.md`** para conocer el formato actual y la sección `[No publicado]`.

3. **Analiza los cambios**:
   - Mira los ficheros modificados.
   - Para cada uno, identifica el TIPO de cambio:
     - **Añadido**: nueva funcionalidad, nuevos módulos.
     - **Cambiado**: cambios en comportamiento existente (no breaking).
     - **Deprecado**: APIs marcadas como deprecadas.
     - **Eliminado**: APIs/features quitadas (breaking).
     - **Arreglado**: bugs corregidos.
     - **Seguridad**: vulnerabilidades.

4. **Genera entradas**:
   - Una entrada por cambio coherente. NO una entrada por fichero.
   - Estilo: imperativo, conciso, en el mismo idioma que el resto del changelog.
   - Ejemplo: `- Añadir parser de URLs con validación estricta de esquema.`
   - Si el cambio implementa una spec, referenciarla: `(spec [0001](specs/0001-parser-de-urls.md))`.
   - Si el commit menciona issue/PR, referenciarlo: `(#42)`.

5. **Edita `docs/changelog.md`**:
   - Inserta las entradas bajo `[No publicado]` en la subsección correcta.
   - Si la subsección dice `_Pendiente de cambios._`, reemplaza ese placeholder con la primera entrada.
   - NO toques las versiones publicadas (`[X.Y.Z]`).

6. **Reporta** las entradas añadidas con su categoría.

## Reglas

- Si no estás seguro del tipo de cambio, pregunta antes de meterlo en una categoría errónea.
- Cambios puramente internos (refactors sin impacto visible, formato, comentarios, tests) **no van al changelog** salvo que el usuario lo pida explícitamente.
- Si una sola entrada cubriría varios cambios pequeños, agrúpalos bien.
