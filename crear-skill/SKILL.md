---
name: crear-skill
metadata:
  version: "1.0.0"
description: >-
  Crea una nueva skill en este repositorio siguiendo el formato estándar de las
  skills existentes: frontmatter con name (= carpeta), metadata.version y
  description; cuerpo en español (Chile); CHANGELOG propio; fila en el README; y
  cumplimiento de la especificación de agentskills.io. Usar cuando se pida crear,
  agregar o "scaffoldear" una skill nueva.
---

# Crear una skill (formato estándar del repo)

Esta skill genera una **skill nueva** con el mismo formato que el resto, para que
todas sean consistentes y válidas según
[la especificación de Agent Skills](https://agentskills.io/specification).

> Antes de crear, revisa las skills existentes: si lo pedido ya está cubierto por
> una, **extiéndela o referénciala** en vez de duplicar contenido.

## Paso 1 — Definir el nombre

El `name` es la pieza más restrictiva (debe coincidir con el nombre de la carpeta):

- 1–64 caracteres, solo **minúsculas, números y guiones** (`a-z`, `0-9`, `-`).
- **No** empieza ni termina con guion, ni lleva guiones consecutivos (`--`).
- **Debe ser idéntico al nombre de la carpeta** que contiene el `SKILL.md`.
- Estilo del repo: verbo/sustantivo en español, en kebab-case
  (ej. `commit`, `definir-spec`, `solicitud-higiene`, `solicitud-analisis`).

## Paso 2 — Crear la carpeta y el `SKILL.md`

Crea `nombre-skill/SKILL.md` con el frontmatter estándar (orden: `name`,
`metadata`, `description`):

```yaml
---
name: nombre-skill
metadata:
  version: "1.0.0"
description: >-
  Qué hace la skill y CUÁNDO usarla, con palabras clave que ayuden a activarla.
  Para descripciones de una sola línea, puede ir sin el bloque `>-`.
---
```

Reglas del frontmatter:

- `description` **obligatoria**, máx **1024 caracteres**, no vacía. Debe decir
  **qué hace** y **cuándo usarla** (los disparadores). Una línea para descripciones
  cortas; bloque plegado `>-` para las largas (como en `delegar-codigo`).
- `metadata.version` es un **string** SemVer; toda skill nace en `"1.0.0"`.
- No agregar campos de primer nivel fuera del estándar
  (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`).
  La versión va **dentro de `metadata`**, no como campo suelto.

## Paso 3 — Escribir el cuerpo

- En **español (Chile)**, con acentos correctos.
- Markdown con encabezados (`#`, `##`), pasos numerados, ejemplos y casos borde.
- Mantener el `SKILL.md` **bajo 500 líneas**; si crece, mover material de detalle
  a archivos aparte (`references/`, `assets/`, `scripts/`) y enlazarlos con rutas
  relativas, un solo nivel desde el `SKILL.md`.
- **No duplicar contenido de otras skills**: si necesitas algo que ya hace otra
  (p. ej. el formato de commit lo define `commit`, la higiene de rama
  `solicitud-higiene`), **referénciala** en vez de repetirla. Indica un fallback
  si esa skill pudiera no estar disponible.
- **Ejemplos genéricos**: nunca uses datos de un cliente o proyecto real (nombres,
  IDs de ticket, rutas con el usuario, dominios específicos). Usa ejemplos neutros
  (ej. un login de aplicación).

## Paso 4 — Crear el `CHANGELOG.md`

Cada skill lleva su propio `CHANGELOG.md` (SemVer, entradas más nuevas arriba):

```markdown
# Changelog — nombre-skill

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.0.0 - AAAA-MM-DD
- Versión inicial.
```

## Paso 5 — Registrar en el `README`

Agrega una fila a la tabla "Skills disponibles" del `README.md` de la raíz, con el
enlace a la carpeta, la versión (`1.0.0`) y un resumen de una línea. Mantén el
orden de la tabla.

## Paso 6 — Validar

Confirma que la skill cumple la especificación antes de darla por lista:

- `SKILL.md` existe en la carpeta.
- `name` = nombre de la carpeta, formato válido, ≤ 64.
- `description` no vacía y ≤ 1024 caracteres.
- Cuerpo < 500 líneas.
- `metadata.version` presente como string.
- Sin datos de proyectos/clientes reales en los ejemplos.

## Paso 7 — Publicar

- Si las skills también se usan de forma global, copia la carpeta a
  `~/.claude/skills/` (mantén repo y global sincronizados).
- Para el commit (y push si se pide), usa la skill `commit`. Si no está
  disponible, haz un commit normal en español.

---

## Estándar resumido

| Aspecto | Convención del repo |
|---------|---------------------|
| Carpeta | una por skill, en la raíz; nombre = `name` |
| Frontmatter | `name`, `metadata.version` (string), `description` (qué + cuándo) |
| Idioma | español (Chile), con acentos |
| Tamaño | `SKILL.md` < 500 líneas; detalle en `references/`/`assets/`/`scripts/` |
| Versionado | SemVer por skill; reglas en el `README` (sección "Versionado") |
| Historial | `CHANGELOG.md` propio por skill |
| Reutilización | referenciar otras skills, nunca duplicar |
| Ejemplos | genéricos, sin datos de clientes/proyectos |

Las reglas de cuándo subir MAJOR/MINOR/PATCH viven en el `README` del repo; no se
repiten aquí.
