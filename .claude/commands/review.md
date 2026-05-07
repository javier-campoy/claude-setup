---
description: Revisión de los cambios pendientes en la rama actual
allowed-tools: Bash(git status), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Read
argument-hint: "[rama base, por defecto main]"
---

Realiza una revisión de código sobre los cambios pendientes.

1. Determina la rama actual con `git branch --show-current`.
2. Compara contra la rama base ($ARGUMENTS o `main` por defecto): `git diff <base>...HEAD`.
3. Lista los ficheros modificados.
4. Para cada fichero relevante, analiza:
   - **Bugs potenciales** (off-by-one, None handling, race conditions, etc.).
   - **Problemas de seguridad** (inyección, secrets en código, validación de input).
   - **Diseño / mantenibilidad** (funciones demasiado largas, acoplamiento, naming).
   - **Performance** (operaciones N+1, bucles innecesarios).
   - **Tests** (¿hay cobertura del cambio?).
   - **Estilo** (consistencia con el resto del codebase).
5. Si los cambios son grandes (>5 ficheros o >300 líneas), considera invocar al subagente `code-reviewer` para una revisión más profunda.

Formato del reporte:
- **Resumen**: 1-2 frases.
- **Hallazgos**: lista priorizada por severidad (Crítico → Alto → Medio → Bajo → Nit).
- **Recomendaciones concretas**: con fichero:línea cuando sea posible.

NO modifiques código en este comando. Solo reporta.
