"""Utilidades compartidas: configuración, logging, Excel y estado."""
from __future__ import annotations

import json
import logging
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from openpyxl import Workbook, load_workbook

RAIZ = Path(__file__).resolve().parent.parent

COLUMNAS_EXCEL = [
    "fecha_valor",
    "dolar_observado_clp",
    "uf_clp",
    "cobre_usd_libra",
    "fuente",
    "fecha_consulta",
]


def cargar_config(ruta: str | Path = "config/config.yaml") -> dict[str, Any]:
    """Carga config.yaml y las variables de entorno de .env (si existe)."""
    load_dotenv(RAIZ / ".env")
    ruta_abs = RAIZ / ruta
    with open(ruta_abs, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def configurar_logging(nombre: str = "bcentral") -> logging.Logger:
    logs_dir = RAIZ / "logs"
    logs_dir.mkdir(exist_ok=True)
    logger = logging.getLogger(nombre)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    formato = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    archivo = logging.FileHandler(logs_dir / "agente.log", encoding="utf-8")
    archivo.setFormatter(formato)
    logger.addHandler(archivo)

    consola = logging.StreamHandler()
    consola.setFormatter(formato)
    logger.addHandler(consola)

    return logger


def _ruta_excel(ruta: str | Path) -> Path:
    ruta_abs = RAIZ / ruta
    ruta_abs.parent.mkdir(parents=True, exist_ok=True)
    return ruta_abs


def _asegurar_libro(ruta_abs: Path, hoja: str) -> Workbook:
    if ruta_abs.exists():
        return load_workbook(ruta_abs)
    wb = Workbook()
    ws = wb.active
    ws.title = hoja
    ws.append(COLUMNAS_EXCEL)
    return wb


def guardar_fila_excel(
    ruta: str | Path, hoja: str, fila: dict[str, Any]
) -> bool:
    """Agrega `fila` al Excel si no existe ya una fila con la misma fecha_valor.

    Devuelve True si se agregó, False si ya existía (no duplica).
    """
    ruta_abs = _ruta_excel(ruta)
    wb = _asegurar_libro(ruta_abs, hoja)
    ws = wb[hoja] if hoja in wb.sheetnames else wb.active

    fecha_valor = str(fila["fecha_valor"])
    for fila_existente in ws.iter_rows(min_row=2, values_only=True):
        if fila_existente and str(fila_existente[0]) == fecha_valor:
            return False

    ws.append([fila.get(col) for col in COLUMNAS_EXCEL])
    wb.save(ruta_abs)
    return True


def _ruta_estado() -> Path:
    estado_dir = RAIZ / "state"
    estado_dir.mkdir(exist_ok=True)
    return estado_dir / "ultimo_estado.json"


def guardar_estado(ok: bool, detalle: str, valores: dict[str, Any] | None = None) -> None:
    datos = {
        "ok": ok,
        "detalle": detalle,
        "valores": valores,
        "marca_tiempo": datetime.now().isoformat(timespec="seconds"),
    }
    with open(_ruta_estado(), "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2, default=str)


def leer_estado() -> dict[str, Any] | None:
    ruta = _ruta_estado()
    if not ruta.exists():
        return None
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)
