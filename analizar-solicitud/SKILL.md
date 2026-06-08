---
name: analizar-solicitud
description: >-
  Analiza una solicitud de cambio sobre el código: clasifica el tipo (error
  funcional, duda de usuario, cambio solo visual o cambio mixto), revisa el
  sistema y el código, y entrega un análisis detallado SIN modificar nada ni
  hacer commit. Si la decisión recomendada es implementar, ejecuta el cambio en
  una rama nueva, valida, commitea y devuelve POR CONSOLA el mensaje para el
  cliente y la nota de bitácora, sin registrar en ningún sistema externo. Usar
  cuando llega una solicitud/ticket para analizar o para analizar y resolver.
metadata:
  version: "1.0.1"
---

# Analizar (y opcionalmente resolver) una solicitud

Esta skill tiene **dos fases**:

- **Fase 1 — Análisis:** obligatoria y **solo lectura**. Clasifica y detalla; no
  toca código.
- **Fase 2 — Ejecución:** se corre **solo si** el análisis concluye que
  corresponde implementar, y **nunca contradice** la clasificación de la Fase 1.

> Toda la salida es **por consola al usuario**. Esta skill **no registra nada**
> en bitácoras ni en sistemas externos.

## Entrada

La solicitud llega con estos datos (los que falten, pedirlos o asumir con criterio):

- **Número** de solicitud
- **Título**
- **Cliente**
- **Descripción** de la solicitud
- **Imágenes** de apoyo, si las hay

---

## Fase 1 — Análisis (SOLO lectura)

Tu tarea es **solo analizar**: no modifiques código, no crees ramas, no hagas commit.

### Pre-requisito de rama
Valida que estás en la rama base (`main`/`master`). Si **no** lo estás, **detén
el análisis** y pide al usuario que actualice el repositorio/rama (la higiene de
git la cubre la skill `iniciar-solicitud`). No crees ramas.

### Objetivo
- Revisar la solicitud en el sistema y en el código.
- Clasificar correctamente el tipo de requerimiento.
- Entregar un análisis detallado de qué se debe cambiar, por qué, y cuál es el
  siguiente paso.

### Clasificación
Primero valida si la solicitud corresponde a una de estas categorías:

- **error del sistema / inconsistencia funcional**
- **duda del usuario** sobre permisos, roles o comportamiento esperado
- **cambio solo visual / de interfaz**
- **cambio mixto:** visual y funcional

**Definición de cambio solo visual:** ajustes de interfaz o presentación que **no**
modifican flujo, reglas, validaciones, persistencia, cálculos, estados, procesos,
integraciones ni comportamiento de datos. Ejemplos:
- textos, labels, placeholders, mensajes, títulos
- orden visual de elementos
- badges, iconos, colores, espaciados, alineación
- visibilidad o presentación de información ya existente
- tooltip o ayuda visual
- distribución responsive

**No es cambio solo visual** si altera aunque sea una de estas cosas:
- datos guardados o leídos
- reglas de negocio
- validaciones
- estados
- transiciones de flujo
- procesos automáticos
- permisos o autorizaciones
- integraciones
- cálculos
- comportamiento del sistema

### Criterio de análisis
- Revisa en el sistema y en el código si lo reportado efectivamente ocurre.
- Si es duda de usuario, valida si corresponde al funcionamiento actual o si en
  realidad es un error.
- Si parece visual, confirma **explícitamente** si toca o no flujo, datos, estado,
  procesos u otra lógica.
- Si es solo visual, explícalo de forma precisa. Si no lo es, detalla exactamente
  qué parte funcional se ve afectada.
- No implementes nada.

### Formato de salida (obligatorio)

```
Resultado de clasificación:
- Tipo: {error funcional | duda de usuario | cambio solo visual | cambio mixto}
- Impacta flujo/comportamiento: {sí | no}
- Impacta datos/estado/procesos: {sí | no}

Análisis:
- Qué ocurre actualmente:
- Por qué ocurre:
- Evidencia en sistema:
- Evidencia en código:
- Alcance real del cambio:

Detalle del cambio propuesto:
- Qué se debe cambiar:
- Por qué se debe cambiar:
- Qué no se debe tocar:
- Riesgos o regresiones a considerar:

Decisión recomendada:
- Siguiente paso: {implementar (Fase 2) | no implementar y solo responder | pedir más contexto}
- Justificación de la decisión:
```

Sé claro, breve y no redundante.

### Reglas de la Fase 1
- Si no estás en `main`/`master`, detente y pide actualizar la rama.
- No crees nueva rama.
- No hagas cambios de código.
- No hagas commit.

---

## Fase 2 — Ejecutar la decisión recomendada

Corre esta fase **solo** si la Fase 1 recomienda **implementar**. Tu tarea es
ejecutar esa decisión.

### Reglas generales
- **No contradigas** la clasificación de la Fase 1. Si el análisis dijo "cambio
  solo visual", no presentes el caso como un error funcional de datos o procesos.
- Alinéate con el archivo **`AGENTS.md`** del proyecto o, en su defecto, con
  **`CLAUDE.md`**.

### Criterio de acción
- Crea una **rama nueva** de trabajo con la convención `T#{numero}-{nombre-corto}`
  (ver la skill `iniciar-solicitud` para la convención de rama y la higiene de git).
- Aplica **solo** los cambios definidos en el análisis.
- Si el cambio es solo visual, **no toques** lógica, persistencia, validaciones,
  estados, procesos ni integraciones.
- **Valida** el cambio realizado.
- Realiza el **commit** con la skill `commit`. Si esa skill no está disponible,
  haz un commit normal en español, sin un formato detallado.
- Genera un **texto final para el cliente** en párrafos normales, claro y poco
  técnico.

### Reglas de redacción para la respuesta al cliente
- No digas que "detectaste", "encontraste" o "identificaste" el problema si fue el
  cliente quien lo reportó.
- No repitas el reporte del cliente con otras palabras.
- Explica el origen de forma directa, por ejemplo:
  - "Esto ocurría porque…"
  - "El problema se debía a…"
  - "La pantalla estaba usando…"
- Explica la corrección aplicada, por ejemplo:
  - "Ya fue corregido…"
  - "Se actualizó…"
  - "Ahora…"
- Si el cambio fue solo visual, descríbelo como ajuste de visualización,
  presentación o interfaz. Si fue funcional, como corrección de comportamiento.
- Tono claro, breve y poco técnico, **sin faltas de ortografía**.

### Formato de la respuesta al cliente

```
{cliente},
{explicación breve y no técnica del origen o aclaración funcional, sin decir que fue detectado o encontrado}
{corrección aplicada o regla funcional correspondiente}
{saludo / firma} — Equipo {Fábrica | Proyectos} · {Kulvio | TareOn}
```

### Salida final por consola

Al terminar, **imprime por consola al usuario** estos dos bloques.

```
Nota — acción ejecutada:
- Acción ejecutada:
- Rama:
- Commit:

Nota — texto final cliente:
- {el texto para el cliente con el formato de arriba}
```

---

## Notas
- La Fase 1 nunca modifica código; la Fase 2 solo corre si el análisis la
  recomienda y respeta su clasificación.
- Mantener español (Chile), con acentos correctos.
