"""Obtiene y valida el dólar observado, la UF y el cobre desde el Banco Central de Chile.

La página https://si3.bcentral.cl/indicadoressiete/secure/indicadoresdiarios.aspx
entrega estos valores en HTML estático (sin JavaScript): cada indicador vive en un
<li class="list-group-item"> que incluye un enlace "Ver serie" con `gcode=<codigo>`.
Usamos ese código (no el id numérico de la etiqueta) porque es estable aunque el
Banco Central reordene o agregue filas a la tabla.
"""
from __future__ import annotations

import re
from datetime import date
from typing import Any

import requests
from bs4 import BeautifulSoup

GCODE_A_CAMPO = {
    "PRE_TCO": "dolar_observado",
    "UF": "uf",
    "LIBRA_COBRE": "cobre",
}

MESES_ABREVIADOS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def obtener_html(config: dict[str, Any]) -> str:
    fuente = config["fuente"]
    headers = {"User-Agent": fuente.get("user_agent", "Mozilla/5.0")}
    respuesta = requests.get(
        fuente["url"], headers=headers, timeout=fuente.get("timeout_segundos", 20)
    )
    respuesta.raise_for_status()
    return respuesta.text


def parsear(html: str) -> dict[str, Any]:
    """Extrae dolar_observado, uf, cobre y fecha_valor de un HTML de indicadores diarios.

    Lanza ValueError si falta alguno de los tres valores o si no se puede
    interpretar como número.
    """
    soup = BeautifulSoup(html, "lxml")
    valores: dict[str, float] = {}

    for item in soup.find_all("li", class_="list-group-item"):
        enlace = item.find("a", href=re.compile(r"gcode="))
        if not enlace:
            continue
        coincidencia = re.search(r"gcode=([A-Za-z0-9_]+)", enlace["href"])
        if not coincidencia:
            continue
        campo = GCODE_A_CAMPO.get(coincidencia.group(1))
        if not campo:
            continue
        etiqueta_valor = item.find("label", id=re.compile(r"^lblValor"))
        if not etiqueta_valor:
            continue
        valores[campo] = _texto_a_numero(etiqueta_valor.get_text(strip=True))

    faltantes = [campo for campo in GCODE_A_CAMPO.values() if campo not in valores]
    if faltantes:
        raise ValueError(
            "No se encontraron en el HTML los valores: " + ", ".join(faltantes)
        )

    valores["fecha_valor"] = _extraer_fecha(soup)
    return valores


def _texto_a_numero(texto: str) -> float:
    limpio = texto.strip().replace(".", "").replace(",", ".")
    try:
        return float(limpio)
    except ValueError as error:
        raise ValueError(f"No se pudo interpretar el valor numérico: '{texto}'") from error


def _extraer_fecha(soup: BeautifulSoup) -> date | None:
    campo_fecha = soup.find("input", id="txtDate")
    if not campo_fecha or not campo_fecha.get("value"):
        return None
    texto = campo_fecha["value"].strip()  # ej: "13 Nov 2026"
    partes = texto.split()
    if len(partes) != 3:
        return None
    dia_str, mes_str, anio_str = partes
    mes = MESES_ABREVIADOS.get(mes_str[:3].lower())
    if mes is None:
        return None
    try:
        return date(int(anio_str), mes, int(dia_str))
    except ValueError:
        return None


def validar(valores: dict[str, Any], rangos: dict[str, Any]) -> None:
    """Lanza ValueError si algún valor falta o cae fuera del rango configurado."""
    for campo, limites in rangos.items():
        valor = valores.get(campo)
        if valor is None:
            raise ValueError(f"Falta el valor de '{campo}'")
        if not (limites["min"] <= valor <= limites["max"]):
            raise ValueError(
                f"El valor de '{campo}' ({valor}) está fuera del rango esperado "
                f"[{limites['min']}, {limites['max']}] {limites.get('unidad', '')}"
            )


def construir_correo(
    valores: dict[str, Any], guardado: bool, config: dict[str, Any]
) -> tuple[str, str]:
    fecha = valores.get("fecha_valor") or "desconocida"
    asunto = config["correo"]["asunto_normal"].format(fecha=fecha)
    nota_guardado = (
        "Se agregó una fila nueva al Excel de respaldo."
        if guardado
        else "Ya existía una fila para esta fecha; no se duplicó en el Excel."
    )
    cuerpo = (
        f"Indicadores del Banco Central de Chile — fecha del valor: {fecha}\n\n"
        f"Dólar observado: {valores['dolar_observado']:.2f} CLP por USD\n"
        f"UF: {valores['uf']:.2f} CLP\n"
        f"Cobre: {valores['cobre']:.2f} USD por libra\n\n"
        f"Fuente: {config['fuente']['url']}\n"
        f"{nota_guardado}\n"
    )
    return asunto, cuerpo
