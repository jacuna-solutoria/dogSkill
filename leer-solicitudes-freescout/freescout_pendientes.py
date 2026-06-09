#!/usr/bin/env python
"""Lee por scraping las solicitudes PENDIENTES de una casilla de FreeScout.

Solo lectura: inicia sesion, entra a la casilla configurada (por defecto
"SOL Fabrica"), recorre sus carpetas activas (No asignado / Propio / Asignado),
y lista las conversaciones pendientes. No escribe nada en FreeScout ni en ningun
otro sistema; no descarga adjuntos.

Replica los selectores HTML que usa la app DogMind (probados contra esa instancia
de FreeScout). Si FreeScout cambia su markup, hay que ajustar los selectores.

Credenciales: se leen del `config.env` junto a este script (lo crea
`configurar.py`). Tambien pueden venir por variables de entorno
`FREESCOUT_URL` / `FREESCOUT_EMAIL` / `FREESCOUT_PASSWORD` / `FREESCOUT_MAILBOX`,
que tienen prioridad sobre el archivo.

Ejemplos:
    python freescout_pendientes.py                 # tabla de pendientes de la casilla
    python freescout_pendientes.py --json          # salida JSON (para procesar)
    python freescout_pendientes.py --mailbox "Otra Casilla"
    python freescout_pendientes.py --detalle        # incluye una descripcion corta por ticket
    python freescout_pendientes.py --limit 20
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None  # type: ignore
    BeautifulSoup = None  # type: ignore

CONFIG_NAME = "config.env"
DEFAULT_URL = "https://mesa.solutoria.help"
DEFAULT_MAILBOX = "SOL - Fabrica"
# Carpetas que cuentan como "pendientes" (no cerradas). Igual que DogMind.
PENDING_FOLDERS = ["No asignado", "Propio", "Asignado"]

CONV_HREF_RE = re.compile(r"/conversation/(\d+)")
NUMBER_RE = re.compile(r"#?\s*(\d{2,})")


# --- configuracion --------------------------------------------------------

def load_config() -> dict[str, str]:
    """config.env + variables de entorno (estas ultimas ganan). No recorta los
    valores (la clave puede tener espacios), solo quita el salto de linea."""
    cfg: dict[str, str] = {}
    path = Path(__file__).resolve().parent / CONFIG_NAME
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            if not raw or raw.lstrip().startswith("#") or "=" not in raw:
                continue
            key, _, value = raw.partition("=")
            cfg[key.strip()] = value
    for key in ("FREESCOUT_URL", "FREESCOUT_EMAIL", "FREESCOUT_PASSWORD", "FREESCOUT_MAILBOX"):
        if os.environ.get(key):
            cfg[key] = os.environ[key]
    return cfg


def _norm(text: str) -> str:
    """minusculas y sin tildes, para comparar nombres de forma tolerante."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower().strip()


def _alnum(text: str) -> str:
    """Solo letras/numeros, sin tildes ni puntuacion: 'SOL - Fabrica' -> 'solfabrica'.
    Asi el nombre de casilla calza aunque difieran guiones/espacios."""
    return re.sub(r"[^a-z0-9]", "", _norm(text))


def _normalize_folder(name: str) -> str:
    """Quita el contador final ('Asignado 13' -> 'asignado') y normaliza."""
    return _norm(re.sub(r"\s*\d+$", "", name or ""))


# --- FreeScout: login y navegacion ---------------------------------------

