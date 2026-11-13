---
description: Método y excepciones para el agente de indicadores del Banco Central (dólar observado, UF, cobre)
---

# Skill: agente de indicadores del Banco Central

## Qué hace
`scripts/run_task.py` obtiene de `https://si3.bcentral.cl/indicadoressiete/secure/indicadoresdiarios.aspx`
el dólar observado (CLP por USD), la UF (CLP) y la libra de cobre (USD por libra),
los valida contra rangos de sanidad (`config/config.yaml: rangos_validos`), los
agrega a `data/indicadores_banco_central.xlsx` (sin duplicar por `fecha_valor`) y
envía un correo con ese Excel adjunto al destinatario configurado.

## Por qué la página se puede scrapear con `requests`
Es HTML estático generado por el servidor (ASP.NET WebForms), no requiere
JavaScript. Cada indicador vive en un `<li class="list-group-item">` que trae
un enlace "Ver serie" con `gcode=<código>` (`PRE_TCO`=dólar, `UF`=UF,
`LIBRA_COBRE`=cobre). `bcentral.parsear()` busca por ese `gcode`, no por el id
numérico de la etiqueta (`lblValor1_3`, etc.), porque el Banco Central puede
reordenar filas y esos números no son estables. Si la página deja de responder
así (403, contenido vacío, el `gcode` ya no aparece), antes de parchear el
parser revisa si cambió el HTML; si requiere JavaScript, usa Playwright; si el
scraping deja de ser viable, considera la API BDE (requiere registro gratuito).

## Fecha del valor
La página trae un campo `<input id="txtDate" value="13 Nov 2026">` con la
fecha a la que corresponden los tres valores mostrados (normalmente el día
hábil vigente). `bcentral._extraer_fecha()` la parsea; si no se encuentra,
`fecha_valor` queda en `None` y la fila se guarda igual, pero sin fecha para
deduplicar (puede revisarse manualmente).

## Reglas de validación
- Si falta cualquiera de los 3 valores, o cae fuera del rango en
  `rangos_validos`, `bcentral.validar()` lanza `ValueError` y **no se guarda
  nada en el Excel ni se marca como éxito**.
- `run_task.py` captura cualquier excepción, registra el fallo en
  `state/ultimo_estado.json` y envía un correo `[ALERTA]` (salvo con
  `--no-email`, donde el error va a stderr).

## Reglas de correo
- `send_email.send()` solo envía a direcciones en
  `config.yaml: correo.destinatarios_permitidos`. Cualquier otra dirección
  lanza `PermissionError` antes de tocar SMTP — este control vive en código,
  no depende del modelo.
- Las credenciales (`EMAIL_USER`, `EMAIL_PASSWORD`) se leen de `.env`, nunca
  del chat ni de config.yaml.

## Excepciones del ramo que aplican aquí
- Nunca cambies `destinatarios_permitidos` o `destinatario` sin aprobación
  explícita del alumno (ver CLAUDE.md e INSTRUCCIONES del task).
- Nunca inventes o "corrijas de memoria" un valor que el parser no pudo leer.
- `reportes/`, `.env`, `logs/` y `state/` no se tocan ni se suben (ver
  `.gitignore` y CLAUDE.md).
- No declares la task terminada con una sola ejecución exitosa: repite el
  plan de pruebas en `tests/PLAN_DE_PRUEBAS.md` al menos 3 veces en los casos
  críticos.
