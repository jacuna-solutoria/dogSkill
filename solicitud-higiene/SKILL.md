---
name: solicitud-higiene
metadata:
  version: "1.0.0"
description: >-
  Primer paso al tomar una solicitud/ticket: deja el repositorio listo antes de
  analizar o tocar nada. Verifica la rama actual; si es la base (main/master)
  hace pull; si ya hay una solicitud en curso (rama T#...) pregunta si es
  continuación, reemplazo o trabajo en paralelo (deriva a `worktree`). No crea la
  rama de trabajo ni modifica código. Usar al empezar/tomar una solicitud, antes
  de `solicitud-analisis`.
---

# solicitud-higiene — dejar el repo listo para una solicitud

Primer eslabón del flujo de una solicitud: **higiene de git**. Garantiza que se
parte desde la rama base actualizada (o desde la rama correcta si el trabajo ya
está en curso) **antes** de analizar o implementar nada.

> **Flujo completo de una solicitud:**
> `solicitud-higiene` → `solicitud-analisis` → (`worktree` si es en paralelo) →
> `solicitud-ejecucion` → `solicitud-respuesta`. Cada skill nombra su paso
> previo; no las invoques fuera de orden.

Esta skill **no** crea la rama de trabajo ni modifica código (eso es
`solicitud-ejecucion`). Solo prepara el terreno y pasa el control a
`solicitud-analisis`.

## Atajo: ¿ya hay análisis hecho en esta carpeta?

Si la rama actual es una `T#<num>-...` **y** existe un `analisis.md` en la raíz,
esta carpeta ya tiene una solicitud higienizada y analizada (típico al abrir la
consola de un **worktree**, que copia el `analisis.md` desde la carpeta original).
En ese caso **no higienices ni re-analices**: salta directo a
`solicitud-ejecucion`. Para detectar un worktree enlazado:

```
git rev-parse --git-dir          # en un worktree: ...\.git\worktrees\<nombre>
git rev-parse --git-common-dir   # apunta al .git común; si difieren, es worktree
```

## 1. Verificar la rama actual

```
git rev-parse --abbrev-ref HEAD
```

- Si ya estás en la rama base (`main` o `master`) → seguir al paso 3 (pull).
- Si estás en **otra rama** (una `T#...`) → esta carpeta ya tiene una solicitud en
  curso. **No hacer checkout a ciegas.** Preguntar cómo seguir y elegir una de tres
  salidas:

  > Estás en `T#<...>`. Esta nueva solicitud, ¿es **(1)** continuación del mismo
  > trabajo, **(2)** una solicitud nueva que reemplaza el contexto actual, o
  > **(3)** una solicitud nueva **en paralelo** (mantienes ambas a la vez)?

  1. **Continuación del mismo trabajo** → quedarte en esta rama, **no** cambiar
     nada, e ir directo al análisis (`solicitud-analisis`).
  2. **Nueva, reemplaza el contexto actual** (ya terminaste/abandonas la actual en
     esta carpeta) → **rama base**: paso 2 (checkout a la base) → 3 (pull) →
     `solicitud-analisis`.
  3. **Nueva, en paralelo** → **NO** hacer checkout: cambiar de rama aquí le movería
     el piso a la otra consola/editor que usa esta carpeta (mismo working tree,
     mismo `HEAD`). Usar la skill **`worktree`** para crear una carpeta hermana con
     la rama nueva y abrir la consola/editor **en esa carpeta**; allí se sigue el
     flujo sobre su propio working tree. Si `worktree` no está disponible, crear el
     worktree a mano: `git worktree add ../<repo>-T<num> -b "T#<num>-<slug>" origin/main`.

  Ante la duda, **preguntar antes de hacer checkout**: en los casos 1 y 3 el
  checkout es destructivo.

La rama base de este repo suele ser **`main`** (remoto `origin/main`). Si el repo
usara `master`, aplicar lo mismo sobre `master`. Para resolverla sin asumir:
```
git symbolic-ref refs/remotes/origin/HEAD   # -> refs/remotes/origin/<base>
```

## 2. Cambiar a la rama base

**Antes de cambiar, revisar que no haya trabajo sin commitear:**
```
git status --short
```
- Si hay cambios locales sin commitear → **NO** hacer checkout (perderías o
  arrastrarías trabajo). Detenerse y avisar al usuario para decidir (commit,
  stash o descarte explícito). No descartar nada por cuenta propia.
- Si el árbol está limpio → cambiar a la base:
```
git checkout main      # o master, según el repo
```

## 3. Actualizar (pull)

```
git pull --ff-only
```
- Traer lo último de `origin`. Si el fast-forward falla (divergencia), detenerse
  y avisar — no forzar merge/rebase sin instrucción.

## 4. Listo → analizar

Con la base actualizada (o ya parado en la rama correcta), el repo está higienizado.
Continuar con **`solicitud-analisis`** (solo lectura). La rama de trabajo `T#<num>`
**no** se crea aquí: nace recién en `solicitud-ejecucion` (o la crea `worktree` en
el caso paralelo).

## Notas

- Esta skill no hace commits, no crea ramas de trabajo ni modifica código.
- La convención de la rama de trabajo es `T#<solicitud>-<nombre-corto>` en
  kebab-case, sin tildes ni espacios (ej. `T#1234-login-con-correo`).
- Para trabajar **varias solicitudes en paralelo** sin pisarse, ver **`worktree`**
  (una carpeta por solicitud sobre el mismo `.git`).
