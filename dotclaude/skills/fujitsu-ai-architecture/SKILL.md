---
name: fujitsu-ai-architecture
description: Arquitectura de referencia de Fujitsu AI para aplicaciones de IA en producción (ML clásico, LLM, RAG, agentes y sistemas híbridos). Úsala al diseñar, especificar (/spec), implementar o revisar cualquier componente que llame a un modelo o LLM, recupere contexto, orqueste agentes o exponga IA a usuarios, y siempre que se hable de guardarraíles, observabilidad, evaluación o preparación para producción de un sistema de IA.
---

# Arquitectura de referencia: aplicaciones de IA en producción

Destilado de la guía *Production AI Application – Engineering Guidelines* de la wiki del grupo `fujitsu_ai`. Es una línea base agnóstica de modelo, proveedor y plataforma. Lo que la guía marca como **MUST** se trata aquí como obligatorio; el resto son recomendaciones.

Fuente: https://code.mahitahi.global.fujitsu.com/groups/fujitsu_ai/-/wikis/Production-AI-Application-Architecture

## Cuándo aplica

Aplica a todo código o spec que:

- Ejecute un modelo (local o remoto) o llame a un LLM.
- Recupere contexto para un modelo (búsqueda, RAG, embeddings).
- Orqueste agentes, herramientas o flujos multi-paso.
- Exponga respuestas generadas por IA a usuarios o a otros sistemas.

No aplica a código que solo *consume* resultados ya validados sin tocar el modelo.

## Los cinco principios (MUST)

1. **Modularidad.** Cada capacidad (recuperación, razonamiento, orquestación, evaluación, observabilidad) evoluciona y se reemplaza de forma independiente.
2. **Agnosticismo tecnológico.** Nada de acoplamiento duro a una herramienta, framework, modelo o proveedor concreto.
3. **Seguridad y gobierno por diseño.** Seguridad, privacidad y cumplimiento son requisitos de arquitectura, no extensiones opcionales.
4. **Observabilidad primero.** Toda interacción con IA es trazable, medible, auditable y explicable.
5. **Evaluación continua.** Calidad, riesgo y rendimiento se miden durante todo el ciclo de vida, no solo antes del primer despliegue.

### Cómo se traducen en código Python

| Principio | Señal de que se cumple | Señal de alarma |
|---|---|---|
| Modularidad | Retrieval, modelo y orquestación en módulos separados con interfaces explícitas | Una función que busca, construye el prompt, llama al modelo y formatea la respuesta |
| Agnosticismo | El proveedor se inyecta detrás de un `Protocol`/interfaz; el modelo se elige por configuración | `import` del SDK de un proveedor disperso por la lógica de negocio; nombres de modelo hardcodeados |
| Seguridad | Validación de entrada y salida como funciones propias, con tests | El texto del usuario se concatena al prompt sin ningún control; la salida se devuelve tal cual |
| Observabilidad | Cada petición lleva un id de traza y registra modelo, latencia, tokens/coste y resultado | `print` sueltos, o ningún registro de qué modelo respondió |
| Evaluación | Existe un dataset dorado y tests de regresión del comportamiento | Solo tests unitarios con el modelo mockeado |

## Mapa de módulos

Los nombres son orientativos. En este kit, los módulos viven bajo `src/<paquete>/`. Crea solo los que el proyecto necesite; un PoC no requiere los quince.

| Módulo | Responsabilidad |
|---|---|
| Application Layer | Entry points, configuración, schemas, ciclo de vida de peticiones |
| Core Services | Lógica de negocio, coordinación de workflows, estado |
| Retrieval Layer | Búsqueda, indexado, ranking, enriquecimiento de contexto |
| Reasoning & Intelligence | Ejecución de modelos, agentes, routing, estrategias de razonamiento |
| Prompt & Policy Management | Plantillas de prompt, políticas de comportamiento, versionado |
| Tooling Layer | Integración con sistemas externos |
| Security & Guardrails | Validación de entrada, moderación de contenido, validación de salida |
| Evaluation & Quality | Benchmarks, datasets de prueba, pipelines de evaluación |
| Observability | Trazas, métricas, logs, coste, feedback |
| Data Management | Fuentes de datos, artefactos procesados, features, embeddings |
| Automation & Operations | Automatización de despliegue, health checks, CI/CD |
| User Interface | Web, móvil o conversacional |
| Testing | Tests unitarios, de integración, de regresión y específicos de IA |
| Documentation | Arquitectura, APIs, runbooks |
| AI Assistant Context | Reglas para el desarrollo asistido por IA (en este kit: `CLAUDE.md` y `.claude/`) |

