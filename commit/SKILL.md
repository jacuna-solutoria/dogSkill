---
name: commit
metadata:
  version: "1.0.0"
description: Crear un commit de git con formato de 3 mensajes (-m), con push opcional. Usar cuando el usuario pida hacer un commit ("haz commit", "/commit", "commitea esto", "commit push"). El commit lleva un título corto, un cuerpo con los hitos modificados, y notas adicionales opcionales. Hace push a remoto solo si el usuario lo indica explícitamente.
---

# commit

Crea un commit de git usando **tres** flags `-m` con un formato estandarizado.

## Push: commit vs commit push

El push depende EXCLUSIVAMENTE de lo que el usuario indique:

- **"commit"** (sin "push") → solo hacer el commit en la **rama actual**, según lo que se está trabajando y las definiciones entregadas. **NO hacer push.**
- **"commit push"** (o el usuario pide explícitamente push) → hacer el commit y, al finalizar, hacer **`git push` de la rama actual al remoto**.

Si el usuario no menciona push, asumir solo commit (nunca pushear por defecto).

## Estructura del commit

El commit se arma SIEMPRE con la forma:

```bash
git commit -m "<título>" -m "<cuerpo de hitos>" -m "<notas adicionales>"
```

### `-m` #1 — Título (obligatorio, ≤ 70 caracteres)
- **Una sola línea física, máximo 70 caracteres.** Es la regla más importante de
  esta skill: GitHub usa la **primera línea** del commit como título del PR y
  manda el resto al cuerpo. Si el título se pasa o lleva un salto de línea, se
  parte mal (ver "Errores comunes").
- **NUNCA** insertar un salto de línea dentro del título, ni "envolverlo" a 72/80
  columnas. El string del primer `-m` no debe contener `\n` jamás — ni siquiera
  para que "quepa". Si es largo, **acortarlo**, no partirlo.
- **No meter listas de scope ni detalle en el paréntesis** (ej. evitar
  `(reporte semanal + technologies)`). El paréntesis es solo el módulo/dominio
  (`fix(scheduler): …`). Todo el detalle va al cuerpo (`-m` #2).
- Explica de forma corta y clara de qué trata el commit.
- En español (Chile), modo imperativo o descriptivo breve.
- Opcionalmente puede llevar prefijo de tipo (`feat:`, `fix:`, `refactor:`, `docs:`, etc.) si encaja, sin pasarse de los 70 chars.
- **Verificar el largo antes de commitear.** Si no estás seguro, contar:
  `"<título>".Length` (PowerShell) o `echo -n "<título>" | wc -c` (Bash). Si
  supera 70, reescribir más corto antes de ejecutar el commit.

### `-m` #2 — Cuerpo de hitos (obligatorio)
- Detalle simple de lo que se está implementando.
- Un bullet por cada hito importante que se modifica, con verbo claro:
  - `se corrige <a>`
  - `se implementa <b>`
  - `se agrega <c>`
  - `se elimina <d>` / `se refactoriza <e>`, etc.
- Cada hito en su propia línea (usar saltos de línea reales dentro del `-m`).
- Mantenerlo conciso: un hito = una línea corta, sin párrafos largos.

### `-m` #3 — Notas adicionales (OPCIONAL)
- Solo si hay algo relevante que agregar: dependencias, follow-ups, breaking changes, contexto de la tarea (ej. ID DogMind), advertencias de migración.
- Si no hay nada que anotar, **omitir este tercer `-m`** por completo (no poner uno vacío).

## Flujo

1. Revisar qué hay para commitear:
   - `git status` y `git diff` (staged y unstaged) para entender los cambios reales.
   - Si nada está staged, decidir qué agregar (`git add`) según lo que el usuario pidió. No agregar archivos no relacionados ni artefactos temporales (capturas `.tmp_*.png`, etc.) salvo que el usuario lo indique.
2. Derivar el título, los hitos y las notas a partir del diff real — no inventar cambios que no están.
3. Construir el commit con los 2 o 3 `-m` según corresponda.
4. No usar `--no-verify` ni saltar hooks salvo que el usuario lo pida explícitamente. Si un hook falla, investigar la causa.
5. Si la rama actual es la rama por defecto (`main`/`master`), considerar crear una rama antes salvo que el usuario indique commitear directo.
6. **Push (solo si el usuario dijo "push"):** al terminar el commit, hacer `git push` de la rama actual al remoto.
   - Si la rama aún no tiene upstream, usar `git push -u origin <rama-actual>`.
   - Si el usuario NO mencionó push, terminar tras el commit y no pushear.

## Ejemplo

Cambios: se arregló un cálculo de plazos en brechas, se agregó un campo nuevo al formulario y se actualizó un template.

### En PowerShell (Windows)

Usar here-strings de comilla simple para los `-m` multilínea:

```powershell
git commit -m "fix(brechas): corrige calculo de plazos y agrega campo origen" -m @'
se corrige el calculo de plazo legal de notificacion de brechas
se agrega el campo "origen" al formulario de incidente
se actualiza el template _breach_form.html con el nuevo campo
'@ -m @'
Requiere migracion para la columna origin_type (ver runbook).
Tarea DogMind #17942.
'@
```

### En Bash

```bash
git commit -m "fix(brechas): corrige calculo de plazos y agrega campo origen" -m "se corrige el calculo de plazo legal de notificacion de brechas
se agrega el campo \"origen\" al formulario de incidente
se actualiza el template _breach_form.html con el nuevo campo" -m "Requiere migracion para la columna origin_type (ver runbook).
Tarea DogMind #17942."
```

## Errores comunes

- **Título demasiado largo / partido en el PR.** Síntoma: en GitHub el título del
  PR sale cortado a mitad de palabra (ej. "…(reporte sema") y la descripción
  empieza con la cola ("…nal + technologies)"). Causa: el primer `-m` superó los
  70 chars o tenía un salto de línea, así que GitHub tomó solo la primera línea
  como título y mandó el resto al cuerpo. **Prevención:** título de una sola
  línea ≤ 70 chars, sin `\n`, sin listas de scope en el paréntesis. Para arreglar
  un commit ya hecho que aún no se pushea: `git commit --amend` con un título
  corregido.

## Reglas

- Título **≤ 70 caracteres** y **una sola línea sin saltos** — verificarlo antes de commitear.
- Español (Chile). Acentos correctos en el texto del commit cuando el entorno lo soporte; si la shell tiene problemas de encoding, preferir texto sin acentos en el comando git para no corromper el mensaje.
- El segundo `-m` siempre lleva al menos un hito.
- El tercer `-m` es opcional: omitirlo si no hay notas.
- No commitear archivos no relacionados con el cambio pedido.
