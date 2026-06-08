---
name: iniciar-solicitud
metadata:
  version: "1.0.0"
description: >-
  Arranque de una nueva solicitud: higiene de git + análisis (solo lectura).
  Verifica la rama actual; si no es la rama base (main/master) hace checkout a
  ella y pull. Luego analiza en detalle lo que el usuario indica SIN tocar
  código. Solo tras aprobación explícita para modificar código crea la rama de
  trabajo T#<solicitud>-<nombre-corto>. Usar al tomar/empezar una solicitud.
---

# Iniciar solicitud — higiene de rama + análisis

Esta skill prepara el repo al **empezar una solicitud nueva** y produce el
**análisis previo** (solo lectura). Garantiza que se parte siempre desde la rama
base actualizada, que se entiende el problema antes de tocar nada, y que el
trabajo aprobado se hace en una rama dedicada con la convención
`T#<solicitud>-<nombre-corto>`.

## 1. Verificar la rama actual

```
git rev-parse --abbrev-ref HEAD
```

- Si ya estás en la rama base (`main` o `master`) → seguir al paso 3 (pull).
- Si estás en cualquier otra rama → paso 2.

La rama base de este repo es **`main`** (remoto `origin/main`). Si el repo usara
`master`, aplicar lo mismo sobre `master`. Para resolverla sin asumir:
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

## 4. Analizar la solicitud — SOLO lectura

Con la base actualizada, analizar **lo que el usuario indica sin modificar ni
una línea de código** (solo leer el repo). El análisis debe ser **detallado** y
cubrir:

- **Por qué ocurre** — la causa raíz real del error/comportamiento, no el
  síntoma. Apuntar a la lógica concreta responsable.
- **Cuándo pasa** — las condiciones que lo disparan: ruta/acción, rol, estado
  del dato, edge case o secuencia que lo reproduce.
- **Cómo se soluciona** — el enfoque de corrección recomendado.
- **Archivos a modificar y por qué** — listar brevemente cada archivo (y
  función/ruta/template si aplica) y qué cambio recibiría y para qué. Es un
  mapa del cambio propuesto, **no** el cambio aplicado.

Reglas del análisis:
- **No** usar Edit/Write sobre código fuente. Solo lectura del repo.
- Si la solicitud no es viable o tiene un problema real, hacer **pushback
  honesto**: contrastar alternativas y recomendar la mejor, no asumir.
- Este análisis es el insumo que se presenta para la aprobación del paso 5.

## 5. Crear la rama de trabajo — SOLO con aprobación

**No crear la rama hasta tener aprobación explícita para modificar código**
(p. ej. "aprobado", "Víctor nos aprueba el cambio" o equivalente). Mientras la
solicitud esté en análisis/solo-lectura, quedarse en la base.

Con la aprobación dada, crear la rama dedicada desde la base ya actualizada:
```
git checkout -b "T#<solicitud>-<nombre-corto>"
```

Convención del nombre:
- `T#<solicitud>` = número de la solicitud/tarea (ej. `T#17455`).
- `<nombre-corto>` = descripción breve en **kebab-case**, sin tildes ni espacios
  (ej. `correccion-estado-proveedores-dpa`).
- Ejemplo completo: `T#17455-correccion-estado-proveedores-dpa`.

## Notas

- Esta skill **no** hace commits ni push. Solo prepara rama y trae cambios.
- Sobre esta rama de trabajo se ejecuta luego la implementación delegada
  (subagentes de código y de pruebas).
