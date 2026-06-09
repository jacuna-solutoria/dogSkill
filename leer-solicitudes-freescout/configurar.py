#!/usr/bin/env python
"""Configura el acceso a FreeScout para esta skill.

Escribe (o actualiza) un `config.env` JUNTO A ESTE SCRIPT (en el directorio de la
skill). Como la skill es global, al instalarla en
`~/.claude/skills/leer-solicitudes-freescout/` las credenciales quedan ahi y
sirven para cualquier proyecto, sin repetirlas en cada `.env`.

Uso interactivo (recomendado):
    python configurar.py
    # pregunta URL, email, clave (oculta) y la casilla/bandeja a revisar

Uso no interactivo:
    python configurar.py --url https://mesa.ejemplo.com --email user@ejemplo.com \\
                         --password CLAVE --mailbox "SOL Fabrica"

La clave NO se imprime en pantalla.
"""
from __future__ import annotations

import argparse
import sys
from getpass import getpass
from pathlib import Path

CONFIG_NAME = "config.env"
DEFAULT_URL = "https://mesa.solutoria.help"
DEFAULT_MAILBOX = "SOL - Fabrica"
KEYS = ("FREESCOUT_URL", "FREESCOUT_EMAIL", "FREESCOUT_PASSWORD", "FREESCOUT_MAILBOX")


def config_path() -> Path:
    return Path(__file__).resolve().parent / CONFIG_NAME


def read_existing() -> dict[str, str]:
    """Lee el config.env actual. No recorta espacios del valor (las claves pueden
    tenerlos); solo quita el salto de linea."""
    path = config_path()
    data: dict[str, str] = {}
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            if not raw or raw.lstrip().startswith("#") or "=" not in raw:
                continue
            key, _, value = raw.partition("=")
            data[key.strip()] = value
    return data


def write_config(values: dict[str, str]) -> Path:
    path = config_path()
    lines = [
        "# Credenciales de FreeScout para la skill leer-solicitudes-freescout.",
        "# Este archivo NO debe commitearse (ver .gitignore).",
    ]
    lines += [f"{k}={values.get(k, '')}" for k in KEYS]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)  # no-op en Windows
    except (OSError, NotImplementedError):
        pass
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Configura el acceso a FreeScout para esta skill.")
    parser.add_argument("--url", help=f"URL base de FreeScout (por defecto {DEFAULT_URL}).")
    parser.add_argument("--email", help="Correo de acceso a FreeScout.")
    parser.add_argument("--password", help="Clave. Si se omite, se pide por consola (oculta).")
    parser.add_argument("--mailbox", help=f"Casilla/bandeja a revisar (por defecto '{DEFAULT_MAILBOX}').")
    args = parser.parse_args(argv)

    existing = read_existing()

    def ask(key: str, label: str, default: str) -> str:
        current = existing.get(key, default)
        try:
            entered = input(f"{label} [{current}]: ").strip()
        except EOFError:
            entered = ""
        return entered or current

    url = args.url or ask("FREESCOUT_URL", "URL de FreeScout", DEFAULT_URL)
    email = args.email or ask("FREESCOUT_EMAIL", "Email", existing.get("FREESCOUT_EMAIL", ""))

    password = args.password
    if password is None:
        prompt = "Clave"
        if existing.get("FREESCOUT_PASSWORD"):
            prompt += " (Enter para conservar la actual)"
        try:
            password = getpass(prompt + ": ")
        except EOFError:
            password = ""
        if not password:
            password = existing.get("FREESCOUT_PASSWORD", "")

    mailbox = args.mailbox or ask("FREESCOUT_MAILBOX", "Casilla/bandeja", DEFAULT_MAILBOX)

    if not (url and email and password):
        print("Faltan URL, email o clave; no se guardo nada.", file=sys.stderr)
        return 1

    path = write_config({
        "FREESCOUT_URL": url.rstrip("/"),
        "FREESCOUT_EMAIL": email,
        "FREESCOUT_PASSWORD": password,
        "FREESCOUT_MAILBOX": mailbox,
    })
    print(f"Guardado en {path}")
    print(f"  FREESCOUT_URL={url.rstrip('/')}")
    print(f"  FREESCOUT_EMAIL={email}")
    print("  FREESCOUT_PASSWORD=*** (oculto)")
    print(f"  FREESCOUT_MAILBOX={mailbox}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
