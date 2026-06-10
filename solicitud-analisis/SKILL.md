---
name: solicitud-analisis
metadata:
  version: "1.0.0"
description: >-
  Analiza una solicitud/ticket SOLO lectura: clasifica el tipo (error funcional,
  duda de usuario, cambio solo visual o mixto), revisa sistema y código, y
  entrega un análisis detallado que termina con una recomendación (implementar,
  no implementar y responder, o pedir más contexto). Escribe el resultado en un
  `analisis.md` (scratch, no se commitea) en la raíz, que `worktree` puede copiar
  a una carpeta nueva para no re-analizar. No modifica código ni hace commit.
  Requiere haber corrido `solicitud-higiene` antes. Usar para analizar una
  solicitud.
---

# solicitud-analisis — analizar una solicitud (solo lectura)

Segundo eslabón del flujo. Clasifica y detalla la solicitud **sin tocar nada** y
deja el resultado escrito en `analisis.md`, que es el insumo para decidir el
siguiente paso (y el *handoff* hacia un worktree, si el trabajo va en paralelo).

> **Requisito previo:** `solicitud-higiene` (estar en la rama base actualizada, o
> en la rama correcta si la solicitud ya está en curso). Si **no** estás en
> `main`/`master` ni en la rama de la solicitud, **detente** y corre primero
> `solicitud-higiene`. No crees ramas aquí.
>
> **Flujo:** higiene → **análisis** → (`worktree` si paralelo) → ejecución → respuesta.

Tarea: **solo analizar**. No modifiques código, no crees ramas, no hagas commit.

## Entrada

La solicitud llega con estos datos (los que falten, pedirlos o asumir con criterio):

- **Número** de solicitud
- **Título**
- **Cliente**
- **Descripción** de la solicitud
- **Imágenes** de apoyo, si las hay

## Objetivo

- Revisar la solicitud en el sistema y en el código (solo lectura del repo).
- Clasificar correctamente el tipo de requerimiento.
- Detallar qué se debe cambiar, por qué, cuándo ocurre y cuál es el siguiente paso.

## Clasificación

Valida si la solicitud corresponde a una de estas categorías:

- **error del sistema / inconsistencia funcional**
- **duda del usuario** sobre permisos, roles o comportamiento esperado
- **cambio solo visual / de interfaz**
- **cambio mixto:** visual y funcional

**Definición de cambio solo visual:** ajustes de interfaz o presentación que **no**
modifican flujo, reglas, validaciones, persistencia, cálculos, estados, procesos,
integraciones ni comportamiento de datos. Ejemplos: textos/labels/placeholders,
orden visual, badges/iconos/colores/espaciados, visibilidad o presentación de
información ya existente, tooltips, distribución responsive.

**No es cambio solo visual** si altera aunque sea una de estas cosas: datos
guardados o leídos, reglas de negocio, validaciones, estados, transiciones de
flujo, procesos automáticos, permisos o autorizaciones, integraciones, cálculos,
o cualquier comportamiento del sistema.

## Criterio de análisis

- Revisa en el sistema y en el código si lo reportado efectivamente ocurre.
- Si es duda de usuario, valida si corresponde al funcionamiento actual o si en
  realidad es un error.
- Si parece visual, confirma **explícitamente** si toca o no flujo, datos, estado,
  procesos u otra lógica. Si es solo visual, explícalo con precisión; si no lo es,
  detalla exactamente qué parte funcional se ve afectada.
- Cubre la **causa raíz** real (no el síntoma), **cuándo** se dispara (ruta/acción,
  rol, estado del dato, edge case) y **cómo** se corrige.
- Lista los **archivos a modificar y por qué** (función/ruta/template si aplica):
  es un mapa del cambio propuesto, **no** el cambio aplicado.
- Si la solicitud no es viable o tiene un problema real, haz **pushback honesto**:
  contrasta alternativas y recomienda la mejor, no asumas.
- **No** uses Edit/Write sobre código fuente. Solo lectura del repo.

## Salida: escribir `analisis.md`

Escribe el análisis en un archivo **`analisis.md`** en la raíz del repo, con este
formato (y muéstralo también por consola):

```
Resultado de clasificación:
- Tipo: {error funcional | duda de usuario | cambio solo visual | cambio mixto}
- Impacta flujo/comportamiento: {sí | no}
- Impacta datos/estado/procesos: {sí | no}

Análisis:
- Qué ocurre actualmente:
- Por qué ocurre (causa raíz):
- Cuándo ocurre (condiciones que lo disparan):
- Evidencia en sistema:
- Evidencia en código:
- Alcance real del cambio:

Detalle del cambio propuesto:
- Qué se debe cambiar:
- Archivos a modificar y por qué:
- Qué NO se debe tocar:
- Riesgos o regresiones a considerar:

Decisión recomendada:
- Siguiente paso: {implementar | no implementar y solo responder | pedir más contexto}
- Justificación:
```

Sé claro, breve y no redundante.

### `analisis.md` es scratch — no se commitea

`analisis.md` es un insumo de trabajo, **no** parte del cambio: no debe entrar en
ningún commit. Asegúralo agregándolo al *exclude* local del repo (afecta también
a los worktrees, que comparten el `.git`):

```powershell
$ex = git rev-parse --git-path info/exclude
if ((Get-Content $ex -ErrorAction SilentlyContinue) -notcontains 'analisis.md') {
    Add-Content $ex 'analisis.md'
}
```

> Por eso el trabajo real lo ignora: `analisis.md` queda fuera de los archivos
> versionados que se tocan en la consola.

## Siguiente paso según la decisión

- **implementar** en esta misma carpeta → `solicitud-ejecucion` (crea la rama
  `T#<num>` e implementa).
- **implementar en paralelo** (sin perder el trabajo actual de esta carpeta) →
  `worktree`: crea la carpeta hermana con la rama `T#<num>`, **copia `analisis.md`**
  (y `.env`) a la carpeta nueva y abre una consola allí. En esa consola se sigue
  con `solicitud-ejecucion` **sin re-analizar** (el análisis ya viaja en el archivo).
- **no implementar y solo responder** → `solicitud-respuesta`.
- **pedir más contexto** → responder al usuario y detenerse.

## Reglas

- Si no estás en `main`/`master` ni en la rama de la solicitud, detente y corre
  `solicitud-higiene`.
- No crees rama, no edites código fuente, no hagas commit.
- Mantener español (Chile), con acentos correctos.
