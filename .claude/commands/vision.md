---
description: Crea o evoluciona docs/VISION.md, el norte direccional del proyecto
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Bash(git log:*), Bash(date:*)
argument-hint: "<descripción del proyecto o del cambio de dirección> (opcional)"
---

Crea o evoluciona `docs/VISION.md`, el documento que define **hacia dónde va el proyecto y por qué**. Es el norte que specs, sprints y decisiones técnicas toman como referencia. No confundir con `docs/STATE.md` (foto del presente, autogenerada): la visión es prescriptiva, de propiedad humana y evoluciona deliberadamente.

## Detecta el modo

1. Lee `docs/VISION.md` si existe.
   - **No existe, o está esencialmente vacío / plantilla** (sin propósito ni objetivos reales) → modo **CREAR**.
   - **Ya está rellenada** → modo **EVOLUCIONAR**.

## Contexto (siempre)

- Lee `CLAUDE.md` para conocer el proyecto y sus convenciones.
- Lee `docs/STATE.md` (si tiene contenido real) para alinear la visión con lo que ya existe.
- Lee `docs/VISION.md` para conocer su estructura y, en modo EVOLUCIONAR, el estado previo.

## Modo CREAR

1. **Recopila la dirección**:
   - Si `$ARGUMENTS` describe el proyecto, úsalo como base.
   - Si `$ARGUMENTS` está vacío o es insuficiente para rellenar el propósito, los usuarios y al menos un objetivo, **pregunta al usuario** lo mínimo imprescindible (entrevista corta): qué problema resuelve, para quién, cómo se ve el éxito, qué NO va a hacer. No inventes la dirección estratégica.

2. **Rellena `docs/VISION.md`** a partir de lo recopilado, con secciones que cubran al menos: visión y principios de diseño, stack, roadmap/objetivos por fases, no-objetivos, riesgos y próximos pasos.
   - **Marca `_[VERIFICAR]_`** todo lo que no puedas inferir con seguridad. Prefiere preguntar a inventar.
   - Añade en la cabecera una nota de revisión: `> Documento vivo. Última revisión: <fecha> (rev. 1 — creación inicial de la visión).`

3. **Reporta**:
   - Confirma la ruta y un resumen de la visión.
   - Lista los `_[VERIFICAR]_` pendientes de input humano.
   - Recuerda: con la visión rellenada, ya puedes usar `/spec`.

## Modo EVOLUCIONAR

> La visión cambia poco y a propósito. Aquí registras un cambio de dirección, no un refresco mecánico.

1. **Entiende el cambio** que pide `$ARGUMENTS` (nuevo objetivo o fase, un no-objetivo que pasa a objetivo, un principio que se ajusta, una decisión de stack que se cierra, etc.). Si no está claro, pregunta.

2. **Aplica el cambio quirúrgicamente**:
   - Edita solo las secciones afectadas de `docs/VISION.md`. NO reescribas secciones que no cambian.
   - Sé conservador con el contenido humano existente: propón el texto y, si el cambio es grande (cambia el norte, elimina un objetivo, mueve algo de no-objetivos a objetivos), **pide confirmación antes de aplicarlo**.
   - Si una spec o ADR vigente entra en conflicto con el nuevo rumbo, **avísalo** (no lo resuelvas en silencio).

3. **Registra la revisión** (obligatorio):
   - Actualiza la nota de revisión de la cabecera: incrementa el contador `rev. N` y la fecha, y resume **qué cambió y por qué** (esa cabecera funciona como historial breve de la visión).
   - Si el proyecto añade una sección dedicada "Historial de revisiones", añade allí una fila en vez de (o además de) la cabecera. NUNCA borres el histórico previo.

4. **Reporta**: qué secciones cambiaron, la nueva revisión, y si algún spec/ADR queda desalineado.

## Reglas

- **NO inventes la dirección estratégica.** Si falta información crítica, pregunta o marca `_[VERIFICAR]_`.
- **NO toques `docs/STATE.md`** desde aquí (eso es `/state`). La visión y el estado son documentos distintos.
- **NUNCA borres el historial de la visión** (la nota de revisión de la cabecera o la sección de historial). Es la memoria del porqué del norte.
- **El owner humano manda.** Ante cambios grandes de rumbo, propón y espera confirmación; no decidas tú la estrategia.
