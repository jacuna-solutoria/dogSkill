---
name: worktree
metadata:
  version: "1.1.0"
description: >-
  Trabajar dos o más tareas/tickets en paralelo con git worktree, sin git stash
  ni cambiar de rama: materializa cada rama en una carpeta hermana que comparte
  el mismo .git. Cubre crear, listar, eliminar y limpiar worktrees con la
  convención de rama T#<num>-<nombre-corto>, más las cosas a cuidar en Windows
  (.venv y .env por carpeta, puertos del dev server, carpetas no anidadas).
  Usar cuando llega un cambio urgente mientras trabajas otra cosa, o cuando se
  pida "trabajar en paralelo", "git worktree", "otra rama sin perder contexto".
---

# worktree — varias ramas en paralelo sin stash

Una sola carpeta de trabajo solo puede tener **una rama activa** (un checkout) a
la vez. Si estás en una tarea y llega otra urgente, lo habitual es `git stash` o
un commit a medias, cambiar de rama y perder contexto. `git worktree` evita eso:
crea **otra carpeta** vinculada al **mismo `.git`**, con una rama distinta. No es
un clon (no duplica el historial ni descarga nada), solo materializa otra rama en
otro directorio; commits y ramas se comparten porque el `.git` es el mismo.

Usar esta skill cuando se necesite trabajar **dos o más tareas en paralelo** sin
mezclar sus cambios.

## 1. Crear un worktree

Desde el repositorio actual. **Carpeta hermana** (al lado, nunca dentro del repo)
y rama con la convención `T#<num>-<nombre-corto>` (ver "Relación con otras skills").

**Rama nueva**, partiendo desde la base actualizada. El worktree nace desde tu
`main` **local**, que puede estar viejo → haz `git fetch` antes, o parte desde
`origin/main` para nacer de lo último del remoto:
```
git fetch origin
git worktree add ../miapp-T1234 -b "T#1234-login-con-correo" origin/main
```
(equivalente partiendo del local ya actualizado: `... -b "T#1234-..." main`).

**Rama que ya existe:**
```
git worktree add ../miapp-T1234 "T#1234-login-con-correo"
```

> En PowerShell el `#` inicia un comentario: **siempre** entre comillas el nombre
> de rama (`"T#1234-..."`), o git verá solo `T`.

Si tu base es `master` en vez de `main`, úsala en su lugar. Para resolverla sin
asumir: `git symbolic-ref refs/remotes/origin/HEAD`.

## 2. Estructura resultante

```
C:\dev\
├── miapp\           ← tarea A (rama T#1100-...)  ← tu carpeta de siempre
└── miapp-T1234\     ← tarea B (rama T#1234-...)  ← carpeta nueva, independiente
```

Trabajas la tarea B en `miapp-T1234` sin tocar nada de la A. Cada carpeta tiene su
propio estado de archivos y su propia rama; el historial y los commits son
compartidos.

> **El agente NO hace `cd` a la carpeta del worktree.** Cambiar el directorio de
> trabajo a mitad de sesión le revuelve el contexto (rutas, archivos abiertos) y
> confunde a los subagentes. En su lugar se **abre una consola nueva para el
> usuario** ya parada en la carpeta (ver más abajo). El agente se queda donde
> estaba; si necesita operar sobre el worktree, usa `git -C ../miapp-T1234 ...`
> en vez de moverse.

### Abrir la consola del usuario en la carpeta nueva

Al crear un worktree se levanta automáticamente una consola en su carpeta,
probando en este **orden de preferencia**:

1. **Windows Terminal** (`wt`) → ventana nueva con la carpeta como directorio inicial.
2. **PowerShell** (`pwsh` 7 si está; si no, Windows PowerShell) → ventana nueva en la carpeta.
3. **cmd** → último recurso.

Lo hace el script de apoyo (`New-Worktree`, o `Open-WorktreeConsole` por separado);
ver sección 6. Si ninguna está disponible, avisa la ruta para abrirla a mano.

## 3. Comandos del día a día

```
git worktree list                       # ver todos los worktrees activos
git worktree add ../miapp-T1300 -b "T#1300-otro" main   # otra tarea más
git worktree remove ../miapp-T1234      # eliminar cuando terminas (mergeado)
git worktree prune                      # limpiar referencias muertas
```

`git worktree remove` falla si la carpeta tiene cambios sin commitear (es una
protección). Revisa con `git status` en esa carpeta antes; usa `--force` solo si
de verdad quieres descartar.

## 4. Cosas importantes (sobre todo en Windows)

1. **Una rama no puede estar en dos worktrees a la vez.** Cada worktree = una rama
   distinta. Eso es justo lo que se busca.
