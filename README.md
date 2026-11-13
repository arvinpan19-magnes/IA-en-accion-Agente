# IA-en-accion-Agente

Agente que cada semana obtiene del Banco Central de Chile el dólar observado,
la UF y el precio del cobre, los respalda en un Excel y los envía por correo.

- Instrucciones del ramo y contrato de la task: ver [CLAUDE.md](CLAUDE.md).
- Método y excepciones del agente: ver
  [.claude/skills/bcentral-indicadores/SKILL.md](.claude/skills/bcentral-indicadores/SKILL.md).
- Automatización semanal (Windows): ver [docs/AUTOMATIZACION.md](docs/AUTOMATIZACION.md).
- Plan y resultados de pruebas: ver [tests/PLAN_DE_PRUEBAS.md](tests/PLAN_DE_PRUEBAS.md).

## Uso rápido

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # y completa EMAIL_USER / EMAIL_PASSWORD ahí, no en el chat
python scripts/run_task.py --no-email   # prueba sin enviar correo
python scripts/run_task.py              # ejecución real
```
