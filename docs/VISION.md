# VISION.md — plantilla avanzada para flujo spec-driven

> 🧭 **Este es el norte del proyecto** (la visión): el documento prescriptivo y de propiedad humana contra el que se justifica toda spec del flujo spec-driven. Complementa a [`STATE.md`](STATE.md) (foto del presente, autogenerada) sin solaparse.
>
> Documento vivo. Última revisión: *(YYYY-MM-DD)* (rev. X — *resumen corto del cambio*).
> Revisiones previas: *(histórico resumido opcional)*
>
> **Lenguaje principal del proyecto:** *[VERIFICAR]*
> **Objetivo:** *[VERIFICAR — frase corta sobre el producto final]*.

---

# 1. Visión y principios de diseño

## 1.1 Qué queremos construir

> 1-3 párrafos. Describe la experiencia, producto o sistema final que queremos que exista cuando el proyecto madure.

*[VERIFICAR] Describe el producto y la experiencia objetivo.*

---

## 1.2 Alcance del repositorio

> Define explícitamente qué vive en este repo y qué no. Evita ambigüedades futuras.

**Este repositorio contiene:**

* *[VERIFICAR]*
* *[VERIFICAR]*

**Fuera de alcance de este repositorio:**

* *[VERIFICAR]*
* *[VERIFICAR]*

---

## 1.3 Principios no negociables

> Reglas de diseño de alto nivel. Cuando haya conflicto entre alternativas, estas prioridades mandan.

1. ***[VERIFICAR — principio]***
   *Explicación y trade-off.*

2. ***[VERIFICAR — principio]***
   *Explicación y trade-off.*

3. ***[VERIFICAR — principio]***
   *Explicación y trade-off.*

4. ***[VERIFICAR — principio]***
   *Explicación y trade-off.*

5. ***[VERIFICAR — principio]***
   *Explicación y trade-off.*

---

## 1.4 Filosofía operativa

> Cómo queremos que evolucione el proyecto.

* Qué priorizamos primero.
* Qué estamos dispuestos a sacrificar.
* Qué tipo de complejidad aceptamos.
* Qué tipo de complejidad rechazamos.

*[VERIFICAR] Describe la filosofía operativa.*

---

## 1.5 Restricciones estratégicas

> Restricciones duras del proyecto.

* *[VERIFICAR] presupuesto*
* *[VERIFICAR] equipo*
* *[VERIFICAR] tiempo*
* *[VERIFICAR] dependencias externas*
* *[VERIFICAR] licencias o compliance*

---

## 1.6 Definición de éxito

> Cómo sabremos que el proyecto “funciona” a nivel de producto.

| Señal         | Objetivo      |
| ------------- | ------------- |
| *[VERIFICAR]* | *[VERIFICAR]* |
| *[VERIFICAR]* | *[VERIFICAR]* |

---

# 2. Stack técnico

> Solo decisiones relevantes a medio/largo plazo. Las decisiones temporales o experimentales viven en `STATE.md` o en specs.

| Capa            | Recomendación | Alternativa   | Justificación |
| --------------- | ------------- | ------------- | ------------- |
| Backend         | *[VERIFICAR]* | *[VERIFICAR]* | *[VERIFICAR]* |
| Base de datos   | *[VERIFICAR]* | *[VERIFICAR]* | *[VERIFICAR]* |
| Cache / colas   | *[VERIFICAR]* | *[VERIFICAR]* | *[VERIFICAR]* |
| Frontend        | *[VERIFICAR]* | *[VERIFICAR]* | *[VERIFICAR]* |
| Infraestructura | *[VERIFICAR]* | *[VERIFICAR]* | *[VERIFICAR]* |
| Observabilidad  | *[VERIFICAR]* | *[VERIFICAR]* | *[VERIFICAR]* |
| Testing         | *[VERIFICAR]* | *[VERIFICAR]* | *[VERIFICAR]* |

> **Estado de las decisiones:**
>
> * *[VERIFICAR — qué está cerrado y qué sigue abierto].*

---

# 3. Inventario de repos, referencias y dependencias externas

> Lista de repos OSS, servicios o referencias conceptuales que probablemente vayamos a reutilizar, estudiar o portar.

## 3.1 Tabla de adopción

| Recurso       | Para qué | Tier | Riesgo legal/técnico | Acción |
| ------------- | -------- | ---- | -------------------- | ------ |
| *[VERIFICAR]* |          |      |                      |        |

### Tier recomendado

* **Alto** → probablemente se adopta.
* **Medio** → útil como referencia.
* **Bajo** → inspiración o descartado.

---

## 3.2 Recursos no-código

* *[VERIFICAR] datasets*
* *[VERIFICAR] assets*
* *[VERIFICAR] documentación*
* *[VERIFICAR] papers*

---

## 3.3 Reglas de licencia y adopción

> Política para evitar problemas legales o deuda invisible.

* Cómo se valida una licencia.
* Qué licencias son aceptables.
* Qué licencias están prohibidas.
* Cómo se documentan atribuciones.
* Qué implica usar código sin licencia.

*[VERIFICAR] Define la política.*

---

# 4. Roadmap por fases

> El roadmap debe describir capacidades de producto, no tareas técnicas sueltas.

---

## Fase 0 — Diseño y andamiaje

### Objetivo

*[VERIFICAR]*

### Checklist

* [ ] *[VERIFICAR]*
* [ ] *[VERIFICAR]*
* [ ] *[VERIFICAR]*

### Entregable

*[VERIFICAR] Qué se puede hacer al cerrar la fase.*

---

## Fase 1 — MVP funcional

### Objetivo

*[VERIFICAR]*

### Sub-fases sugeridas

#### 1.0 Inicialización

* [ ] *[VERIFICAR]*

#### 1.1 Núcleo funcional

* [ ] *[VERIFICAR]*

#### 1.2 Persistencia

* [ ] *[VERIFICAR]*

#### 1.3 Herramientas operativas

* [ ] *[VERIFICAR]*

#### 1.4 Definition of Done

* [ ] *[VERIFICAR — criterio chequeable]*
* [ ] *[VERIFICAR — criterio chequeable]*
* [ ] *[VERIFICAR — criterio chequeable]*

### Entregable

*[VERIFICAR]*

### Reusar de repos

* *[VERIFICAR]*

### Mitigaciones relevantes

* *[VERIFICAR]*

---

## Fase 2 — Escalabilidad y persistencia

### Objetivo

*[VERIFICAR]*

### Capacidades previstas

#### 2.0 Arquitectura base

* *[VERIFICAR]*

#### 2.1 Optimización

* *[VERIFICAR]*

#### 2.2 Persistencia avanzada

* *[VERIFICAR]*

#### 2.3 Automatización

* *[VERIFICAR]*

#### 2.4 Definition of Done

* [ ] *[VERIFICAR]*
* [ ] *[VERIFICAR]*

### Entregable

*[VERIFICAR]*

---

## Fase 3 — Producto avanzado

### Objetivo

*[VERIFICAR]*

### Capacidades previstas

* *[VERIFICAR]*
* *[VERIFICAR]*
* *[VERIFICAR]*

### Entregable

*[VERIFICAR]*

---

## Fase 4 — Pulido y producción

### Objetivo

*[VERIFICAR]*

### Capacidades previstas

* *[VERIFICAR]*
* *[VERIFICAR]*
* *[VERIFICAR]*

### Entregable

*[VERIFICAR]*

---

# 5. Filosofía de arquitectura y adjudicación

> Sección opcional pero recomendada para proyectos complejos.
>
> Aquí se documentan:
>
> * límites entre lógica determinista y heurística,
> * responsabilidades de cada capa,
> * invariantes importantes,
> * contratos conceptuales del sistema.

## 5.1 Separación de responsabilidades

