# Dudas de implementación

Una vez por spec implementada, el subagente `spec-implementer` deja aquí `NNNN-slug.md` con todo lo que la spec no resolvía y tuvo que decidir **sin preguntar**: dudas, decisiones no previstas, desviaciones y propuestas que no aplicó (cambios a VISION/STATE que requieren tu visto bueno). Está pensado para trabajar de forma autónoma y revisar **después** de una tanda de implementaciones.

## Cómo revisar una tanda

1. Mira la tabla de abajo y abre primero los documentos con entradas `Alto` o con `Confianza: Baja`.
2. En cada documento, la tabla **Resumen** ordena las entradas; cada una tiene su detalle y un apartado **Si no te convence** con los pasos para cambiarla.
3. Marca cada entrada en su línea `Revisión`: `[x] Aceptada` (no hay nada que hacer), `[x] Cambiar` (pídele a Claude que aplique el «Si no te convence») o `[x] Propuesta aplicada` (para las diferidas que has llevado a VISION/STATE).
4. Cuando todas las entradas del documento estén revisadas, cambia su estado a `Revisado` en la tabla de abajo.

## Qué es cada tipo de entrada

| Tipo | Significa |
|---|---|
| **Duda** | La spec era ambigua; se eligió una lectura. |
| **Decisión no prevista** | La spec no decía nada y hubo que elegir (nombre, valor por defecto, política de error…). |
| **Desviación** | Se hizo algo distinto a lo que dice la spec porque era inviable o contradictorio. Es lo más importante de revisar. |
| **Propuesta diferida** | Cambio a VISION, STATE §5.5, ADR o dependencias que en modo autónomo **no se aplica**; viene con el texto literal listo para aplicar. |
| **Bloqueante** | No se pudo continuar; la implementación está incompleta (el worktree se conserva). |

## Índice

| Spec | Documento | Entradas | Alto / Desviación / Bloqueante | Estado |
|---|---|---|---|---|

> El índice lo actualiza `/implement-spec` (paso 8) al terminar cada spec: una fila por documento. Estados: `Pendiente de revisión` → `Revisado`. En conflicto de merge se conservan ambas filas.
