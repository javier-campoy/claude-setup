---
description: Coordina una ronda de implementación de varias specs aprobadas, con ruta previa y paralelismo donde sea posible
model: opus
allowed-tools: Read, Edit, Write, Glob, Grep, Agent, SendMessage, ListAgents, ToolSearch, Bash(uv run:*), Bash(uv sync:*), Bash(git diff:*), Bash(git status), Bash(git log:*), Bash(git rev-parse:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git fetch:*), Bash(git checkout:*), Bash(git pull:*), Bash(git merge:*), Bash(git branch:*), Bash(git worktree:*), Bash(git -C:*), Bash(git ls-remote:*), Bash(cd:*), Bash(cp:*), Bash(docker:*), Bash(docker.exe:*), Bash(glab api:*), Bash(date:*)
argument-hint: "[NNNN ...] [--plan-only] [--auto] [--max-parallel N]"
---

Coordina una ronda de implementación de specs según $ARGUMENTS. Eres el **coordinador** (Opus): decides la ruta, lanzas a los subagentes `spec-implementer` (Sonnet), compruebas lo que devuelven e integras en `develop`. No implementas el código de las specs tú mismo.

`/implement-spec` sigue siendo la referencia del flujo de cada spec: este comando no lo duplica, solo dice qué paso se hace cuándo y quién lo hace.

## Argumentos

- `NNNN ...`: specs de la ronda. Sin números, todas las de `status: Approved`.
- `--plan-only`: traza la ruta, la muestra y termina. No crea worktrees ni escribe nada.
- `--auto`: no espera a que se apruebe la ruta.
- `--max-parallel N`: máximo de implementadores a la vez (por defecto, 3).

## 1. Comprobaciones previas

Para y explica el motivo si algo falla:

- El proyecto tiene `/implement-spec` y el subagente `spec-implementer`, y usa el flujo spec-driven (`docs/specs/`, `docs/dudas/`). Si no, explícalo y para.
- La rama es `develop`, sin cambios *tracked* y sincronizada con `origin/develop`. La última CI de `develop` está en verde (con `glab api`). Si no puedes leerla, dilo y sigue.
- `ListAgents` no muestra otra sesión en esta copia: los hooks de `pre-commit` hacen stash y pisan ediciones ajenas.
- Cada spec cumple el paso 1 de `/implement-spec`: `Approved`, sin marcadores de verificación y sin veredicto `RETHINK`. Una spec no trivial sin revisión no bloquea, pero se anota como riesgo en la ruta.
- No existe `.claude/worktrees/NNNN` ni `feat/NNNN-*` para ninguna spec de la ronda, salvo que estés reanudando (sección 7).

## 2. Trazar la ruta

Lee de cada spec el frontmatter (`related`), §3, §5, §6 y §7. Para cada par de specs clasifica lo que las une:

| Relación | Ejemplos | Consecuencia |
|---|---|---|
| **Dependencia** | Usa una regla, API o fichero que crea la otra; §7 dice «depende de» | Orden estricto: olas distintas |
| **Mismo código** | Ambas modifican el mismo módulo de `src/`, el mismo fixture o `corpus.toml` | Olas distintas, salvo que sean adiciones en zonas claramente separadas |
| **Medición encadenada** | Un CA compara con el resultado de la otra («no cambia de veredicto respecto a…»), o una usa el corpus que crea la otra | Olas distintas, en el orden que dé sentido a la medición |
| **Recurso exclusivo** | Ambas necesitan el mismo entorno único: `docker compose` con puertos fijos, un e2e, una base compartida | Misma ola, con turnos (sección 4) |
| **Solo docs vivas** | `STATE.md`, `changelog.md`, `docs/specs/README.md`, `docs/dudas/README.md` | Misma ola; las resuelves tú al integrar |

Agrupa en olas: dos specs comparten ola solo si entre ellas no hay ninguna de las tres primeras relaciones. Ninguna ola supera `--max-parallel`. Si dudas sobre una relación, sepáralas: una ola de más cuesta tiempo, y un conflicto de código o una medición falsa cuestan más. No fuerces paralelismo para aprovechar el máximo.

Muestra la ruta:

| Ola | Specs en paralelo | Turnos del recurso exclusivo | Por qué van aquí |
|---|---|---|---|

Añade debajo qué pares se separaron y por qué, los riesgos y las decisiones humanas que quedarán al final.

- Con `--plan-only`, termina aquí.
- Sin `--auto`, espera la confirmación. Si el usuario cambia la ruta, respétala.

## 3. Registro de la ronda

Crea `docs/dudas/ronda-AAAA-MM-DD.md` con la ruta y una tabla de estado por spec. Actualízala en cada cambio de estado: es lo que permite reanudar si se pierde el contexto. No la commitees hasta el cierre (sin *stage*, no le afecta el stash de los hooks).

Estados: `pendiente` → `implementando` → `esperando turno` → `verificada` → `integrada`. Finales: `integrada parcial`, `bloqueada`, `saltada`.

## 4. Ejecutar cada ola

**a. Worktrees.** Espera a que la ola anterior esté integrada y empujada. Para cada spec, sigue el paso 3.5 de `/implement-spec`, partiendo de `origin/develop` actualizado.

**b. Implementadores.** Lanza un subagente `spec-implementer` por spec, en segundo plano y en un único mensaje. No uses `isolation`: el worktree ya existe. El prompt incluye la ruta absoluta del worktree, la ruta de la spec, `Modo ronda` y las notas de las specs ya integradas que le afecten (APIs creadas, cambios de `expected`). Mientras trabajan no hagas polling: te llega una notificación al acabar cada uno.

