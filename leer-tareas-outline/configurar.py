#!/usr/bin/env python
"""Configura las credenciales de Outline para esta skill.

Escribe (o actualiza) un archivo `config.env` JUNTO A ESTE SCRIPT, es decir, en
el directorio de la skill. Como la skill es global, al instalarla en
`~/.claude/skills/leer-tareas-outline/` el token queda guardado ahi y sirve para
cualquier proyecto, sin tener que repetirlo en cada `.env`.

Uso interactivo (recomendado):
    python configurar.py
    # pregunta la URL (con valor por defecto) y la API key (no se muestra al teclear)

Uso no interactivo:
    python configurar.py --url https://wikikulvio.conversus.digital --api-key ol_api_xxx

El valor del token NO se imprime en pantalla.
"""
from __future__ import annotations

import argparse
import sys
from getpass import getpass
from pathlib import Path

CONFIG_NAME = "config.env"
DEFAULT_URL = "https://wikikulvio.conversus.digital"


def config_path() -> Path:
    return Path(__file__).resolve().parent / CONFIG_NAME


def read_existing() -> dict[str, str]:
    path = config_path()
    data: dict[str, str] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            data[key.strip()] = value.strip()
    return data


def write_config(url: str, api_key: str) -> Path:
    path = config_path()
    content = (
        "# Credenciales de Outline para la skill leer-tareas-outline.\n"
        "# Este archivo NO debe commitearse (ver .gitignore).\n"
        f"OUTLINE_URL={url}\n"
        f"OUTLINE_API_KEY={api_key}\n"
    )
    path.write_text(content, encoding="utf-8")
    # Permisos restrictivos donde el SO lo permita (no-op en Windows).
    try:
        path.chmod(0o600)
    except (OSError, NotImplementedError):
        pass
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Configura el acceso a Outline para esta skill.")
    parser.add_argument("--url", help=f"URL base de Outline (por defecto {DEFAULT_URL}).")
    parser.add_argument("--api-key", help="API key de Outline. Si se omite, se pide por consola.")
    args = parser.parse_args(argv)

    existing = read_existing()

    url = args.url
    if not url:
        default_url = existing.get("OUTLINE_URL", DEFAULT_URL)
        try:
            entered = input(f"URL de Outline [{default_url}]: ").strip()
        except EOFError:
            entered = ""
        url = entered or default_url

    api_key = args.api_key
    if not api_key:
        prompt = "API key de Outline"
        if existing.get("OUTLINE_API_KEY"):
            prompt += " (Enter para conservar la actual)"
        try:
            api_key = getpass(prompt + ": ").strip()
        except EOFError:
            api_key = ""
        if not api_key:
            api_key = existing.get("OUTLINE_API_KEY", "")

    if not api_key:
        print("No se entrego una API key; no se guardo nada.", file=sys.stderr)
        return 1

    path = write_config(url, api_key)
    print(f"Guardado en {path}")
    print(f"  OUTLINE_URL={url}")
    print("  OUTLINE_API_KEY=*** (oculto)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
