---
name: solicitud-ejecucion
metadata:
  version: "1.0.0"
description: >-
  Implementa el cambio recomendado por el análisis de una solicitud: crea la rama
  de trabajo `T#<num>-<nombre-corto>` (si no existe ya, p. ej. en un worktree),
  aplica SOLO lo definido en el análisis sin contradecir su clasificación, valida
  y commitea (vía la skill `commit`). Requiere un análisis previo que recomiende
  implementar (`solicitud-analisis`) y la aprobación para modificar código. No
  redacta la respuesta al cliente (eso es `solicitud-respuesta`). Usar para
  ejecutar/implementar una solicitud ya analizada.
---

# solicitud-ejecucion — implementar la solicitud analizada

Tercer eslabón del flujo: ejecutar la decisión del análisis. Solo corre si
`solicitud-analisis` recomendó **implementar** y hay **aprobación explícita** para
modificar código.

> **Requisito previo:** `solicitud-analisis` con decisión "implementar". El insumo
> es el `analisis.md` de la raíz (si vienes de un worktree, ya está copiado ahí).
> **No contradigas** la clasificación del análisis.
>
> **Flujo:** higiene → análisis → (`worktree` si paralelo) → **ejecución** → respuesta.

## Aprobación

No empieces a modificar código sin **aprobación explícita** (p. ej. "aprobado",
"nos aprueban el cambio" o equivalente). Mientras la solicitud esté en
análisis/solo-lectura, quédate en la base sin crear la rama.

## 1. Rama de trabajo

Con la aprobación dada, asegúrate de estar en la rama de trabajo:

- **En tu carpeta normal:** crea la rama desde la base ya actualizada:
  ```
  git checkout -b "T#<solicitud>-<nombre-corto>"
  ```
- **En un worktree:** la rama `T#<num>` **ya existe** (la creó `worktree`). No
  crees otra: trabaja sobre la que ya está.

Convención del nombre: `T#<solicitud>` = número de la solicitud; `<nombre-corto>`
= descripción breve en **kebab-case**, sin tildes ni espacios
(ej. `T#1234-login-con-correo-y-contrasena`).

> En PowerShell el `#` inicia un comentario: **siempre** entre comillas el nombre
> de rama (`"T#1234-..."`).

## 2. Implementar

- Alinéate con el archivo **`AGENTS.md`** del proyecto o, en su defecto, con
  **`CLAUDE.md`**.
- Aplica **solo** los cambios definidos en el `analisis.md`. Nada fuera de alcance.
- Si el análisis dijo **cambio solo visual**, **no toques** lógica, persistencia,
  validaciones, estados, procesos ni integraciones.
- No conviertas un cambio visual en uno funcional (ni viceversa): respeta la
  clasificación del análisis.

## 3. Validar

- **Valida** el cambio realizado (probar el flujo afectado, correr lo que
  corresponda según el proyecto). No des por hecho que funciona.

## 4. Commit

- Realiza el **commit** con la skill **`commit`**. Si esa skill no está disponible,
  haz un commit normal en español, sin un formato detallado.
- El `analisis.md` está marcado como scratch (`info/exclude`), así que **no** entra
  en el commit; confírmalo con `git status` antes de commitear.

## 5. Siguiente paso

Con el cambio commiteado, continuar con **`solicitud-respuesta`** para redactar el
texto al cliente y la nota de bitácora.

## Notas

- Esta skill modifica código y commitea, pero **no** registra nada en sistemas
  externos ni redacta la respuesta al cliente (eso es `solicitud-respuesta`).
- Para limpiar un worktree una vez mergeada la rama, ver `worktree`
  (`Remove-Worktree` / `git worktree remove`).
- Mantener español (Chile), con acentos correctos.
