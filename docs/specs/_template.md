---
id: NNNN
title: "Título corto y descriptivo"
status: Draft           # Draft | Approved | Implemented | Rejected
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "Tu nombre o handle"
implemented_in: ""      # commit hash o PR number cuando esté Implemented
related: []             # IDs de otras specs relacionadas: [0001, 0003]
---

# NNNN — Título corto y descriptivo

## 1. Resumen

> 2-4 frases. ¿Qué problema resolvemos y cómo? Si alguien lee solo este apartado debería entender la spec entera.

## 2. Motivación

¿Por qué hace falta este cambio? ¿Qué duele hoy? ¿Qué casos de uso lo motivan?

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
- [ ] Actualizar `STATE.md` y `CHANGELOG.md`

## 6. Criterios de aceptación

Lista verificable de qué debe ser cierto cuando se considere implementada.

- [ ] CA1: Comportamiento X funciona en escenario Y.
- [ ] CA2: Tests para casos límite Z.
- [ ] CA3: Documentación de la API actualizada (docstrings).

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

## 10. Decisiones durante la implementación

> Sección que rellena Claude durante `/implement-spec`. Si surgen preguntas o desviaciones de la spec, las anota aquí (sin tocar las secciones anteriores) para revisión post-implementación.

- _(vacío)_
