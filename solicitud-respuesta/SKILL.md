---
name: solicitud-respuesta
metadata:
  version: "1.0.0"
description: >-
  Redacta la salida final de una solicitud y la entrega POR CONSOLA: el texto para
  el cliente (claro, breve, poco técnico, sin faltas de ortografía) y la nota de
  bitácora con la acción ejecutada. No registra nada en bitácoras ni sistemas
  externos. Se usa tras `solicitud-ejecucion` (solicitud implementada) o tras un
  análisis cuya decisión fue "no implementar y solo responder". Usar para cerrar y
  responder una solicitud.
---

# solicitud-respuesta — texto al cliente y nota de bitácora

Último eslabón del flujo: producir la **respuesta al cliente** y la **nota de
bitácora**, ambas **por consola al usuario**. Esta skill **no registra nada** en
bitácoras ni en sistemas externos: solo redacta y entrega el texto.

> **Requisito previo:** `solicitud-ejecucion` (cambio implementado y commiteado) o
> un `solicitud-analisis` cuya decisión fue **"no implementar y solo responder"**.
>
> **Flujo:** higiene → análisis → (`worktree` si paralelo) → ejecución → **respuesta**.

## Reglas de redacción para el cliente

- No digas que "detectaste", "encontraste" o "identificaste" el problema si fue el
  cliente quien lo reportó.
- No repitas el reporte del cliente con otras palabras.
- Explica el origen de forma directa, por ejemplo:
  - "Esto ocurría porque…"
  - "El problema se debía a…"
  - "La pantalla estaba usando…"
- Explica la corrección o la aclaración, por ejemplo:
  - "Ya fue corregido…"
  - "Se actualizó…"
  - "Ahora…"
- Si el cambio fue **solo visual**, descríbelo como ajuste de visualización,
  presentación o interfaz. Si fue **funcional**, como corrección de comportamiento.
  No contradigas la clasificación del análisis.
- Si la decisión fue **no implementar** (era el funcionamiento esperado / duda de
  usuario), responde aclarando el comportamiento correcto, sin inventar un arreglo.
- Tono claro, breve y poco técnico, **sin faltas de ortografía**.

## Formato de la respuesta al cliente

```
{cliente},
{explicación breve y no técnica del origen o aclaración funcional, sin decir que fue detectado o encontrado}
{corrección aplicada o regla funcional correspondiente}
{saludo / firma} — Equipo {Fábrica | Proyectos} · {Kulvio | TareOn}
```

## Salida final por consola

Al terminar, **imprime por consola al usuario** estos dos bloques:

```
Nota — acción ejecutada:
- Acción ejecutada:
- Rama:
- Commit:

Nota — texto final cliente:
- {el texto para el cliente con el formato de arriba}
```

Si la decisión fue "no implementar y solo responder", en la nota de acción indica
que no hubo cambio de código (sin rama ni commit) y por qué.

## Notas

- Toda la salida es **por consola al usuario**; esta skill no toca sistemas externos.
- Mantener español (Chile), con acentos correctos.
