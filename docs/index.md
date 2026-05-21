# Documentación del proyecto

Esta carpeta contiene la documentación viva del repositorio. Está pensada para leerse desde un editor o desde GitHub directamente — no se publica como sitio web.

## Mapa

| Fichero / carpeta | Para qué sirve | Quién lo actualiza |
|---|---|---|
| **[VISION.md](VISION.md)** | El norte del proyecto: hacia dónde vamos y por qué (objetivos, no-objetivos, principios, temas estratégicos). Se construye **antes** de la primera spec. | Tú (o Claude con `/vision`, con confirmación). Humano, evoluciona deliberadamente. |
| **[STATE.md](STATE.md)** | Estado actual del repo: arquitectura, módulos, stack, decisiones técnicas y specs activas. | Auto-actualizado por Claude tras cambios en `src/`. Revísalo en cada PR. |
| **[changelog.md](changelog.md)** | Historial cronológico de cambios. Formato Keep a Changelog. | Auto-actualizado por Claude tras cambios en `src/`. |
| **[specs/](specs/)** | Especificaciones de features/cambios. Una spec se aprueba antes de implementar. | Tú con `/spec`, luego Claude la implementa con `/implement-spec`. |
| **[modules/](modules/)** | Documentación por módulo: API pública, responsabilidad, dependencias, ejemplos. Un `.md` por cada módulo Python en `src/`. | Auto-generado por Claude con `/docs`, `/state` e `/implement-spec`. |

## Flujo spec-driven

```
0. /vision "describe tu proyecto"   (una vez, antes de la primera spec)
   → Claude crea/rellena docs/VISION.md (el norte). Tú lo revisas y ajustas.

1. /spec "descripción de lo que quieres"
   → Claude verifica que la visión existe (si no, te manda a /vision)
   → Claude crea docs/specs/NNNN-slug.md (estado: Draft), alineada con el norte

2. Revisas, editas, apruebas
   → Cambias el estado de la spec a Approved

3. /implement-spec docs/specs/NNNN-slug.md
   → Claude implementa el código siguiendo la spec
   → Auto-actualiza STATE.md y changelog.md
   → Marca la spec como Implemented

4. /commit
   → Pasa el gate de calidad y commitea
```

## Reglas

- **VISION.md se construye antes de la primera spec** y evoluciona deliberadamente (con `/vision`). Es el norte: toda spec debe poder justificarse contra él. No lo regenera `/state`.
- **STATE.md, changelog.md y `modules/*.md` no se editan a mano** salvo correcciones puntuales. Los gestiona Claude.
- **Las specs son la fuente de verdad** para cualquier cambio no trivial. Si haces algo importante sin spec, creas una spec retroactiva.
- **Una spec por unidad de cambio**. Refactors grandes, features, cambios breaking → spec. Hotfixes triviales → directo al commit.
- **Un `modules/<modulo>.md` por módulo Python**. Se crea cuando el módulo aparece y se actualiza cada vez que cambia su API pública.
