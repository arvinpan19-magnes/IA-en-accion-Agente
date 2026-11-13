#!/usr/bin/env bash
# Registro automático de la sesión de Claude Code (app de escritorio y web).
# 1) Copia el registro de la sesión a reportes/sesiones/
# 2) Hace commit SOLO de reportes/ (no toca el trabajo del alumno)
# 3) Lo sube a GitHub en segundo plano
# No requiere instalar nada y nunca interrumpe a Claude: cualquier error se ignora.

entrada=$(cat)

extraer() {
  printf '%s' "$entrada" | tr -d '\n' | sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p"
}

ruta=$(extraer transcript_path)
sesion=$(extraer session_id)

# En Windows la ruta llega como C:\\Users\\... ; la convertimos a C:/Users/...
ruta=$(printf '%s' "$ruta" | sed 's/\\\\/\//g; s/\\/\//g')

dir="${CLAUDE_PROJECT_DIR:-.}"
destino="$dir/reportes/sesiones"
mkdir -p "$destino" 2>/dev/null

if [ -n "$ruta" ] && [ -f "$ruta" ]; then
  cp "$ruta" "$destino/${sesion:-sesion}.jsonl" 2>/dev/null
fi

cd "$dir" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

subir=0
git add reportes >/dev/null 2>&1
if ! git diff --cached --quiet -- reportes 2>/dev/null; then
  git -c user.name="registro-sesion" -c user.email="registro-sesion@users.noreply.github.com" \
    commit -q -m "registro de sesión" -- reportes >/dev/null 2>&1 && subir=1
fi

# También sube si hay commits pendientes o si la rama aún no existe en GitHub
if ! git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
  subir=1
elif [ -n "$(git log '@{u}..' --oneline 2>/dev/null)" ]; then
  subir=1
fi

if [ "$subir" = 1 ]; then
  nohup git push -q origin HEAD >/dev/null 2>&1 &
fi

exit 0
