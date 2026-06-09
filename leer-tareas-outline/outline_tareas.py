#!/usr/bin/env python
"""Lee un documento de Outline via `documents.info` y devuelve su contenido.

Pensado para obtener las tareas pendientes acordadas en reuniones desde el
documento "Tareas" del wiki, pero sirve para cualquier documento.

Credenciales: se leen del `config.env` junto a este script (lo crea
`configurar.py`). Tambien pueden venir por variables de entorno
`OUTLINE_API_KEY` / `OUTLINE_URL`, que tienen prioridad sobre el archivo.

Ejemplos:
    # documento de tareas por defecto, markdown completo:
    python outline_tareas.py

    # un documento por id, slug o URL completa:
    python outline_tareas.py https://wikikulvio.conversus.digital/doc/tareas-rxGJ59og3f
    python outline_tareas.py tareas-rxGJ59og3f

    # solo las filas de la tabla que contengan ciertos textos (AND, sin tildes/case):
    python outline_tareas.py --filtrar Jaime --filtrar pendiente

    # la tabla como JSON (lista de filas, cada fila lista de celdas):
    python outline_tareas.py --json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import unicodedata
from pathlib import Path

try:
    import requests
except ImportError:  # el wiki esta tras Cloudflare, que bloquea urllib; requests sí pasa.
    requests = None

CONFIG_NAME = "config.env"
DEFAULT_URL = "https://wikikulvio.conversus.digital"
DEFAULT_DOC = "tareas-rxGJ59og3f"


def load_config() -> dict[str, str]:
    """config.env + variables de entorno (estas ultimas ganan)."""
    cfg: dict[str, str] = {}
    path = Path(__file__).resolve().parent / CONFIG_NAME
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            cfg[key.strip()] = value.strip()
    for key in ("OUTLINE_URL", "OUTLINE_API_KEY"):
        if os.environ.get(key):
            cfg[key] = os.environ[key]
    return cfg


def doc_id_from(value: str) -> str:
    """Acepta un id, un slug o una URL completa y devuelve el id usable.

    Outline resuelve `documents.info` con el slug completo que va tras `/doc/`
    (p. ej. `tareas-rxGJ59og3f`), tal como lo usa la app DogMind.
    """
    value = value.strip()
    if "/doc/" in value:
        value = value.split("/doc/", 1)[1]
    # quita querystring o fragmentos y barras sobrantes
    value = value.split("?", 1)[0].split("#", 1)[0].strip("/")
    return value


def fetch_text(base_url: str, doc_id: str, api_key: str) -> str:
    """Texto markdown de un documento via documents.info.

    Usa `requests`: el wiki esta tras Cloudflare, que bloquea la firma de
    `urllib` con un 403/1010; `requests` la atraviesa (igual que la app DogMind).
    """
    resp = requests.post(
        f"{base_url.rstrip('/')}/api/documents.info",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        },
        json={"id": doc_id},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["data"]["text"]


def _norm(text: str) -> str:
    """minusculas y sin tildes, para comparar de forma tolerante."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower()


def extract_table(markdown: str) -> list[list[str]]:
    """Devuelve las filas de la primera tabla markdown como listas de celdas.

    Incluye la fila de encabezado; descarta la fila separadora (`---`).
    """
    rows: list[list[str]] = []
    in_table = False
    for line in markdown.splitlines():
        stripped = line.strip()
        is_row = stripped.startswith("|")
        if is_row:
            in_table = True
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(set(c) <= {"-", ":", " "} and c for c in cells):
                continue  # fila separadora del encabezado
            rows.append(cells)
        elif in_table:
            break  # la tabla termino
    return rows


def main(argv: list[str] | None = None) -> int:
    # El doc trae tildes y emoji; la consola de Windows (cp1252) los rompe.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Lee un documento de Outline (documents.info).")
    parser.add_argument("doc", nargs="?", default=DEFAULT_DOC, help="id, slug o URL del documento.")
    parser.add_argument("--filtrar", action="append", default=[], metavar="TEXTO",
                        help="conserva filas de la tabla que contengan TEXTO (repetible, AND).")
    parser.add_argument("--json", action="store_true", help="emite la tabla como JSON.")
    args = parser.parse_args(argv)

    if requests is None:
        print(
            "Falta la libreria 'requests' (Cloudflare bloquea urllib en este wiki).\n"
            "Instalala con:  python -m pip install requests",
            file=sys.stderr,
        )
        return 3

    cfg = load_config()
    api_key = cfg.get("OUTLINE_API_KEY")
    base_url = cfg.get("OUTLINE_URL", DEFAULT_URL)
    if not api_key:
        print(
            "Falta la API key de Outline. Configurala con:\n"
            "    python configurar.py\n"
            "o exporta OUTLINE_API_KEY en el entorno.",
            file=sys.stderr,
        )
        return 2

    doc_id = doc_id_from(args.doc)
    try:
        text = fetch_text(base_url, doc_id, api_key)
    except requests.HTTPError as exc:
        code = exc.response.status_code
        hint = {
            401: "token invalido o vencido (revisa la API key con configurar.py).",
            403: "el token no tiene acceso a ese documento (puede ser un API key con scope limitado).",
            404: "documento no encontrado (revisa el id/slug).",
        }.get(code, "")
        print(f"Error HTTP {code} contra Outline. {hint}".strip(), file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"No se pudo conectar a {base_url}: {exc}", file=sys.stderr)
        return 1

    if not args.filtrar and not args.json:
        print(text)
        return 0

    rows = extract_table(text)
    if not rows:
        print("No se encontro una tabla en el documento.", file=sys.stderr)
        print(text)
        return 0

    if args.filtrar:
        needles = [_norm(n) for n in args.filtrar]
        header = rows[0]
        kept = [header]
        for row in rows[1:]:
            joined = _norm(" | ".join(row))
            if all(n in joined for n in needles):
                kept.append(row)
        rows = kept

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print("| " + " | ".join(row) + " |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
