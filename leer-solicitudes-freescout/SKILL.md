---
name: leer-solicitudes-freescout
metadata:
  version: "1.0.0"
description: >-
  Lee por scraping (solo lectura) las solicitudes/tickets PENDIENTES de una
  casilla de FreeScout, por defecto "SOL Fabrica". Inicia sesion, recorre las
  carpetas activas (No asignado / Propio / Asignado) y lista cada solicitud
  (numero, asunto, cliente, etiquetas, carpeta y URL). Las credenciales viven
  junto a la skill en un `config.env` (global, sirve para cualquier proyecto) que
  crea un script de configuracion. Usar cuando se pida revisar/listar las
  solicitudes o tickets pendientes de FreeScout (la casilla SOL Fabrica).
---

# Leer solicitudes pendientes desde FreeScout

Esta skill scrapea (HTML, **solo lectura**) una casilla de **FreeScout** y lista
sus **solicitudes pendientes**. Por defecto revisa la casilla **"SOL Fabrica"**.
No escribe nada en FreeScout ni en ningun otro sistema y no descarga adjuntos.

Es **global**: las credenciales se guardan **junto a la skill**, asi el mismo
acceso funciona desde cualquier proyecto. Sigue el mismo patron que
`leer-tareas-outline`.

## Como guarda las credenciales

URL, email, clave y casilla viven en un `config.env` **en el directorio de la
skill**. Instalada de forma global
(`~/.claude/skills/leer-solicitudes-freescout/`), ese `config.env` aplica a todos
los proyectos. **No se commitea** (esta en `.gitignore`).

```
FREESCOUT_URL=https://mesa.ejemplo.com
FREESCOUT_EMAIL=usuario@ejemplo.com
FREESCOUT_PASSWORD=********
FREESCOUT_MAILBOX=SOL Fabrica
```

> A diferencia de Outline (un token), aqui se guarda **email + clave** en texto
> plano (FreeScout no expone API key para esto). El archivo es local y queda
> ignorado por git; aun asi, tratalo como secreto.

Tambien se respetan las variables de entorno `FREESCOUT_URL`, `FREESCOUT_EMAIL`,
`FREESCOUT_PASSWORD`, `FREESCOUT_MAILBOX`, con prioridad sobre el archivo.

## Paso 1 — Configurar el acceso (una sola vez)

Si aun no existe `config.env`, pide configurarlo. El script pregunta URL, email,
clave (oculta al teclear) y la casilla a revisar:

```
python configurar.py
```

No interactivo (evita poner la clave en el historial del shell; prefiere el modo
interactivo):

```
python configurar.py --url https://mesa.ejemplo.com --email user@ejemplo.com --password <clave> --mailbox "SOL Fabrica"
```

**Nunca** imprimas la clave en el chat ni en logs.

## Paso 2 — Listar las solicitudes pendientes

```
python freescout_pendientes.py
```

Devuelve la casilla y, por cada solicitud pendiente, una linea con numero,
asunto, cliente, etiquetas, carpeta y la URL del ticket.

Opciones:

```
python freescout_pendientes.py --json            # salida estructurada (para procesar)
python freescout_pendientes.py --mailbox "Otra"  # revisar otra casilla
python freescout_pendientes.py --folders "No asignado,Asignado"   # otras carpetas pendientes
python freescout_pendientes.py --detalle         # agrega descripcion corta (1 GET extra por ticket)
python freescout_pendientes.py --limit 20        # tope de solicitudes
```

## Como funciona el scraping (resumen)

Replica los selectores ya probados de la app DogMind contra esta instancia de
FreeScout (Laravel):

1. **Login**: GET `/login` para el token CSRF `_token`, luego POST `/login` con
   `email` + `password` + `_token`. Si la respuesta aun trae el campo `password`,
   el login fallo.
2. **Casilla**: GET `/` → enlaces `/mailbox/<id>`; calza el nombre de la casilla
   (tolerante a mayusculas/tildes, acepta coincidencia parcial).
3. **Carpetas pendientes**: GET `/mailbox/<id>` → enlaces `/mailbox/<id>/<folder>`;
   se quedan las carpetas cuyo nombre (sin el contador final) este en la lista de
   pendientes (`No asignado`, `Propio`, `Asignado`).
4. **Conversaciones**: GET `/mailbox/<id>/<folder>?page=N` → filas
   `tr[data-conversation_id]`; de cada una saca numero, asunto, etiquetas y
   cliente. Pagina hasta que no aparezcan filas nuevas. Deduplica por numero.

## Errores comunes

- **Faltan credenciales**: corre `configurar.py`.
- **Login fallido**: email/clave incorrectos en `config.env`.
- **"No encontre la casilla ..."**: el script lista las casillas disponibles;
  ajusta `FREESCOUT_MAILBOX`.
- **No aparecen carpetas pendientes**: los nombres de carpeta no calzan; revisa
  `--folders` con los nombres exactos de FreeScout.
- **Sale vacio o raro**: FreeScout pudo cambiar su HTML; hay que ajustar los
  selectores en `freescout_pendientes.py`.

## Notas

- Requiere **`requests`** y **`beautifulsoup4`**
  (`python -m pip install requests beautifulsoup4`).
- Skill de **solo lectura**: nunca responde, asigna ni cierra tickets.
- Salida forzada a **UTF-8** para la consola de Windows.
