---
description: Crea o evoluciona docs/VISION.md, el norte direccional del proyecto
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Bash(git log:*), Bash(date:*)
argument-hint: "<descripción del proyecto o del cambio de dirección> (opcional)"
---

Crea o evoluciona `docs/VISION.md`, el documento que define **hacia dónde va el proyecto y por qué**. Es el norte que specs, sprints y decisiones técnicas toman como referencia. No confundir con `docs/STATE.md` (foto del presente, autogenerada): la visión es prescriptiva, de propiedad humana y evoluciona deliberadamente.

## Detecta el modo

1. Lee `docs/VISION.md` si existe.
   - **No existe, o sigue siendo la plantilla** (secciones con `_[VERIFICAR]_`, frase-norte sin rellenar, metadatos vacíos) → modo **CREAR**.
   - **Ya está rellenada** → modo **EVOLUCIONAR**.

## Contexto (siempre)

- Lee `CLAUDE.md` para conocer el proyecto y sus convenciones.
- Lee `docs/STATE.md` (si tiene contenido real) para alinear la visión con lo que ya existe.
- Lee `docs/VISION.md` para conocer la estructura y, en modo EVOLUCIONAR, el estado previo.

## Modo CREAR

1. **Recopila la dirección**:
   - Si `$ARGUMENTS` describe el proyecto, úsalo como base.
   - Si `$ARGUMENTS` está vacío o es insuficiente para rellenar el propósito, los usuarios y al menos un objetivo, **pregunta al usuario** lo mínimo imprescindible (entrevista corta): qué problema resuelve, para quién, cómo se ve el éxito, qué NO va a hacer. No inventes la dirección estratégica.

2. **Rellena `docs/VISION.md`** sección a sección a partir de lo recopilado:
   - Metadatos: owner (pregunta o deja `_[VERIFICAR]_`), fecha de hoy (`date +%Y-%m-%d`), revisión `v1`, horizonte.
   - 1. Propósito · 2. Visión a futuro (la frase-norte) · 3. Usuarios · 4. Objetivos · 5. No-objetivos · 6. Principios · 7. Métricas · 8. Temas estratégicos · 9. Restricciones · 10. Riesgos.
   - **Marca `_[VERIFICAR]_`** todo lo que no puedas inferir con seguridad. Prefiere preguntar a inventar.
   - Sección 11 (Historial): añade la fila `v1 | <fecha> | <autor> | Creación inicial de la visión.`

3. **Reporta**:
   - Confirma la ruta y un resumen de la frase-norte.
   - Lista los `_[VERIFICAR]_` pendientes de input humano.
   - Recuerda: con la visión rellenada, ya puedes usar `/spec`.

## Modo EVOLUCIONAR

> La visión cambia poco y a propósito. Aquí registras un cambio de dirección, no un refresco mecánico.

1. **Entiende el cambio** que pide `$ARGUMENTS` (nuevo objetivo, un no-objetivo que pasa a objetivo, un tema estratégico nuevo, un principio que se ajusta, etc.). Si no está claro, pregunta.

2. **Aplica el cambio quirúrgicamente**:
   - Edita solo las secciones afectadas. NO reescribas secciones que no cambian.
   - Sé conservador con el contenido humano existente: propón el texto y, si el cambio es grande (cambia el norte, elimina un objetivo, mueve algo de no-objetivos a objetivos), **pide confirmación antes de aplicarlo**.
   - Si una spec o ADR vigente entra en conflicto con el nuevo rumbo, **avísalo** (no lo resuelvas en silencio).

3. **Registra la revisión** (obligatorio):
   - Incrementa `Revisión` en Metadatos (`v2`, `v3`, …) y actualiza `Última actualización`.
   - Añade una fila a la sección 11 (Historial de revisiones) con fecha, autor y **qué cambió y por qué**. NUNCA borres filas anteriores.

4. **Reporta**: qué secciones cambiaron, la nueva revisión, y si algún spec/ADR queda desalineado.

## Reglas

- **NO inventes la dirección estratégica.** Si falta información crítica, pregunta o marca `_[VERIFICAR]_`.
- **NO toques `docs/STATE.md`** desde aquí (eso es `/state`). La visión y el estado son documentos distintos.
- **NUNCA borres el historial de revisiones** (sección 11). Es la memoria del porqué del norte.
- **El owner humano manda.** Ante cambios grandes de rumbo, propón y espera confirmación; no decidas tú la estrategia.