2. **Carpetas hermanas, no anidadas.** Crea los worktrees como `../miapp-XXXX` (al
   lado), **nunca dentro** del repo, para que git no se confunda.
3. **El entorno virtual NO se comparte.** Cada worktree es una carpeta separada;
   si trabajas con `.venv` local, crea el suyo (`python -m venv .venv` + instalar
   deps) o apunta el intérprete a uno existente.
4. **Lo que git ignora NO existe en el worktree nuevo.** El `.env` y los archivos
   de configuración local (`settings.local.*`, credenciales, certificados de dev)
   no están versionados, así que la carpeta nueva nace sin ellos y la app no
   levanta hasta que los **copies desde el repo oficial** (a mano o con el script
   de apoyo). Para ver qué tienes ignorado: `git status --ignored --short`. **No**
   copies `.venv` ni `node_modules`: se regeneran por carpeta (rutas absolutas).
5. **Puertos del dev server.** Si levantas dos servidores a la vez, usa puertos
   distintos (ej. `--port 5009` vs `--port 5010`) para que no choquen.
6. **El agente no se cambia de carpeta.** No hagas `cd` al worktree: abre una
   **consola aparte** para el usuario (`wt` → PowerShell → `cmd`) y, para los
   comandos de git que el agente necesite sobre esa carpeta, usa `git -C <ruta>`.
   Así no se confunde el contexto de la sesión ni el de otros subagentes.

## 5. Limpiar al terminar

Cuando la rama de un worktree ya está mergeada y no la necesitas:
```
git worktree remove ../miapp-T1234     # borra la carpeta de trabajo
git branch -d "T#1234-login-con-correo"   # borra la rama si ya está mergeada
git worktree prune                     # limpia referencias muertas
```

## 6. Script de apoyo (opcional)

`scripts/worktree.ps1` deja funciones para crear/listar/eliminar worktrees con la
convención `T#<num>-<nombre-corto>` y **copiar los archivos de configuración**
ignorados desde el repo oficial. Cárgalo en la sesión con `. .\scripts\worktree.ps1`
(dot-source) y luego:

```powershell
New-Worktree -Numero 1234 -Slug "login-con-correo"   # crea ../<repo>-T1234 desde la base, copia .env y ABRE una consola en la carpeta
New-Worktree -Numero 1234 -Slug "login-con-correo" -Config '.env','config.local.json'   # copia varios
New-Worktree -Numero 1234 -Slug "login-con-correo" -NoConsole   # crea sin abrir consola
Get-Worktrees                                         # = git worktree list
Remove-Worktree -Numero 1234                          # elimina la carpeta y referencias
Open-WorktreeConsole -Path ..\miapp-T1234            # abre una consola en una carpeta ya existente
```

`-Config` recibe la lista de archivos/carpetas ignorados que la app necesita
(por defecto `.env`); omite `.venv` y `node_modules`.

`New-Worktree` **abre una consola nueva en la carpeta del worktree** al terminar
(orden `wt` → PowerShell → `cmd`); usa `-NoConsole` para evitarlo. `Open-WorktreeConsole`
hace solo eso, útil para reabrir una consola en un worktree que ya existe. El
agente nunca hace `cd`: esta consola es **para el usuario**.

Son un atajo; los comandos `git worktree` directos siempre funcionan igual.

## Relación con otras skills

- **`iniciar-solicitud`** define la convención de rama `T#<solicitud>-<nombre-corto>`
  y la higiene de la base (estar en `main`/`master` actualizado). Esta skill
  **reutiliza** esa convención para nombrar tanto la rama como la carpeta del
  worktree; no la repitas, refiérete a ella. Diferencia clave: `iniciar-solicitud`
  hace **checkout** sobre una sola carpeta; `worktree` materializa la rama en una
  **carpeta aparte** para trabajar en paralelo. Si esa skill no está disponible,
  el nombre de rama sigue siendo `T#<num>-<nombre-corto>` en kebab-case, sin
  tildes ni espacios.
- Para commitear el trabajo dentro de un worktree, usar la skill **`commit`** (el
  `.git` es el mismo, así que el commit queda en la rama de ese worktree).

## Comparación rápida

| Opción | 2 tareas en paralelo | Disco | Cambio de contexto |
|--------|----------------------|-------|--------------------|
| `git stash` / cambiar de rama | ❌ una a la vez | mínimo | lento, frágil |
| `git worktree` | ✅ sí, real | bajo (comparte `.git`) | instantáneo (cambias de carpeta) |
| Clonar el repo 2 veces | ✅ sí | alto (todo duplicado) | ok pero pesado |