**c. Turnos del recurso exclusivo.** Si el proyecto tiene un entorno único, solo una spec lo usa a la vez. Lo más habitual es `docker compose`, con `docker` o `docker.exe` según el entorno y los perfiles y opciones de construcción que indiquen `CLAUDE.md` y la spec. Cuando un implementador devuelva pasos en `PENDIENTE_EXCLUSIVO`, ponlo en cola y, en su turno:

1. Desde el worktree: copia el `.env` de la copia principal si falta (está ignorado por git), `compose down` y `compose up -d --build --wait`.
2. Retoma al mismo implementador con `SendMessage` y dile que ya tiene el turno. Si el identificador ya no sirve, lanza uno nuevo sobre ese worktree.
3. Al acabar, **antes de pasar el turno**: `compose down` desde el worktree y, si no hay más turnos, `compose up -d --wait` desde la copia principal.

Reglas de los turnos:

- **Una spec con migración** de una base compartida va la última de su ola. Si no, las demás arrancan con un esquema por delante de su código. Levanta el entorno desde la copia principal solo después de integrarla.
- **Nunca borres un worktree con el compose apuntando a él**: Docker recrea sus rutas de montaje como directorios de `root`. Esos contenedores no vuelven a arrancar bien y el directorio solo se puede borrar con `sudo`.

**d. Verificación.** No te fíes solo del informe. Para cada spec terminada:

- Revisa `git -C <worktree> status` y `diff --stat`: nada fuera del alcance de la spec.
- Lee `docs/dudas/NNNN-slug.md`.
- Comprueba que los CA marcados tienen evidencia, sobre todo las mediciones: deben estar en la sección 10.
- Si falta algo arreglable dentro de la spec, devuélvelo al implementador con `SendMessage`, con instrucciones concretas. Dos veces como mucho: después pasa a `bloqueada`.

Clasifica el resultado:

| Resultado | Condición | Qué haces |
|---|---|---|
| **Completa** | Todos los CA cumplidos | Pasos 5 a 9 de `/implement-spec` |
| **Parcial** | Gate en verde; lo que falta depende de una persona, de un tercero o de un corpus que no está | Integra con `status: Approved`, sin `implemented_in`, y anota qué falta |
| **Bloqueada** | Hay `Bloqueante` o el gate no pasa | No integres; conserva worktree y rama |

**e. Integración, de una en una.** Sigue los pasos 5 a 9 de `/implement-spec` en modo `--auto`: los cierres de VISION, las directrices nuevas y los ADR quedan como `Propuesta diferida` en `docs/dudas/`. El orden dentro de la ola es el de menor riesgo primero. Reglas añadidas:

- Conflictos en docs vivas: conserva ambos lados.
- Conflictos de código: `git merge --abort`. Si son adiciones independientes, repite el merge, resuélvelo conservando ambas y anótalo en las dudas de la spec. Si dudas del resultado o el gate falla, déjala `bloqueada`.
- El gate tras el merge es obligatorio aunque la spec pasara en su worktree: es lo único que comprueba la combinación de la ola.
- No hagas `/state`: regeneraría `STATE.md` y mezclaría las specs en curso.

**f. Fin de ola.** Con todo empujado, espera a la CI del último commit, con un bucle en segundo plano. Si falla, para la ronda y arregla o informa antes de abrir la siguiente ola.

## 5. Si algo se tuerce

- **Spec bloqueada**: las que dependan de ella pasan a `saltada`. El resto de la ronda sigue. Replantea la ruta solo si cambian las dependencias.
- **La misma causa en dos specs**: para la ola. Probablemente la ruta o `develop` estén mal, no las specs.
- **La spec contradice VISION, un ADR o una directriz**: no lo resuelvas tú; anótalo y deja la spec `bloqueada`.
- **Nunca** uses `--no-verify`, `git push --force`, `git reset --hard` ni `git stash`, ni borres un worktree con trabajo sin integrar.

## 6. Cierre

1. Si hay un recurso exclusivo, déjalo levantado desde la copia principal. Comprueba que `git worktree list` solo muestra lo esperado.
2. Pasa `uv run python .claude/hooks/check_spec_state_sync.py`.
3. Actualiza `docs/STATE.md` §7 y, si existe, `docs/roadmap-specs.md`.
4. Añade la ronda al índice de `docs/dudas/README.md` y haz commit en `develop` del registro y de estos cambios, con `docs: cerrar la ronda de specs <lista>`. Haz push y espera a la CI.
5. Informa al usuario:
   - Una tabla por spec: estado final, merge, CA abiertos y dudas de impacto `Alto`, `Desviación` o `Bloqueante`.
   - Qué ramas o worktrees siguen vivos y por qué.
   - Qué le toca a él: revisar `docs/dudas/`, aplicar las propuestas diferidas y lo que quedó parcial.

No integres en `main` ni publiques.

## 7. Reanudar

Si al empezar hay un `docs/dudas/ronda-*.md` sin cerrar, léelo y contrástalo con `git worktree list`, `git branch` y el frontmatter de las specs. Lo que digan git y las specs manda sobre el registro. Las specs `implementando` con cambios sin commitear se retoman sobre su worktree; no empieces de cero. Si no está claro qué pasó, pregunta antes de tocar nada.
