---
id: NNNN
title: "Título de la campaña"
status: Draft            # Draft | Active | Paused | Done | Aborted
created: YYYY-MM-DD
updated: YYYY-MM-DD
vision_refs: []          # objetivo(s)/tema(s) de docs/VISION.md que persigue: ["O1", "T1"]
specs: []                # specs en alcance, en orden: ["0002", "0003"]
branch: ""               # rama de trabajo: feature/campaign-<slug>
caps:
  rounds_per_spec: 3     # máximo de rondas implementer↔critic por spec
  max_specs: 1           # v1: una sola spec por campaña
---

# NNNN — Título de la campaña

> Una **campaña** es un loop autónomo acotado que persigue un objetivo de la visión a través de una (v1) o varias (v2) specs, alternando un agente que implementa y otro que critica, hasta cumplir los criterios de "hecho". La orquesta `/campaign`. Este fichero es su **estado durable y auditable**: el orquestador lo lee y escribe entre rondas.

## 1. Directriz

> La intención general. ¿Qué objetivo de `docs/VISION.md` persigue y por qué? 2-4 frases.

_[VERIFICAR] Describe la directriz._

## 2. Criterios de "hecho" (Definition of Done)

> Traducción **comprobable** del objetivo de visión: lo que el crítico debe poder verificar para declarar la campaña terminada. NO prosa vaga. La campaña acaba cuando todos están ✅.

- [ ] DC1 — _[VERIFICAR] criterio verificable_
- [ ] DC2 — _…_

## 3. Specs en alcance

| Orden | Spec | Estado | Notas |
|---|---|---|---|
| 1 | `docs/specs/NNNN-slug.md` | Approved | |

## 4. Log de iteraciones

> **Append-only**. Lo escribe `/campaign` tras cada ronda. NO se edita a mano. Es la memoria del diálogo implementer↔crítico.

| # | Spec | Ronda | Veredicto | VERIFICAR auto-resueltos | Gate | Resumen / feedback |
|---|---|---|---|---|---|---|
| — | | | | | | _(vacío)_ |

## 5. Cola de escalación (pendiente de humano)

> `_[VERIFICAR:humano]_` y bloqueos que requieren tu decisión. **El loop se pausa** mientras haya algo aquí sin resolver. Resuélvelo (edita la spec, responde la pregunta) y relanza `/campaign`.

- [ ] _(vacío)_

## 6. Decisiones registradas (auto-resueltas)

> Resoluciones de `_[VERIFICAR]_` de bajo riesgo que aplicó el loop, con el razonamiento del crítico que las validó. **Auditable**: revísalas en el PR; si alguna no te convence, ajústala como un cambio normal.

- _(vacío)_
