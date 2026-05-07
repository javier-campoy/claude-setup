---
description: Crea una nueva spec en docs/specs/ a partir de una descripción
allowed-tools: Read, Write, Glob, Bash(ls:*), Bash(git log:*), Bash(date:*)
argument-hint: "<descripción breve de la feature/cambio>"
---

Crea una spec nueva siguiendo el flujo spec-driven del proyecto.

## Procedimiento

1. **Contexto**:
   - Lee `docs/STATE.md` para entender el estado actual del repo.
   - Lee `docs/specs/_template.md` para conocer la estructura.
   - Mira `docs/specs/` (con `ls`) para determinar el siguiente número (`NNNN`): el máximo existente + 1, formateado a 4 dígitos.

2. **Slug**:
   - A partir de $ARGUMENTS, deriva un slug corto: minúsculas, palabras separadas por guiones, sin tildes, máximo ~5 palabras.
   - Ejemplo: "Quiero un parser de URLs" → `parser-de-urls`.

3. **Crea el fichero**: `docs/specs/NNNN-slug.md` copiando la plantilla y rellenando:
   - Frontmatter:
     - `id`: NNNN
     - `title`: título descriptivo en una línea
     - `status`: Draft
     - `created` y `updated`: fecha de hoy (`date +%Y-%m-%d`)
     - `author`: si lo conoces, déjalo en blanco si no
   - Sección 1 (Resumen): 2-4 frases basadas en $ARGUMENTS.
   - Sección 2 (Motivación): infiere casos de uso plausibles. Marca con `_[VERIFICAR]_` lo que no puedas inferir con seguridad.
   - Secciones 3-9: rellena con tu mejor entendimiento, marcando `_[VERIFICAR]_` donde haga falta input humano.
   - Sección 10: déjala vacía (la rellenarás al implementar).

4. **Actualiza el índice** en `docs/specs/README.md`:
   - Añade una fila a la tabla "Índice de specs".

5. **Actualiza `docs/STATE.md`** sección 5 (Specs → Activas).

6. **Reporta al usuario**:
   - Ruta del fichero creado.
   - Lista de los `_[VERIFICAR]_` que necesitan revisión humana.
   - Recordatorio de cambiar `status: Draft` → `status: Approved` cuando esté lista.

## Reglas

- **NO inventes** comportamiento técnico no pedido. Si $ARGUMENTS no especifica algo crítico, marca `_[VERIFICAR]_` en lugar de adivinar.
- **NO implementes** código aquí. Solo se crea la spec.
- Si $ARGUMENTS está vacío, pide al usuario que describa qué quiere especificar.
