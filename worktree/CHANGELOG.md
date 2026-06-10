# Changelog — worktree

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.2.0 - 2026-06-10
- `New-Worktree` ahora copia también **`analisis.md`** (el análisis previo que
  escribe `solicitud-analisis`) a la carpeta nueva, como *handoff*: la consola
  nueva arranca en `solicitud-ejecucion` sin re-analizar. El archivo se agrega a
  `.git/info/exclude` para que no se commitee. Actualizadas las referencias a la
  antigua `iniciar-solicitud` por la cadena `solicitud-*`.

## 1.1.0 - 2026-06-09
- El agente ya no hace `cd` al worktree (revolvía su contexto): al crear uno se
  **abre una consola nueva para el usuario** en la carpeta, probando en orden
  `wt` (Windows Terminal) → PowerShell → `cmd`. Nueva función `Open-WorktreeConsole`,
  `New-Worktree` la llama por defecto (opt-out con `-NoConsole`). Documentado el
  uso de `git -C <ruta>` para operar el worktree sin moverse.

## 1.0.0 - 2026-06-09
- Versión inicial: crear, listar, eliminar y limpiar git worktrees para trabajar
  tareas en paralelo, con la convención de rama `T#<num>-<nombre-corto>`,
  consideraciones de Windows (`.venv`/`.env` por carpeta, puertos) y un script de
  apoyo en PowerShell.
