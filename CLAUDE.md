# Reglas del ramo para esta task

- Este repositorio corresponde a UNA sola task. No mezcles trabajo de otras tasks aquí.
- Al iniciar una sesión, antes de hacer cualquier otra cosa: ejecuta `git fetch --all` y revisa si hay ramas remotas `claude/...` (u `origin/main`) con commits que no estén en tu rama actual. Si las hay, intégralas en tu rama con `git merge`, de la más antigua a la más reciente, y avisa al alumno en una línea que recuperaste su trabajo anterior. Si hay conflictos, conserva la versión más reciente del trabajo, y en `reportes/` conserva todos los archivos. Nunca borres ramas.
- La carpeta `reportes/` se registra y se sube sola. No la borres, no la edites a mano y no la agregues a `.gitignore`.
- Haz commit y push del trabajo del alumno cada vez que completes un avance importante y antes de terminar una sesión.
- Usa Sonnet como modelo por defecto, salvo que el alumno pida otro.
- Cuando el alumno escriba "cerrar task" (o `/cerrar-task`), ejecuta el cierre descrito en `.claude/commands/cerrar-task.md`. No inicies el cierre por otras frases como "listo", "terminé" o "ya está": son parte normal de la conversación. Si el alumno parece haber terminado, puedes recordarle que escriba "cerrar task".
- Nunca guardes contraseñas, claves de API ni datos personales en el repositorio.
