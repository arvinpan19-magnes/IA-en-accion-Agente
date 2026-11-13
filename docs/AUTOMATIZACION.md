# Automatización — Programador de tareas de Windows

Horario acordado: **una vez por semana, los lunes a las 21:00, hora de Chile
(America/Santiago)**. Corre en este computador (no en un servidor), así que
solo se ejecuta si el equipo está encendido a esa hora.

## Requisitos antes de programar
1. `config/config.yaml` ya probado con `python scripts/run_task.py --no-email`.
2. `.env` creado (copiado de `.env.example`) con `EMAIL_USER` y
   `EMAIL_PASSWORD` válidos. **Sin `.env` correcto no se programa nada.**
3. Entorno virtual `.venv` creado en la raíz del repo, con
   `pip install -r requirements.txt` ya ejecutado.
4. Verifica la zona horaria de Windows: el Programador de tareas usa la hora
   local del sistema. Si el reloj de Windows no está en "Hora de Santiago",
   el lunes 21:00 programado NO será las 21:00 de Chile.
   - Panel de control → Reloj e idioma → Fecha y hora → confirma "Zona
     horaria: (UTC-04:00) Santiago" (o la que corresponda según horario de
     verano vigente en Chile).

## Paso 1 — Wrapper
Ya existe `scripts/ejecutar_semanal.bat`, que activa `.venv` y ejecuta
`python scripts/run_task.py` desde la raíz del repo.

## Paso 2 — Crear la tarea
### Opción A: Programador de tareas (interfaz gráfica)
1. Abrir "Programador de tareas" (`taskschd.msc`).
2. Acción → Crear tarea básica.
3. Nombre: `Agente Banco Central - semanal`.
4. Desencadenador: Semanalmente → día **lunes** → hora **21:00**.
5. Acción: Iniciar un programa → Programa/script:
   `C:\Users\arvin\repos\IA-en-accion-Agente\scripts\ejecutar_semanal.bat`
   Iniciar en (opcional): `C:\Users\arvin\repos\IA-en-accion-Agente`
6. Finalizar. Edita la tarea creada → pestaña "Condiciones": desmarca
   "Iniciar la tarea solo si el equipo está conectado a la corriente" si vas
   a probarla en un portátil con batería.

### Opción B: línea de comandos (`schtasks`)
```bash
schtasks /Create /SC WEEKLY /D MON /ST 21:00 /TN "Agente Banco Central - semanal" /TR "C:\Users\arvin\repos\IA-en-accion-Agente\scripts\ejecutar_semanal.bat"
```

## Paso 3 — Prueba programada
1. En el Programador de tareas, clic derecho sobre la tarea → "Ejecutar"
   (no hace falta esperar al lunes).
2. Revisar `logs/agente.log` para confirmar que corrió y qué resultado tuvo.
3. Confirmar que llegó (o no) el correo esperado, según si se usó
   `--no-email` o no en el wrapper.

## Notas
- El wrapper no usa `--no-email`: cada ejecución programada envía correo real
  (normal o `[ALERTA]`). Si se quiere una prueba silenciosa, ejecutar
  manualmente `python scripts/run_task.py --no-email` en vez de la tarea.
- Los logs de cada corrida quedan en `logs/agente.log` (no se sube a git).
- El último resultado también queda en `state/ultimo_estado.json` (tampoco se
  sube a git).
