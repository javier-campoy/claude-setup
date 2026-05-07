# Specs

Cada cambio significativo del proyecto empieza con una **spec**: un documento Markdown que describe el problema, la solución propuesta y los criterios de aceptación. Las specs se aprueban **antes** de implementar.

## Convenciones

- **Nombre**: `NNNN-slug-corto.md` donde `NNNN` es un número secuencial de 4 dígitos.
  - Ejemplo: `0001-parser-de-urls.md`, `0002-cache-en-memoria.md`.
- **Estado**: en el frontmatter de cada spec: `Draft` → `Approved` → `Implemented` (o `Rejected`).
- **Una spec por unidad de cambio coherente**. Si tocas tres cosas no relacionadas, son tres specs.

## Ciclo de vida

```
┌─────────┐     /spec    ┌───────────┐   revisión    ┌──────────┐  /implement-spec  ┌─────────────┐
│  idea   │  ─────────▶  │   Draft   │  ──────────▶  │ Approved │  ──────────────▶  │ Implemented │
└─────────┘              └───────────┘               └──────────┘                   └─────────────┘
                                │
                                │ rechazo
                                ▼
                          ┌───────────┐
                          │ Rejected  │
                          └───────────┘
```

## Crear una spec

```
/spec "descripción breve de lo que quieres"
```

Claude:
1. Lee `STATE.md` para entender el contexto del repo.
2. Asigna el siguiente número (`NNNN`).
3. Crea `docs/specs/NNNN-slug.md` usando la plantilla en `_template.md`.
4. Estado inicial: `Draft`.

Tú revisas, editas, y cuando estás conforme cambias el campo `status` a `Approved`.

## Implementar una spec

```
/implement-spec docs/specs/NNNN-slug.md
```

Claude:
1. Lee la spec.
2. Verifica que su estado es `Approved`. Si no, para.
3. Implementa los cambios siguiendo la spec **al pie de la letra**.
4. Si en mitad encuentra algo que no encaja con la spec, **NO improvisa**: para y lo discute.
5. Al terminar:
   - Marca la spec como `Implemented` con commit/PR de referencia.
   - Actualiza `docs/STATE.md` (movida de Active → Implemented).
   - Añade entrada en `docs/CHANGELOG.md`.

## Plantilla

Ver [`_template.md`](_template.md). Cópialo y rellénalo cuando quieras escribir una spec a mano.

## Índice de specs

> Esta tabla la mantiene Claude. La fuente de verdad sigue siendo el frontmatter de cada fichero.

| ID | Título | Estado | Owner | Última actualización |
|---|---|---|---|---|
| _(vacío)_ | | | | |
