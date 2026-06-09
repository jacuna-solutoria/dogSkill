# Changelog — leer-solicitudes-freescout

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.1.0 - 2026-06-08
- Nuevo `--ticket <numero|URL>`: muestra el contenido COMPLETO de un ticket (todos los mensajes sin truncar) y descarga sus imagenes (inline y adjuntas) a `descargas/<numero>/` junto a la skill, imprimiendo las rutas locales para abrirlas. Soporta `--json` y `--out`.
- Resuelve el numero de ticket buscando en las carpetas de la casilla (pendientes y, si no aparece, todas); tambien acepta la URL `/conversation/<id>` directa.
- Filtra los eventos de actividad (asignaciones, workflows) para mostrar solo mensajes reales. `descargas/` ignorado por git.

## 1.0.1 - 2026-06-08
- Corrige el nombre real de la casilla por defecto: "SOL - Fabrica" (con guion) en la doc y el matching tolerante a guiones/tildes.

## 1.0.0 - 2026-06-08
- Versión inicial: lista por scraping (solo lectura) las solicitudes pendientes de una casilla de FreeScout (por defecto "SOL - Fabrica").
- `configurar.py` guarda URL, email, clave y casilla en un `config.env` junto a la skill (global), con la clave oculta al teclear.
- `freescout_pendientes.py` replica el login Laravel (CSRF) y los selectores de conversaciones de DogMind; soporta `--json`, `--mailbox`, `--folders`, `--detalle`, `--limit`; salida UTF-8.
- `config.env` y `__pycache__` ignorados por git.
