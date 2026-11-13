@echo off
REM Wrapper para el Programador de tareas de Windows.
REM Activa el entorno virtual y ejecuta el agente. No imprime nada sensible.

cd /d "%~dp0\.."
call .venv\Scripts\activate.bat
python scripts\run_task.py
