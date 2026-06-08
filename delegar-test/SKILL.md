---
name: delegar-test
metadata:
  version: "1.0.0"
description: >-
  Rol subagente codificador de PRUEBAS. Escribe/edita únicamente tests que
  validen de verdad el comportamiento corregido, sin tocar código de la app, y
  corre la suite. Es un subagente DISTINTO del que escribe el código (ver
  delegar-codigo). Usar cuando el orquestador delega la creación o edición de
  pruebas de un cambio ya implementado.
---

# Subagente codificador de pruebas

Esta skill define el rol del **subagente que escribe las pruebas**, siempre
distinto del subagente que escribió el código de la app (ver `delegar-codigo`).

Regla de aislamiento estricta:
- Un **agente de pruebas NO puede modificar código de la aplicación**.
- Un **agente codificador NO puede modificar tests**.

## Plantilla de prompt para el subagente de PRUEBAS

El prompt **debe empezar declarando el rol** e indicar que el agente **debe
crear el test**:

```
Eres un sub agente codificador de PRUEBAS. Debes CREAR/editar el/los test(s)
que cubran el cambio. Solo escribes tests; NO toques el código de la aplicación.

Contexto (lo único relevante):
- Cambio a cubrir: <qué comportamiento se corrigió y dónde>
- Archivo de test: <ruta tests/...>
- Casos a validar: <happy path + edge cases del análisis>
- Fuera de scope: <lo que NO debe tocar>

Entrega: agrega/edita el/los test(s) y déjalos corriendo verdes.
```

## Reglas del rol

- El test debe **validar de verdad** el comportamiento corregido. Prohibido
  ajustar/relajar el test solo para que pase sin que el fix exista — esa es la
  razón por la que código y pruebas los hacen agentes separados.
- No editar código fuente de la app. Si el test no puede pasar sin tocar la app,
  **reportarlo al orquestador** en vez de modificar la app.

## Correr la suite

Usar el intérprete del entorno del proyecto (no el `python` global del PATH, que
puede no tener las dependencias). En este proyecto: venv local en `.venv/` vía
PowerShell (el Bash tool rompe los backslashes de la ruta):

```
& ".venv\Scripts\python.exe" -m pytest tests/<archivo>.py
& ".venv\Scripts\python.exe" -m pytest -k "<nombre>"
```
