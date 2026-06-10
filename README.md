# Skills

Repositorio de **skills** propias para Claude Code. Cada carpeta de la raíz es una
skill autocontenida: un `SKILL.md` con el instructivo (y, si corresponde,
templates, ejemplos o scripts de apoyo).

## Skills disponibles

| Skill | Versión | Qué hace |
|-------|---------|----------|
| [`commit`](commit/) | 1.1.0 | Crea un commit de git con formato de 3 mensajes (`-m`), con push opcional; antes de commitear código recuerda el gate de pruebas, calidad y seguridad. |
| [`crear-skill`](crear-skill/) | 1.0.0 | Crea una skill nueva con el formato estándar del repo (frontmatter, CHANGELOG, fila en README) y la valida contra la spec de agentskills.io. |
| [`definir-spec`](definir-spec/) | 1.0.1 | Convierte una historia de usuario (o un bug) en una especificación, validando asunciones una a una. Incluye templates, ejemplo y generador de PDF. |
| [`delegar-calidad`](delegar-calidad/) | 1.0.0 | Rol subagente revisor de calidad (solo lectura): revisa el cambio buscando malas prácticas y entrega hallazgos priorizados, sin corregir. Subagente distinto del de seguridad. |
| [`delegar-codigo`](delegar-codigo/) | 1.1.0 | Rol del agente principal como orquestador: NO escribe código ni tests, delega código (codificador), pruebas (`delegar-test`) y revisión (`delegar-calidad`/`delegar-seguridad`), y delega las correcciones a nuevos codificadores. |
| [`delegar-seguridad`](delegar-seguridad/) | 1.0.0 | Rol subagente revisor de seguridad (solo lectura): revisa el cambio siguiendo OWASP y entrega hallazgos por severidad, sin corregir. Subagente distinto del de calidad. |
| [`delegar-test`](delegar-test/) | 1.0.0 | Rol subagente de pruebas: escribe/edita solo tests que validan el comportamiento corregido y corre la suite. |
| [`leer-solicitudes-freescout`](leer-solicitudes-freescout/) | 1.1.0 | Lista por scraping (solo lectura) las solicitudes pendientes de una casilla de FreeScout (por defecto "SOL - Fabrica"); con `--ticket` trae el contenido completo de un ticket y descarga sus imagenes; credenciales globales en un `config.env` junto a la skill. |
| [`leer-tareas-outline`](leer-tareas-outline/) | 1.0.0 | Lee un documento de Outline (wiki) vía `documents.info` para obtener las tareas pendientes de reuniones; token global en un `config.env` junto a la skill. |
| [`revisar-coderabbit`](revisar-coderabbit/) | 1.0.0 | Triaje y cierre de las observaciones de CodeRabbit en un PR a partir de su URL. |
| [`solicitud-analisis`](solicitud-analisis/) | 1.0.0 | Analiza una solicitud (clasifica y detalla, solo lectura); escribe el resultado en `analisis.md` (scratch) y recomienda el siguiente paso. 2º paso del flujo de solicitud, tras `solicitud-higiene`. |
| [`solicitud-ejecucion`](solicitud-ejecucion/) | 1.0.0 | Implementa el cambio recomendado por el análisis: crea/usa la rama `T#<num>`, aplica solo lo definido, valida y commitea (vía `commit`). 3er paso del flujo de solicitud. |
| [`solicitud-higiene`](solicitud-higiene/) | 1.0.0 | Higiene de git al tomar una solicitud: verifica rama, pull, y maneja una solicitud en curso (continuación/reemplazo/paralelo→`worktree`). 1er paso del flujo de solicitud. |
| [`solicitud-respuesta`](solicitud-respuesta/) | 1.0.0 | Redacta por consola el texto final al cliente y la nota de bitácora de una solicitud, sin registrar en sistemas externos. Último paso del flujo de solicitud. |
| [`worktree`](worktree/) | 1.2.0 | Trabajar tareas en paralelo con git worktree (sin stash): crea, lista, elimina y limpia worktrees con la convención `T#<num>-<nombre-corto>`; copia `.env` y el `analisis.md` (handoff, sin commitear) a la carpeta nueva; abre una consola nueva para el usuario (`wt`→PowerShell→`cmd`) sin que el agente haga `cd`; incluye script PowerShell de apoyo. |

## Estructura de una skill

```
<nombre-skill>/
  SKILL.md        # instructivo + frontmatter (name, version, description)
  CHANGELOG.md    # historial de versiones de esta skill
  ...             # opcional: templates/, examples/, scripts
```

El `SKILL.md` sigue el [formato Agent Skills](https://agentskills.io/specification):
`name` y `description` son obligatorios; la versión va dentro de `metadata`
(campo opcional del estándar) como string:

```yaml
---
name: commit
description: ...
metadata:
  version: "1.0.0"
---
```

## Versionado

Cada skill se versiona de forma **independiente** con
[SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

| Parte | Cuándo subirla | Ejemplo |
|-------|----------------|---------|
| **PATCH** (`1.0.0` → `1.0.1`) | Corrección de typo, aclaración o ajuste menor de redacción que **no** cambia el comportamiento. | Mejorar el wording de un paso. |
| **MINOR** (`1.0.1` → `1.1.0`) | Nueva capacidad o paso **compatible** con el uso actual: lo que ya funcionaba sigue igual. | Agregar una opción nueva opcional. |
| **MAJOR** (`1.1.0` → `2.0.0`) | Cambio de comportamiento o de invocación que **rompe** la forma anterior de usar la skill. | Renombrar la skill, cambiar el flujo esperado. |

### Cómo registrar un cambio

Cuando modifiques una skill:

1. Sube la versión en `metadata.version` del frontmatter del `SKILL.md` según la
   tabla de arriba.
2. Agrega una entrada arriba de todo en el `CHANGELOG.md` de esa skill:
   ```markdown
   ## 1.1.0 - AAAA-MM-DD
   - Qué cambió, en una o dos líneas.
   ```
3. Actualiza la columna **Versión** de la tabla "Skills disponibles" en este
   README.

> La versión de una skill solo refleja sus propios cambios; cada skill avanza a
> su ritmo, no hay una versión global del repositorio.

## Uso

Estas skills se instalan en el directorio de skills de Claude Code (p. ej.
`~/.claude/skills/`). Para usar la versión de este repo, copia (o enlaza) la
carpeta de la skill a ese directorio.