El árbol de proyecto de referencia completo, adaptado al layout `src/` del kit, está en [references/estructura-referencia.md](references/estructura-referencia.md).

## Capacidades obligatorias

### Recuperación de contexto

- Admite varias estrategias (semántica, por palabras clave, estructurada).
- Ranking y optimización de relevancia; filtrado y validación del contexto antes de pasarlo al modelo.
- **Procedencia:** cada fragmento recuperado conserva su fuente, y la respuesta puede citarla.
- **MUST:** la capa de recuperación está desacoplada de la ejecución del modelo. Cambiar de modelo no obliga a tocar el retrieval, ni al revés.

### Razonamiento, agentes y orquestación

- Selección y routing de modelos explícitos y configurables.
- Evitar depender de un solo modelo o proveedor.
- La lógica de orquestación es explícita y observable: se puede reconstruir qué pasos se ejecutaron y por qué.
- Definir rutas de *fallback* y de fallo seguro: qué ocurre si el modelo no responde, excede el tiempo o devuelve algo inválido.

### Seguridad, guardarraíles y gobierno

Protección en tres capas:

1. **Entrada:** saneado del prompt, detección de inyección y de uso indebido.
2. **Contenido:** detección de información sensible o restringida; filtrado basado en políticas.
3. **Salida:** validación de la respuesta, mitigación de alucinaciones y de riesgo, alineación con las políticas de IA responsable.

**MUST:** las reglas de gobierno son configurables, auditables y aplicables. Una regla que solo existe en un prompt no es auditable ni aplicable; debe haber código que la haga cumplir y un registro de cuándo actúa.

### Observabilidad y operación

Requisitos mínimos para considerar algo listo para producción:

- Trazado extremo a extremo de cada petición de IA y de sus decisiones.
- Métricas de rendimiento, latencia y errores.
- Seguimiento de uso de recursos y de coste.
- Mecanismos de feedback humano y automático.

### Evaluación y mejora continua

- Datasets dorados y benchmarks.
- Tests de regresión automatizados del comportamiento de la IA.
- Evaluación online a partir del feedback de usuarios.
- Detección de drift, degradación y anomalías.

Los resultados de la evaluación deben alimentar decisiones concretas: cambios de prompt y de políticas, routing de modelos y ajuste de guardarraíles.

### Documentación (MUST)

Toda aplicación de IA en producción incluye documentación de arquitectura, contratos de API e integración, runbooks operativos y artefactos de gobierno y cumplimiento. En este kit:

| Artefacto | Dónde |
|---|---|
| Arquitectura | `docs/STATE.md` y `docs/modules/` |
| Contratos de API | `docs/modules/<modulo>.md` |
| Decisiones de diseño | `docs/specs/` |
| Runbooks y gobierno | `docs/` (créalos cuando el proyecto vaya a producción) |

## Cómo usar esta guía

**Al escribir una spec** (`/spec`) de un componente de IA, la spec debe responder explícitamente:

- ¿Qué capa del mapa de módulos toca, y qué interfaz expone?
- ¿Cómo se sustituiría el modelo o proveedor?
- ¿Qué guardarraíles de entrada, contenido y salida aplican?
- ¿Qué se traza y se mide (latencia, coste, errores, feedback)?
- ¿Cómo se evalúa: dataset, métrica y umbral de aceptación?
- ¿Cuál es el comportamiento de fallback?

**Al revisar código**, marca como hallazgo:

- [ ] SDK de proveedor o nombre de modelo acoplado a la lógica de negocio.
- [ ] Texto de usuario que llega al prompt sin validación.
- [ ] Salida del modelo que se usa o se devuelve sin validar.
- [ ] Retrieval mezclado con la llamada al modelo.
- [ ] Llamadas a modelo sin traza, sin latencia o sin registro de coste.
- [ ] Sin ruta de error definida ante timeout o respuesta inválida.
- [ ] Prompts como strings inline sin versionar.
- [ ] Cambio de comportamiento de IA sin un test de regresión o evaluación asociado.
- [ ] Secretos o claves de API en código en vez de variables de entorno.

Ajusta la exigencia a la fase. En un PoC basta con que el diseño no impida cumplir los principios. En producción, todos los MUST deben cumplirse.
