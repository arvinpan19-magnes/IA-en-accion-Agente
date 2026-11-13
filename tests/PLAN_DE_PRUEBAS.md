# Plan de pruebas — Agente Banco Central

Metodología Prompt2Agent: el resultado esperado se escribe ANTES de ejecutar
cada prueba. Los casos críticos se repiten 3 veces. Si algo falla, se corrige
donde corresponde y se repite toda la tabla (regresión).

| # | Prueba | Cómo | Resultado esperado | Resultado obtenido | Evidencia | Estado |
|---|---|---|---|---|---|---|
| 1 | Caso normal | `python scripts/run_task.py --no-email` | Imprime asunto y cuerpo del correo con dólar, UF y cobre dentro de rango, y agrega 1 fila nueva a `data/indicadores_banco_central.xlsx` | | | Pendiente |
| 2 | Dos veces el mismo día | Ejecutar `run_task.py --no-email` dos veces seguidas y contar filas del Excel | La segunda ejecución no agrega fila nueva (misma `fecha_valor`); el Excel sigue con la misma cantidad de filas que tras la prueba 1 | | | Pendiente |
| 3 | Sin internet / URL inválida | Copiar `config/config.yaml` a uno temporal con `fuente.url` inválida y ejecutar apuntando a esa copia | `bcentral.obtener_html()` lanza una excepción de red/HTTP; `run_task.py` termina con código distinto de 0, registra el fallo en `state/ultimo_estado.json` (ok=false) y no agrega filas al Excel | | | Pendiente |
| 4 | HTML sin los valores | Llamar a `bcentral.parsear()` con un HTML local que no contenga los `gcode` esperados | Lanza `ValueError` mencionando qué valores faltan (`dolar_observado`, `uf` y/o `cobre`) | | | Pendiente |
| 5 | Valor fuera de rango | Llamar a `bcentral.validar()` con un diccionario de valores con, por ejemplo, `dolar_observado=50000` | Lanza `ValueError` indicando el campo y el rango esperado; no se llega a guardar en Excel | | | Pendiente |
| 6 | Destinatario no permitido | `send_email.send(to="otro@x.cl", subject="x", body="x", config=config)` | Lanza `PermissionError` antes de intentar conectarse a SMTP | | | Pendiente |

## Repetición de casos críticos (mínimo 3 veces)

Casos críticos: 1 (caso normal), 2 (no duplicar) y 6 (destinatario no permitido).

| # | Prueba | Intento | Resultado obtenido | Evidencia | Estado |
|---|---|---|---|---|---|
| 1 | Caso normal | 1 | | | Pendiente |
| 1 | Caso normal | 2 | | | Pendiente |
| 1 | Caso normal | 3 | | | Pendiente |
| 2 | No duplicar | 1 | | | Pendiente |
| 2 | No duplicar | 2 | | | Pendiente |
| 2 | No duplicar | 3 | | | Pendiente |
| 6 | Destinatario no permitido | 1 | | | Pendiente |
| 6 | Destinatario no permitido | 2 | | | Pendiente |
| 6 | Destinatario no permitido | 3 | | | Pendiente |

## Envío real de correo (requiere aprobación del alumno antes de ejecutar)

| # | Prueba | Cómo | Resultado esperado | Resultado obtenido | Evidencia | Estado |
|---|---|---|---|---|---|---|
| 7 | Envío real a correo del alumno | `destinatario` y `destinatarios_permitidos` temporalmente al correo del alumno; `python scripts/run_task.py` | Llega un correo con los 3 valores y el Excel adjunto | | | Pendiente |
| 8 | Envío real a c.becar@udd.cl | Restaurar `destinatario`/`destinatarios_permitidos` a `c.becar@udd.cl`; `python scripts/run_task.py` | Llega un correo con los 3 valores y el Excel adjunto a c.becar@udd.cl | | | Pendiente |

## Alcance validado

_(Completar en el Paso 8, con honestidad: qué funciona, bajo qué condiciones y qué no se probó.)_

- Qué funciona:
- Bajo qué condiciones (SO, cuenta de correo, horario):
- Qué NO se probó:
