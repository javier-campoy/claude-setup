# Documentación por módulo

Cada fichero de esta carpeta describe un módulo Python concreto de `src/`. Son generados y mantenidos automáticamente por Claude tras cada cambio significativo en el código fuente.

## Índice

| Módulo | Fichero | Descripción breve |
|--------|---------|-------------------|
| _(vacío — Claude lo rellena cuando existan módulos en `src/`)_ | | |

## Cómo se gestiona

- **Generado por**: `/state`, `/docs` y `/implement-spec` tras cada cambio en `src/`.
- **Mantenido por**: el agente `docs-maintainer` en auditorías de coherencia.
- **Formato**: cada fichero sigue `_template.md`.

## Reglas

- **No edites estos ficheros a mano** salvo correcciones puntuales. Los regenera Claude.
- **Un fichero por módulo Python** (`src/<paquete>/foo.py` → `docs/modules/foo.md`).
- Para submódulos de paquetes anidados: `src/<paquete>/sub/bar.py` → `docs/modules/sub.bar.md`.