| Responsabilidad | Sistema       |
| --------------- | ------------- |
| *[VERIFICAR]*   | *[VERIFICAR]* |
| *[VERIFICAR]*   | *[VERIFICAR]* |

---

## 5.2 Invariantes

* *[VERIFICAR]*
* *[VERIFICAR]*
* *[VERIFICAR]*

---

# 6. Riesgos, mitigaciones y anti-patrones

> Lista de problemas conocidos que podrían degradar el producto si no se controlan.

| Riesgo        | Impacto | Mitigación |
| ------------- | ------- | ---------- |
| *[VERIFICAR]* |         |            |

---

## 6.1 Anti-patrones explícitos

> Cosas que parecen buena idea pero el proyecto decide evitar deliberadamente.

* *[VERIFICAR]*
* *[VERIFICAR]*
* *[VERIFICAR]*

---

# 7. Coste, rendimiento y sostenibilidad

> Especialmente importante si hay IA, APIs externas o infraestructura costosa.

| Área          | Coste esperado | Estrategia |
| ------------- | -------------- | ---------- |
| *[VERIFICAR]* |                |            |

---

## 7.1 Objetivos operativos

* *[VERIFICAR] latencia*
* *[VERIFICAR] coste por usuario*
* *[VERIFICAR] throughput*
* *[VERIFICAR] caching*
* *[VERIFICAR] degradación graceful*

---

# 8. Operación y mantenimiento

## 8.1 Filosofía de specs

> Cómo se espera que interactúen `/vision`, `/spec`, `/implement-spec` y `STATE.md`.

*[VERIFICAR]*

---

## 8.2 Política de evolución

* Qué decisiones requieren cambiar VISION.
* Qué decisiones solo afectan STATE.
* Cuándo se crea una nueva spec.
* Cuándo se reemplaza una directriz.

*[VERIFICAR]*

---

# 9. Riesgos estratégicos

> Riesgos a nivel de producto o negocio.

| Riesgo        | Probabilidad    | Impacto         | Mitigación    |
| ------------- | --------------- | --------------- | ------------- |
| *[VERIFICAR]* | Baja/Media/Alta | Bajo/Medio/Alto | *[VERIFICAR]* |

---

# 10. Decisiones abiertas

> Preguntas estratégicas todavía no cerradas.

| Tema          | Estado  | Próximo paso  |
| ------------- | ------- | ------------- |
| *[VERIFICAR]* | Abierto | *[VERIFICAR]* |

---

# 11. Historial de revisiones

> Registro de cómo ha evolucionado la visión del proyecto.

| Revisión | Fecha          | Autor     | Qué cambió y por qué           |
| -------- | -------------- | --------- | ------------------------------ |
| v1       | *(YYYY-MM-DD)* | *(autor)* | Creación inicial de la visión. |

---

# 12. Directrices estratégicas e inventarios de specs

> Esta sección conecta el norte estratégico con el flujo spec-driven.

---

## 12.1 Directrices estratégicas vigentes

> Reglas de norte citables `DV-NN`.

| ID    | Origen        | Directriz     | Estado  |
| ----- | ------------- | ------------- | ------- |
| DV-01 | *[VERIFICAR]* | *[VERIFICAR]* | Vigente |

---

## 12.2 Ideas de specs registradas

> Inventario histórico de specs creadas vía `/spec`.

Formato canónico:

```md
- **NNNN — `<slug>`** _(estado: Draft|Approved|Implemented, registrado: YYYY-MM-DD)_ — `<resumen corto>`. Avanza: `<vision_refs>`. _Implementada en: <hash>|pendiente._
```

* *(vacío)*

---

## 12.3 Ideas para futuras specs (sin spec asociada todavía)

> Backlog de ideas emergentes detectadas durante el flujo spec-driven.

Formato canónico:

```md
- **`<slug-tentativo>`** _(propuesta por spec NNNN el YYYY-MM-DD)_ — `<motivación>`. Estado: propuesta | consolidada en NNNN-<slug>.
```

* *(vacío)*
