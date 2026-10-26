---
id: NNNN
title: "Título corto y descriptivo"
status: Draft           # Draft | Approved | Implemented | Rejected
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "Tu nombre o handle"
implemented_in: ""      # commit hash o número de merge request (!NN) cuando esté Implemented
related: []             # IDs de otras specs relacionadas: [0001, 0003]
vision_refs: []         # objetivos/temas de docs/VISION.md que avanza: ["O2", "T1"]
directives_followed: [] # IDs de directrices STATE §5.5 (D-NN) y/o VISION §12.1 (DV-NN) que esta spec honra
directives_closed: []   # IDs de directrices que esta spec cierra (típicamente del backlog en STATE §5.5)
directives_opened: []   # IDs propuestos para directrices nuevas que emergen de la spec
vision_idea_ref: ""     # Ancla de la entrada en VISION §12.2 (auto-rellenada por /spec): "§12.2 idea NNNN"
---

# NNNN — Título corto y descriptivo

## 1. Resumen

> 2-4 frases. ¿Qué problema resolvemos y cómo? Si alguien lee solo este apartado debería entender la spec entera.

## 2. Motivación

¿Por qué hace falta este cambio? ¿Qué duele hoy? ¿Qué casos de uso lo motivan?

### Alineación con la visión

> Conecta esta spec con el norte del proyecto ([`docs/VISION.md`](../VISION.md)). ¿Qué objetivo(s) y tema(s) estratégico(s) avanza? Si no encaja con ningún objetivo, dilo: quizá la visión deba evolucionar (con `/vision`) o la spec replantearse.

- **Avanza**: _(p.ej. O2 — "reducir el boilerplate", dentro del tema T1)_
- **Objetivos que esta spec cierra** (`/implement-spec` propondrá marcarlos `[x]` en VISION §4 con confirmación humana si la spec los cumple completamente, no solo avanza): _(p.ej. "O2 queda cerrado con esta spec porque cubre el caso completo")_
- **Idea registrada en VISION**: _(rellena `/spec` con la confirmación humana; ancla `§12.2 idea NNNN`)_

### Directrices que esta spec cumple, cierra o abre

> Cita por ID las directrices de [`docs/STATE.md`](../STATE.md) §5.5 "Directrices vigentes para próximas specs" (`D-NN` tácticas) y/o de [`docs/VISION.md`](../VISION.md) §12.1 "Directrices estratégicas vigentes" (`DV-NN` estratégicas) que esta spec honra, cierra o **propone añadir** (las que emergen de la propia spec). Coordínalo con el frontmatter `directives_followed` / `directives_closed` / `directives_opened`.

| ID | Acción | Nota breve |
|---|---|---|
| D-NN o DV-NN | cumple | _(p.ej. "Honra la directriz D-03: API pública estable")_ |
| D-NN | cierra | _(p.ej. "Esta spec implementa el backlog declarado en D-05")_ |
| D-NUEVA | abre (propone) | _(p.ej. "Tras esta spec, todo módulo X debe pasar por validador Y")_ |

## 3. Propuesta

Descripción detallada de la solución. Incluye:

- **API pública afectada**: nuevas funciones/clases, cambios en firmas existentes.
- **Comportamiento**: qué hace, qué no hace.
- **Estructura**: en qué módulos vive el código nuevo.
- **Datos / persistencia** (si aplica): formato, migraciones.

### Ejemplo de uso (post-implementación)

```python
# Cómo lo usaría el usuario final tras implementar la spec
from mi_paquete import nueva_api

resultado = nueva_api.haz_algo(...)
```

## 4. Alternativas consideradas

| Alternativa | Pros | Contras | Por qué no |
|---|---|---|---|
| _(opción A)_ | | | |

## 5. Plan de implementación

Pasos concretos en orden. Marcar checkboxes cuando se completan.

- [ ] Paso 1 — _qué hacer y dónde_
- [ ] Paso 2
- [ ] Paso 3
- [ ] Tests
- [ ] Actualizar `STATE.md` y `changelog.md`

## 6. Criterios de aceptación

Lista verificable de qué debe ser cierto cuando se considere implementada.

- [ ] CA1: Comportamiento X funciona en escenario Y.
- [ ] CA2: Tests para casos límite Z.
- [ ] CA3: Documentación de la API actualizada (docstrings).
- [ ] CA4: CI verde — el pipeline de `.gitlab-ci.yml` pasa en el push o merge request de implementación.

## 7. Compatibilidad y migración

¿Es breaking? ¿Cómo migran los usuarios existentes? ¿Hay deprecation period?

## 8. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| _(riesgo A)_ | Baja/Media/Alta | Bajo/Medio/Alto | _(plan)_ |

## 9. Notas y enlaces

- Issues relacionados: #N
- Discusiones: enlaces relevantes
- Referencias externas: papers, blog posts, RFCs de otras librerías

<!--
Si la spec es no trivial (módulo nuevo, boundaries entre componentes, API pública, decisión de diseño que podría acabar en ADR, solapamiento con otra spec activa), pasa /spec-review antes de aprobarla. El comando insertará aquí la subsección:

## Revisión arquitectónica

con el veredicto del subagente spec-architect (Opus) y los cambios mínimos propuestos. Para specs triviales, sáltatela.
-->

## 10. Decisiones durante la implementación

> Sección que rellena Claude durante `/implement-spec`. Si surgen preguntas o desviaciones de la spec, las anota aquí (sin tocar las secciones anteriores) para revisión post-implementación.

- _(vacío)_
