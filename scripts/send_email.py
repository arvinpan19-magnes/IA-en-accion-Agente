"""Envío de correo por SMTP, restringido a los destinatarios permitidos en config.yaml.

El control de a quién se puede escribir vive aquí, fuera del alcance del modelo:
`send()` revisa `correo.destinatarios_permitidos` de config.yaml y rechaza
cualquier otro destinatario con PermissionError, sin intentar enviar nada.
"""
from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Any


def send(
    to: str,
    subject: str,
    body: str,
    config: dict[str, Any],
    attachments: list[str | Path] | None = None,
) -> None:
    permitidos = config["correo"]["destinatarios_permitidos"]
    if to not in permitidos:
        raise PermissionError(
            f"'{to}' no está en destinatarios_permitidos de config.yaml: {permitidos}"
        )

    usuario = os.environ.get("EMAIL_USER")
    clave = os.environ.get("EMAIL_PASSWORD")
    if not usuario or not clave:
        raise RuntimeError(
            "Faltan EMAIL_USER / EMAIL_PASSWORD. Crea un archivo .env (copia .env.example)."
        )

    mensaje = EmailMessage()
    mensaje["Subject"] = subject
    mensaje["From"] = f"{config['correo'].get('remitente_nombre', usuario)} <{usuario}>"
    mensaje["To"] = to
    mensaje.set_content(body)

    for ruta in attachments or []:
        ruta = Path(ruta)
        if not ruta.exists():
            continue
        with open(ruta, "rb") as f:
            datos = f.read()
        mensaje.add_attachment(
            datos,
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=ruta.name,
        )

    smtp_cfg = config["smtp"]
    with smtplib.SMTP(smtp_cfg["servidor"], smtp_cfg["puerto"], timeout=20) as smtp:
        smtp.starttls()
        smtp.login(usuario, clave)
        smtp.send_message(mensaje)
