---
id: 0001
title: "Ejemplo: parser de URLs"
status: Draft
created: 2026-05-07
updated: 2026-05-07
author: "Javier"
implemented_in: ""
related: []
---

# 0001 — Ejemplo: parser de URLs

> Esta es una spec **de ejemplo** para que veas cómo se rellena la plantilla. Bórrala o úsala como referencia.

## 1. Resumen

Añadir un módulo `mi_paquete.urls` que parsea URLs y devuelve sus componentes como un objeto inmutable, con validación estricta del esquema y soporte para query strings tipados.

## 2. Motivación

Hoy tenemos código que parsea URLs en tres sitios distintos con `urllib.parse`, cada uno con manejo de errores diferente. Queremos centralizar esto en un solo módulo con una API consistente.

Casos de uso:

- Validar URLs de entrada en la CLI.
- Extraer componentes para construir URLs derivadas.
- Comparar URLs canonicalizadas (mismo host, mismo path normalizado).

## 3. Propuesta

### API pública

```python
from mi_paquete.urls import parse_url, URL

url: URL = parse_url("https://example.com/api/v1/users?id=42")

url.scheme   # "https"
url.host     # "example.com"
url.port     # None
url.path     # "/api/v1/users"
url.query    # {"id": "42"}
url.canonical()  # URL canonicalizada (lowercase host, path normalizado)
```

### Comportamiento

- Solo acepta esquemas `http` y `https` por defecto.
- Lanza `InvalidURLError` si el formato es inválido.
- `URL` es un `dataclass(frozen=True)`.

### Estructura

```
src/mi_paquete/
└── urls/
    ├── __init__.py     # Re-exporta parse_url, URL, InvalidURLError
    ├── parser.py       # Lógica de parseo
    └── errors.py       # InvalidURLError
```

### Ejemplo de uso (post-implementación)

```python
from mi_paquete.urls import parse_url

try:
    url = parse_url("https://example.com/path?x=1")
except InvalidURLError as e:
    print(f"URL inválida: {e}")
```

## 4. Alternativas consideradas

| Alternativa | Pros | Contras | Por qué no |
|---|---|---|---|
| Usar `urllib.parse` directamente | Sin deps | API verbosa, sin validación | Es lo que tenemos hoy y queremos mejorarlo |
| Usar `yarl` | Maduro, completo | Dep extra, API más compleja de la que necesitamos | Overkill para el alcance actual |
| Solo añadir helpers sobre `urllib` | Mínimo cambio | Sigue habiendo 3 sitios distintos | No resuelve la consistencia |

## 5. Plan de implementación

- [ ] Crear `src/mi_paquete/urls/errors.py` con `InvalidURLError`.
- [ ] Crear `src/mi_paquete/urls/parser.py` con `URL` (dataclass frozen) y `parse_url()`.
- [ ] Crear `src/mi_paquete/urls/__init__.py` re-exportando los símbolos públicos.
- [ ] Tests en `tests/urls/test_parser.py` cubriendo: caso feliz, esquemas inválidos, query strings, URLs malformadas.
- [ ] Migrar los 3 sitios actuales que usan `urllib.parse` a la nueva API.
- [ ] Actualizar `docs/STATE.md` y `docs/changelog.md`.

## 6. Criterios de aceptación

- [ ] `parse_url("https://example.com")` devuelve un `URL` con campos correctos.
- [ ] `parse_url("ftp://...")` lanza `InvalidURLError`.
- [ ] Cobertura ≥90% en `mi_paquete.urls`.
- [ ] Los 3 callers existentes están migrados y sus tests pasan.
- [ ] Docstrings estilo Google en toda la API pública.

## 7. Compatibilidad y migración

Cambio aditivo: introduce un nuevo módulo. Los callers internos se migran como parte de esta spec. No hay impacto en usuarios externos del paquete porque `mi_paquete.urls` es nuevo.

## 8. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| API divergente respecto a `urllib.parse` confunde usuarios | Media | Bajo | Documentar bien el porqué en docstring del módulo |
| Algún caller migrado introduce regresión | Media | Medio | Tests de integración antes de mergear |

## 9. Notas y enlaces

- Issues relacionados: ninguno
- Inspiración: `yarl`, `furl`

## 10. Decisiones durante la implementación

- _(vacío)_
