---
name: leer-tareas-outline
metadata:
  version: "1.0.0"
description: >-
  Lee un documento de Outline (wiki) via la API `documents.info` y devuelve su
  contenido en markdown, pensada para obtener las tareas pendientes acordadas en
  reuniones desde el documento "Tareas". El token vive junto a la skill en un
  `config.env` (global, sirve para cualquier proyecto) que crea un script de
  configuracion. Usar cuando se pida revisar/listar tareas pendientes, leer el
  doc de tareas del wiki, o traer el contenido de un documento de Outline.
---

# Leer tareas pendientes desde Outline

Esta skill consulta un documento de **Outline** (el wiki, p. ej.
`wikikulvio.conversus.digital`) con la API `documents.info` y devuelve su texto
en markdown. El caso principal es leer el documento **"Tareas"** para revisar las
**tareas pendientes acordadas en reuniones**, pero sirve para cualquier documento.

Es **global**: el token de Outline se guarda **junto a la skill** (no en el
`.env` de cada proyecto), asi el mismo acceso funciona desde cualquier proyecto.

## Como guarda las credenciales

El token y la URL viven en un archivo `config.env` **en el directorio de la
skill** (junto a los scripts). Cuando la skill esta instalada de forma global
(`~/.claude/skills/leer-tareas-outline/`), el `config.env` queda ahi y aplica a
todos los proyectos. Ese archivo **no se commitea** (esta en el `.gitignore`).

```
OUTLINE_URL=https://wikikulvio.conversus.digital
OUTLINE_API_KEY=ol_api_xxxxxxxx
```

Tambien se respetan las variables de entorno `OUTLINE_API_KEY` / `OUTLINE_URL`,
que tienen prioridad sobre el archivo (util para CI o pruebas puntuales).

## Paso 1 — Configurar el acceso (una sola vez)

Si aun no existe `config.env`, pide configurarlo. Ejecuta el script de
configuracion; pregunta la URL (con valor por defecto) y la API key sin
mostrarla al teclear:

```
python configurar.py
```

No interactivo (no muestra el token al escribirlo si se usa `--api-key`, pero
puede quedar en el historial del shell; prefiere el modo interactivo):

```
python configurar.py --url https://wikikulvio.conversus.digital --api-key <token>
```

- La API key se obtiene en Outline: **Settings → API Tokens → New token**.
- **Nunca** imprimas el valor del token en el chat ni en logs.

## Paso 2 — Leer el documento

Por defecto lee el documento de tareas (`tareas-rxGJ59og3f`) y devuelve el
markdown completo:

```
python outline_tareas.py
```

Aceptar tambien id, slug o **URL completa** del documento:

```
python outline_tareas.py https://wikikulvio.conversus.digital/doc/tareas-rxGJ59og3f
python outline_tareas.py tareas-rxGJ59og3f
```

El script resuelve el id tomando lo que va tras `/doc/` (igual que la app
DogMind), por lo que se le puede pasar la URL tal cual.

## Paso 3 — Filtrar las pendientes (opcional)

El documento de tareas es una tabla markdown. Para acotar a ciertas filas usa
`--filtrar` (repetible; combina con AND, ignora mayusculas y tildes). Por
ejemplo, las filas de un responsable que sigan pendientes:

```
python outline_tareas.py --filtrar Jaime --filtrar pendiente
```

Para procesar las filas programaticamente, pide la tabla como JSON (lista de
filas, cada fila lista de celdas; la primera fila es el encabezado):

```
python outline_tareas.py --json
```

Si no se conoce el esquema exacto de la tabla, lo mas robusto es leer el markdown
completo (Paso 2) y razonar sobre el; los filtros son una conveniencia, no un
parser estricto.

## Errores comunes

- **Falta la API key**: el script lo avisa y apunta a `configurar.py`.
- **HTTP 401**: token invalido o vencido → reconfigurar con `configurar.py`.
- **HTTP 403**: el token no tiene permiso sobre ese documento.
- **HTTP 404**: id/slug equivocado.

## Notas

- Requiere la libreria **`requests`** (`python -m pip install requests`). El wiki
  esta tras **Cloudflare**, que bloquea la firma TLS de `urllib` con un 403
  (`error code: 1010`); `requests` la atraviesa (igual que la app DogMind).
- La llamada es `POST {OUTLINE_URL}/api/documents.info` con
  `Authorization: Bearer <token>` y cuerpo `{"id": "<slug>"}`.
- Esta skill es de **solo lectura** sobre Outline: no crea ni edita documentos.
  Un token con scope de solo lectura (incluso limitado a `documents.info`) basta;
  `auth.info`, `documents.list` o `collections.list` pueden dar 403 sin afectar.
