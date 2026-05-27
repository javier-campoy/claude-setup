# Visión del proyecto

> **El norte del proyecto.** Este documento define *hacia dónde vamos y por qué*. Es el nexo que specs, sprints y decisiones técnicas toman como referencia: cualquier cambio significativo debe poder justificarse contra esta visión.
>
> **Cómo se relaciona con `STATE.md`**: son complementarios y NO se solapan.
> - `VISION.md` (este fichero) → **dirección a futuro**. Prescriptivo, de propiedad humana, estable. Responde *"¿a dónde vamos?"*.
> - [`STATE.md`](STATE.md) → **foto del presente**. Descriptivo, regenerado por Claude tras cada cambio en `src/`, volátil. Responde *"¿dónde estamos ahora?"*.
>
> **Es un documento vivo, pero NO automático.** Evoluciona deliberadamente conforme aprendemos: lo edita una persona (o Claude vía `/vision`, con confirmación), nunca `/state`. Cada cambio relevante de dirección queda registrado en la sección 11 (Historial de revisiones).
>
> **Construye esta visión ANTES de redactar tu primera spec.** El flujo `/spec` la exige rellenada. Si sigue siendo la plantilla, créala con `/vision "describe tu proyecto"`.

---

## Metadatos

| Campo | Valor |
|---|---|
| **Owner** | _(persona responsable de la visión)_ |
| **Última actualización** | _(YYYY-MM-DD)_ |
| **Revisión** | _(v1, v2, … — coincide con la última entrada de la sección 11)_ |
| **Horizonte** | _(p.ej. próximos 6-12 meses)_ |

---

## 1. Propósito

> 2-4 frases. ¿Qué problema resolvemos y por qué importa? Si alguien lee solo este apartado debería entender la razón de existir del proyecto.

_[VERIFICAR] Describe el problema central que justifica el proyecto._

---

## 2. Visión a futuro (el norte)

> Una sola frase que capture el estado ideal al que aspiramos. Debe ser ambiciosa pero reconocible. Es la brújula que usarás cuando dudes entre dos caminos.

> **Ejemplo**: _"Que cualquier desarrollador Python pueda parsear y validar configuración compleja sin escribir una sola línea de boilerplate."_

_[VERIFICAR] Escribe aquí la frase-norte del proyecto._

---

## 3. Usuarios y necesidades

> ¿Para quién es esto? ¿Qué necesitan y qué les duele hoy? Sé concreto: un usuario bien definido vale más que "todo el mundo".

| Usuario / perfil | Qué necesita | Qué le duele hoy |
|---|---|---|
| _[VERIFICAR]_ | | |

---

## 4. Objetivos

> Qué queremos lograr (resultados, no tareas). Cada objetivo debería ser comprobable. Las specs y los sprints existen para mover estos objetivos.

- [ ] **O1** — _[VERIFICAR] objetivo medible_
- [ ] **O2** — _…_
- [ ] **O3** — _…_

---

## 5. No-objetivos (fuera de alcance)

> Tan importante como lo que haremos: lo que deliberadamente **NO** haremos. Define los bordes del norte y evita el scope creep. Una spec que cae aquí se rechaza.

- _[VERIFICAR] qué decidimos NO hacer y por qué_

---

## 6. Principios rectores

> Los criterios con los que tomamos decisiones cuando hay tensión. Guían los trade-offs de cada spec. Ejemplos: "simplicidad sobre completitud", "sin dependencias pesadas", "la API pública es sagrada".

1. _[VERIFICAR] principio 1_
2. _…_
3. _…_

---

## 7. Métricas de éxito

> ¿Cómo sabremos que avanzamos hacia el norte? Señales observables, no opiniones. Si no se puede medir, descríbelo como una señal cualitativa clara.

| Métrica / señal | Estado actual | Objetivo |
|---|---|---|
| _[VERIFICAR]_ | | |

---

## 8. Temas estratégicos

> Los grandes pilares de trabajo que agrupan specs y sprints. Cada tema es un "epic" de alto nivel; cada spec debería poder colgar de un tema. Esta es la tabla que conecta la visión con el trabajo concreto del día a día.

| ID tema | Tema | Objetivo que mueve | Estado | Specs asociadas |
|---|---|---|---|---|
| T1 | _[VERIFICAR]_ | O1 | Por empezar / En curso / Hecho | _(NNNN, …)_ |

---

## 9. Restricciones y supuestos

> Límites con los que jugamos (técnicos, de negocio, de tiempo, de equipo) y supuestos que damos por buenos hasta que se demuestre lo contrario.

- **Restricciones**: _[VERIFICAR]_
- **Supuestos**: _[VERIFICAR]_

