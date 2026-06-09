# Changelog — leer-tareas-outline

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.0.0 - 2026-06-08
- Versión inicial: lee documentos de Outline vía `documents.info` y devuelve el markdown.
- `configurar.py` guarda URL y API key en un `config.env` junto a la skill (global), con el token oculto al teclear.
- `outline_tareas.py` acepta id, slug o URL, con filtros de tabla (`--filtrar`) y salida JSON; salida forzada a UTF-8 para la consola de Windows.
- Usa `requests` (no `urllib`): el wiki está tras Cloudflare, que bloquea la firma de `urllib` con un 403/1010.
- `config.env` ignorado por git para no commitear el token.
