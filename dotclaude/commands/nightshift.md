---
description: Modo nightshift — aplaza lo pesado a una sesión nocturna autónoma (on, off, status, add, run, unlock)
argument-hint: "on | off | status | add <qué hay que ejecutar> | run | unlock"
---

El helper es `~/.claude/nightshift/bin/nightshift`; si no está en el PATH, usa esa ruta. Argumento: `$ARGUMENTS`.

Cómo funciona el modo:

- De día, todo proceso que tarde más de 20 minutos y no necesite interacción humana se encola en vez de ejecutarse. Entran builds y ejecuciones del compose, el e2e, los tests lentos y las conversiones o evaluaciones largas. No cuentan como pesados las rondas de implementación ni los subagentes del ciclo normal.
- A las 23:00, cron lanza una sesión `claude -p` autónoma por cada repo activo que tenga tareas.
- Por la mañana queda un informe en `.claude/nightshift/nights/<fecha>/informe.md`.
- Mientras dura la noche, un cerrojo impide a las demás sesiones escribir en el repo.

Según el primer argumento:

- **`on`**: ejecuta `nightshift on` y confirma al usuario el repo, la cola y la entrada de cron. El modo se queda puesto hasta `off`.
- **`off`**: ejecuta `nightshift off`. La cola se conserva.
- **`status`** (o sin argumento): ejecuta `nightshift status` y resúmelo. Si hay una última noche, ofrece leer su informe.
- **`add <descripción>`**: encola una tarea.
  0. **Antes, combina o descarta.** Lee la cola con `nightshift status` y abre las tareas.
     - Si una ya ejecuta lo mismo o casi (mismo build, mismo e2e, mismo commit o uno que lo contiene), **amplía esa tarea**: añade tu criterio de éxito, tu «Si falla» y tu «después», y anota la sesión que lo pide. No crees otra.
     - Si el resultado ya se conoce (un job de día, un informe nocturno reciente sobre el mismo commit, sin cambios que afecten a lo que mide) y repetirlo no aporta lo suficiente, **no lo encoles**: reutiliza esa evidencia y díselo al usuario.
  1. Ejecuta `nightshift new <slug-corto> --title "<título>"`. Imprime la ruta del fichero nuevo.
  2. Rellena **todas** las secciones de la plantilla con lo que sabes de esta sesión. La sesión nocturna no tendrá más contexto que ese fichero, así que hace falta:
     - directorio de trabajo, rama y commit exactos;
     - dependencias de otras tareas de la cola (`nightshift status` las lista);
     - recursos exclusivos y duración estimada;
     - el contexto mínimo: specs, CA y decisiones ya tomadas;
     - los comandos exactos, con todos los flags y gotchas del entorno;
     - un criterio de éxito verificable;
     - qué hacer si falla;
     - qué acciones quedan autorizadas si sale bien (marcar CA, cerrar spec, commit, push, merge).
  3. Enséñale al usuario un resumen de 3-4 líneas de la tarea.
  4. Sigue con el trabajo del día, dejándolo coherente sin el resultado.
- **`run`**: lanzamiento manual inmediato. Avisa al usuario de que, desde ese momento, esta sesión queda en solo lectura en el repo hasta que termine la noche. Luego lánzalo desacoplado de esta sesión: `setsid nohup ~/.claude/nightshift/bin/nightshift launch >> ~/.claude/nightshift/cron.log 2>&1 < /dev/null &`. Después confirma con `nightshift status`.
- **`unlock`**: ejecuta `nightshift status`. Si el cerrojo es huérfano, `nightshift unlock`. Si la noche sigue viva, no lo fuerces sin que el usuario lo pida expresamente.

**Antes de encolar, mira si puede ir de día en segundo plano.** Hazlo antes de cada `add` y cada vez que el hook bloquee un comando por pesado:

1. Estima la duración con margen. Toma como referencia lo que tardó la última vez (memoria, informes, CLAUDE.md).
2. Comprueba que no choca con nada en marcha: `docker.exe ps`, jobs en segundo plano de esta u otras sesiones (`ListAgents`), `free -g`, y el recurso exclusivo que necesite (Docker, conversión, modelos).
3. Si acaba antes de las 22:45 (`day_cutoff` de `.claude/nightshift.json`) y no choca, lánzalo ya con `run_in_background: true` y `NIGHTSHIFT_ETA_MIN=<minutos>` delante del comando, y sigue trabajando en paralelo. Cuando termine, verifica el resultado tú.
4. Si no cabe o choca, encólalo con `add`.

No esquives el hook de otra forma. Solo si el usuario pide expresamente ejecutarlo ya, antepón `NIGHTSHIFT_BYPASS=1` al comando.
