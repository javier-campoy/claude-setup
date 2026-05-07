---
module: mi_paquete.nombre_modulo
updated: YYYY-MM-DD
commit: abcdef0
---

# `mi_paquete.nombre_modulo`

> _Descripción en una línea extraída del docstring del módulo. Si no hay docstring, Claude infiere una desde el código._

## Responsabilidad

_Qué hace este módulo, por qué existe y qué problema resuelve dentro del paquete. 2-4 frases._

## API pública

_Solo funciones, clases y constantes exportadas (sin underscore prefijo o listadas en `__all__`)._

### Clases

#### `NombreClase(arg1: Tipo, arg2: Tipo)`

_Descripción breve._

**Atributos**:
- `atributo_1: Tipo` — qué representa.
- `atributo_2: Tipo` — qué representa.

**Métodos públicos**:
- `metodo(arg) -> tipo` — qué hace.

---

### Funciones

#### `nombre_funcion(arg1: Tipo, arg2: Tipo) -> TipoRetorno`

_Descripción breve (imperativo)._

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `arg1` | `Tipo` | Qué es. |
| `arg2` | `Tipo` | Qué es. |

**Retorna**: qué y bajo qué condiciones.  
**Lanza**: `ErrorTipo` — cuándo.

---

### Constantes / tipos exportados

| Nombre | Tipo | Valor / descripción |
|--------|------|---------------------|
| `CONSTANTE` | `str` | Qué representa. |

## Dependencias internas

_Solo dependencias dentro del mismo paquete. Las externas no se listan._

- `mi_paquete.bar` — para qué se usa.

## Consumidores conocidos

_Quién importa de este módulo dentro del repo._

- `mi_paquete.cli` — usa `nombre_funcion` para X.
- `tests/test_nombre_modulo.py` — suite de tests del módulo.

## Ejemplos de uso

```python
from mi_paquete.nombre_modulo import nombre_funcion

resultado = nombre_funcion(arg1=..., arg2=...)
```

## Notas y decisiones

_Solo si hay algo no obvio: invariantes, workarounds, comportamiento sorprendente, decisiones de diseño locales. Vacío si no aplica._