---

## 10. Riesgos estratégicos

> Lo que podría desviarnos del norte. A nivel de proyecto, no de implementación (esos van en cada spec).

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| _[VERIFICAR]_ | Baja/Media/Alta | Bajo/Medio/Alto | _(plan)_ |

---

## 11. Historial de revisiones

> El registro de cómo ha evolucionado la dirección del proyecto. Cada cambio relevante de la visión añade una fila (lo hace `/vision` o tú a mano). **Nunca se borran filas**: son la memoria de por qué el norte es como es hoy.

| Revisión | Fecha | Autor | Qué cambió y por qué |
|---|---|---|---|
| v1 | _(YYYY-MM-DD)_ | _(autor)_ | Creación inicial de la visión. |

---

## 12. Directrices estratégicas e inventarios de specs

> Tres subsecciones que cierran el flujo spec-driven con la visión:
> - **§12.1** codifica el **norte no-negociable** como reglas citables `DV-NN`. Solo se editan con `/vision`.
> - **§12.2** mantiene el **inventario de specs creadas** con `/spec` (auto-añadido por el comando con confirmación humana).
> - **§12.3** mantiene el **backlog de ideas para futuras specs** (auto-extraídas por `/spec` y `/implement-spec` con confirmación humana).
>
> Para entender el sistema completo (cómo se entrelazan con las **directrices tácticas** `D-NN` de [`STATE.md`](STATE.md) §5.5), lee `CLAUDE.md` sección "Documentación viva".

### 12.1 Directrices estratégicas vigentes

> Son **reglas de norte** que toda spec del proyecto debe respetar mientras estén vigentes. Distintas de las directrices tácticas de [`STATE.md`](STATE.md) §5.5 (arquitectura, calidad, producto y backlog concreto): las estratégicas codifican lo **no-negociable** del producto y solo se editan con `/vision`. Cada una tiene ID citable `DV-NN`. Las specs declaran en su frontmatter (`directives_followed`) qué `DV-NN` honran.
>
> **Cómo rellenarla**: extrae directrices estratégicas de los principios (§6), no-objetivos (§5) y restricciones (§9) ya definidos. Empieza con 3-5 directrices que codifiquen lo realmente no-negociable; ampliar después.

| ID | Origen | Directriz | Estado |
|---|---|---|---|
| _(vacío — añade tus primeras directrices estratégicas tras tener objetivos y principios estables)_ | | | |

### 12.2 Ideas de specs registradas

> Inventario de specs creadas con `/spec`. Lo mantiene **automáticamente** el comando con confirmación humana (paso 7.5 de `/spec`). Cada entrada se actualiza a `Implemented` cuando `/implement-spec` cierra la spec (paso 7f, confirmación humana). La sección **se rellena hacia adelante** — no se reescriben entradas pasadas, quedan como histórico.
>
> Formato canónico de cada entrada:
> ```
> - **NNNN — `<slug>`** _(estado: Draft|Approved|Implemented, registrado: YYYY-MM-DD)_ — `<resumen 1 línea desde la sección 1 de la spec>`. Avanza: `<lista de vision_refs>`. _Implementada en: <hash>|pendiente._
> ```

- _(vacío — primera entrada se añadirá con la próxima spec creada vía `/spec` tras la convención)_

### 12.3 Ideas para futuras specs (sin spec asociada todavía)

> Backlog vivo de ideas que **emergen durante el flujo spec-driven** y aún no son spec. Las extraen automáticamente:
> - `/spec` paso 7.6 — escanea las secciones 4 (Alternativas consideradas), 7 (Compatibilidad y migración), 8 (Riesgos y mitigaciones) y 9 (Notas y enlaces) de la spec recién creada buscando menciones tipo "se difiere a spec futura", "queda como spec candidata", "post-implementación".
> - `/implement-spec` paso 7c.bis — escanea la sección 10 (Decisiones durante la implementación) de la spec implementada buscando menciones equivalentes.
>
> Ambos comandos **proponen** las ideas con confirmación humana; **nunca** inventan ideas que no estén en la spec. Cuando una idea se consolida en una spec real, `/spec` la marca `consolidada en NNNN-<slug>` con confirmación. **Nunca se borran** — quedan como histórico.
>
> Formato canónico de cada entrada:
> ```
> - **`<slug-tentativo>`** _(propuesta por spec NNNN el YYYY-MM-DD)_ — `<motivación 1 línea>`. Estado: propuesta | consolidada en NNNN-<slug>.
> ```

- _(vacío — se rellena cuando alguna spec mencione trabajo diferido a futuras specs)_