def login(session, base_url: str, email: str, password: str) -> None:
    """Inicia sesion en FreeScout (Laravel: token CSRF _token + cookies)."""
    r = session.get(urljoin(base_url + "/", "login"), timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    token_el = soup.find("input", attrs={"name": "_token"})
    data = {"email": email, "password": password}
    if token_el and token_el.has_attr("value"):
        data["_token"] = token_el["value"]
    r = session.post(urljoin(base_url + "/", "login"), data=data, timeout=30)
    r.raise_for_status()
    if BeautifulSoup(r.text, "html.parser").find("input", attrs={"name": "password"}):
        raise SystemExit("Login fallido: revisa email/clave (corre configurar.py).")


def find_mailbox(session, base_url: str, wanted_name: str) -> tuple[str, str]:
    """Devuelve (id, nombre) de la casilla cuyo nombre calza con wanted_name
    (comparacion tolerante a mayusculas/tildes; acepta coincidencia parcial)."""
    r = session.get(base_url + "/", timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    mailboxes: dict[str, str] = {}
    for a in soup.find_all("a", href=re.compile(r"/mailbox/\d+")):
        m = re.search(r"/mailbox/(\d+)", a["href"])
        name = a.get_text(" ", strip=True)
        if m and name and m.group(1) not in mailboxes:
            mailboxes[m.group(1)] = name
    if not mailboxes:
        raise SystemExit("No se encontraron casillas en el panel (revisa los selectores).")

    target = _alnum(wanted_name)
    for mid, name in mailboxes.items():  # calce exacto (sin puntuacion/tildes)
        if _alnum(name) == target:
            return mid, name
    for mid, name in mailboxes.items():  # coincidencia parcial de respaldo
        if target and target in _alnum(name):
            return mid, name
    disponibles = ", ".join(sorted(mailboxes.values()))
    raise SystemExit(f"No encontre la casilla '{wanted_name}'. Disponibles: {disponibles}")


def active_folders(session, base_url: str, mailbox_id: str,
                   wanted: list[str]) -> list[tuple[str, str]]:
    """Devuelve [(nombre, url)] de las carpetas de la casilla en `wanted`."""
    r = session.get(f"{base_url}/mailbox/{mailbox_id}", timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    wanted_norm = {_normalize_folder(w) for w in wanted}
    folders: dict[str, str] = {}
    for a in soup.find_all("a", href=re.compile(rf"/mailbox/{mailbox_id}/-?\d+")):
        m = re.search(rf"/mailbox/{mailbox_id}/(-?\d+)", a["href"])
        name = a.get_text(" ", strip=True)
        if not m or not name:
            continue
        if _normalize_folder(name) in wanted_norm:
            folders.setdefault(m.group(1), name)
    return [(name, f"{base_url}/mailbox/{mailbox_id}/{fid}") for fid, name in folders.items()]


# --- FreeScout: parseo de conversaciones ----------------------------------

def parse_conversation_rows(html: str, base_url: str) -> list[dict]:
    """Extrae las conversaciones de una pagina de carpeta (markup de FreeScout:
    tr[data-conversation_id], td.conv-subject, td.conv-number, td.conv-customer)."""
    soup = BeautifulSoup(html, "html.parser")
    out: list[dict] = []
    for row in soup.find_all("tr", attrs={"data-conversation_id": True}):
        conv_id = row["data-conversation_id"]
        subj_td = row.find("td", class_="conv-subject")
        link = (subj_td.find("a", href=CONV_HREF_RE) if subj_td
                else row.find("a", href=CONV_HREF_RE))
        href = link["href"] if link else f"{base_url}/conversation/{conv_id}"

        tags: list[str] = []
        subject = "(sin asunto)"
        if subj_td:
            tags = [t.get_text(" ", strip=True) for t in subj_td.select(".conv-tags .tag")
                    if t.get_text(strip=True)]
            p = subj_td.find("p")
            if p:
                for tg in p.select(".conv-tags"):
                    tg.extract()
                subject = p.get_text(" ", strip=True) or subject

        num_td = row.find("td", class_="conv-number")
        m = NUMBER_RE.search(num_td.get_text()) if num_td else None
        number = m.group(1) if m else conv_id

        customer = ""
        cust_td = row.find("td", class_="conv-customer")
        if cust_td:
            node = cust_td.find("a") or cust_td
            for sub in node.select(".conv-owner-mobile, .conv-email"):
                sub.extract()
            customer = node.get_text(" ", strip=True)

        out.append({
            "number": str(number),
            "subject": subject,
            "customer": customer,
            "tags": tags,
            "url": urljoin(base_url, href),
        })
    return out


def collect(session, base_url: str, folders: list[tuple[str, str]],
            max_pages: int = 10) -> list[dict]:
    """Recolecta las conversaciones de las carpetas, deduplicando por numero."""
    seen: dict[str, dict] = {}
    for fname, furl in folders:
        for page in range(1, max_pages + 1):
            sep = "&" if "?" in furl else "?"
            r = session.get(f"{furl}{sep}page={page}", timeout=30)
            if r.status_code != 200:
                break
            rows = parse_conversation_rows(r.text, base_url)
            if not rows:
                break
            new = 0
            for row in rows:
                if row["number"] not in seen:
                    row["folder"] = fname
                    seen[row["number"]] = row
                    new += 1
            if new == 0:
                break
    return list(seen.values())


def fetch_descripcion(session, url: str, max_chars: int = 240) -> str:
    """Descripcion corta del mensaje original del ticket (solo lectura, 1 GET)."""
    try:
        r = session.get(url, timeout=30)
        r.raise_for_status()
    except requests.RequestException:
        return ""
    soup = BeautifulSoup(r.text, "html.parser")
    bodies = (soup.select(".thread-content") or soup.select(".thread-body")
              or soup.select(".body"))
    if not bodies:
        return ""
    text = bodies[-1].get_text(" ", strip=True)
    return (text[:max_chars] + "...") if len(text) > max_chars else text


# --- principal ------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # consola Windows (cp1252) rompe tildes
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Lista las solicitudes pendientes de una casilla de FreeScout.")
    parser.add_argument("--mailbox", help="Casilla a revisar (por defecto la del config).")
    parser.add_argument("--folders", help="Carpetas pendientes separadas por coma (sobrescribe el default).")
    parser.add_argument("--json", action="store_true", help="emite la lista como JSON.")
    parser.add_argument("--detalle", action="store_true", help="agrega una descripcion corta por ticket (1 GET extra c/u).")
    parser.add_argument("--limit", type=int, default=None, help="procesa como maximo N solicitudes.")
    args = parser.parse_args(argv)

    if requests is None or BeautifulSoup is None:
        print("Faltan dependencias. Instalalas con:\n"
              "    python -m pip install requests beautifulsoup4", file=sys.stderr)
        return 3

    cfg = load_config()
    url = (cfg.get("FREESCOUT_URL") or DEFAULT_URL).rstrip("/")
    email = cfg.get("FREESCOUT_EMAIL")
    password = cfg.get("FREESCOUT_PASSWORD")
    mailbox_name = args.mailbox or cfg.get("FREESCOUT_MAILBOX") or DEFAULT_MAILBOX
    folders_wanted = ([f.strip() for f in args.folders.split(",") if f.strip()]
                      if args.folders else PENDING_FOLDERS)

    if not (email and password):
        print("Faltan credenciales de FreeScout. Configuralas con:\n"
              "    python configurar.py", file=sys.stderr)
        return 2

    session = requests.Session()
    session.headers.update({"User-Agent": "leer-solicitudes-freescout/1.0"})

    try:
        login(session, url, email, password)
        mid, mname = find_mailbox(session, url, mailbox_name)
        folders = active_folders(session, url, mid, folders_wanted)
        if not folders:
            print(f"No encontre carpetas pendientes {folders_wanted} en la casilla '{mname}'.",
                  file=sys.stderr)
            return 1
        solicitudes = collect(session, url, folders)
    except requests.RequestException as exc:
        print(f"Error de conexion contra {url}: {exc}", file=sys.stderr)
        return 1

    solicitudes.sort(key=lambda s: int(s["number"]) if s["number"].isdigit() else 0, reverse=True)
    if args.limit:
        solicitudes = solicitudes[: args.limit]

    if args.detalle:
        for s in solicitudes:
            s["descripcion"] = fetch_descripcion(session, s["url"])

    if args.json:
        print(json.dumps({"casilla": mname, "total": len(solicitudes), "solicitudes": solicitudes},
                         ensure_ascii=False, indent=2))
        return 0

    print(f"Casilla: {mname}  ·  solicitudes pendientes: {len(solicitudes)}")
    for s in solicitudes:
        tags = f"  [{', '.join(s['tags'])}]" if s["tags"] else ""
        cli = f"  ({s['customer']})" if s["customer"] else ""
        print(f"\n#{s['number']}  {s['subject']}{cli}{tags}")
        print(f"    carpeta: {s['folder']}  ·  {s['url']}")
        if args.detalle and s.get("descripcion"):
            print(f"    {s['descripcion']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
