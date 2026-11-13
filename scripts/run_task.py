"""Orquestador del agente de indicadores del Banco Central.

Uso:
    python scripts/run_task.py             # ejecución real: guarda en Excel y envía correo
    python scripts/run_task.py --no-email  # solo imprime el resultado; no envía nada

Si falla, intenta avisar por correo con asunto "[ALERTA]" (salvo con --no-email,
donde el error se imprime en stderr) y nunca guarda datos dudosos en el Excel.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bcentral  # noqa: E402
import common  # noqa: E402
import send_email  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="No envía ningún correo (ni de alerta); solo imprime el resultado.",
    )
    args = parser.parse_args()

    logger = common.configurar_logging()
    config = common.cargar_config()

    try:
        html = bcentral.obtener_html(config)
        valores = bcentral.parsear(html)
        bcentral.validar(valores, config["rangos_validos"])

        guardado = common.guardar_fila_excel(
            config["excel"]["ruta"],
            config["excel"]["hoja"],
            {
                "fecha_valor": valores["fecha_valor"],
                "dolar_observado_clp": valores["dolar_observado"],
                "uf_clp": valores["uf"],
                "cobre_usd_libra": valores["cobre"],
                "fuente": config["fuente"]["url"],
                "fecha_consulta": datetime.now().isoformat(timespec="seconds"),
            },
        )

        asunto, cuerpo = bcentral.construir_correo(valores, guardado, config)
        logger.info("Obtención exitosa: %s", valores)
        common.guardar_estado(ok=True, detalle="Ejecución correcta", valores=valores)

        if args.no_email:
            print(asunto)
            print(cuerpo)
        else:
            send_email.send(
                to=config["correo"]["destinatario"],
                subject=asunto,
                body=cuerpo,
                config=config,
                attachments=[config["excel"]["ruta"]],
            )
            logger.info("Correo enviado a %s", config["correo"]["destinatario"])
        return 0

    except Exception as error:
        logger.exception("Fallo en la ejecución del agente")
        common.guardar_estado(ok=False, detalle=str(error))
        if args.no_email:
            print(f"[ALERTA] {error}", file=sys.stderr)
        else:
            try:
                send_email.send(
                    to=config["correo"]["destinatario"],
                    subject=config["correo"]["asunto_alerta"],
                    body=f"Falló la obtención de indicadores del Banco Central:\n\n{error}",
                    config=config,
                )
            except Exception:
                logger.exception("No se pudo enviar el correo de alerta")
        return 1


if __name__ == "__main__":
    sys.exit(main())
