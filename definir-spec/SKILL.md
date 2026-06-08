---
name: definir-spec
metadata:
  version: "1.0.1"
description: >-
  Definir una especificación (spec) a partir de una historia de usuario, o un
  spec de fix para un bug/corrección. Rellena un template, muestra en un listado
  numerado las asunciones funcionales/no técnicas, deja que el usuario marque las
  que no le parecen, y pregunta una a una (con barra de progreso y 4 asunciones +
  "otra") hasta cerrar la definición. Recién entonces crea el archivo de spec en
  la carpeta de specs del proyecto. Usar cuando se pida "definir un spec",
  "crear una especificación" o redactar el spec de una corrección.
---

# Definir spec

Convierte una **historia de usuario** (o la descripción de un bug) en una
especificación, mediante un diálogo de validación de asunciones. **No se escribe
el archivo hasta el final**, cuando la definición está cerrada.

Quien corre esta skill actúa como **orquestador**: define el spec, **no
implementa código**. La implementación posterior se delega aparte
(`delegar-codigo` / `delegar-test`).

## Paso 0 — Destino y tipo de spec

**Ubicación** (adaptarse a la convención del proyecto, no asumir):
- Si existe `docs/superpowers/specs/` → usar esa carpeta.
- Si no, usar `docs/specs/` (crearla si hace falta).
- Si el proyecto define otra ruta de specs, respetarla.

**Formato de salida — SIEMPRE el mismo.** La estructura de la spec es estándar y
fija: se usa el template canónico correspondiente, sin reinventar secciones ni
numeración entre una spec y otra. Solo cambia el **contenido**, no el formato:
- Feature → `templates/spec-feature.md`
- Fix → `templates/spec-fix.md`

(La ubicación puede variar por proyecto; el **formato del documento no**.)

**Nombre del archivo:** siempre con slug. `yyyymmdd-<slug-kebab>-spec.md` para
feature; `yyyymmdd-<slug-kebab>-fix.md` para corrección de bug (fecha compacta
sin guiones, ej. `20260101-login-email-password-spec.md`).

**Tipo de spec:**
- **Feature** — nace de una historia de usuario; usa el template "Feature".
- **Fix** — nace de un bug o corrección indicada por el usuario; usa el template
  "Fix" (foco en causa raíz, reproducción y corrección, no en alcance nuevo).

## Paso 1 — Rellenar el borrador desde la historia

Con la historia de usuario, completar el template "en borrador". Donde falte
información, **asumir con criterio** (no preguntar todavía) y dejar registrada
cada asunción para el listado del Paso 2.

## Paso 2 — Listado de asunciones (funcionales / no técnicas)

Mostrar al usuario un **listado numerado** con **todas las asunciones
funcionales o de negocio** que se tomaron — las decisiones que solo el
usuario/negocio puede validar (reglas, alcances, comportamientos, casos
incluidos/excluidos). Los detalles puramente técnicos (modelo de datos, rutas,
nombres internos) los resuelve el spec y **no** van en este listado.

Formato:
```
Asunciones que tomé (dime los números que NO te parecen):
1. <asunción funcional>
2. <asunción funcional>
...
```

## Paso 3 — El usuario marca lo que no le parece

El usuario responde con los **números** de las asunciones con las que no está de
acuerdo. Esos números forman la cola de preguntas del Paso 4. (Si no objeta
ninguna, saltar al Paso 5.)

## Paso 4 — Preguntas una a una (con barra de progreso)

Por **cada** asunción objetada, hacer **una sola pregunta a la vez** usando la
herramienta de preguntas (AskUserQuestion). Cada pregunta debe:

- **Mostrar barra de progreso** en el enunciado, con cuántas llevas y cuántas
  faltan. Ej.: `Pregunta 2/5  [▓▓░░░]`.
- Ofrecer **4 asunciones alternativas** como opciones + una **quinta opción
  "Otra"** (la herramienta agrega "Other"/"Otra" automáticamente; basta dar 4
  opciones). Si el usuario elige "Otra", entrega su propia definición.
- Tras la respuesta, **actualizar la definición** del spec con lo que el usuario
  indicó antes de pasar a la siguiente pregunta.

Hacer las preguntas **secuencialmente** (una llamada por asunción), no todas
juntas — así la barra de progreso avanza pregunta a pregunta.

## Paso 5 — Listo para crear la spec

Cuando no queden asunciones pendientes, **avisar explícitamente**: "Ya estoy
listo para crear la especificación." Recién ahí escribir el archivo en la
carpeta y con el nombre del Paso 0, con la definición ya consensuada.

(No commit ni push salvo que el usuario lo pida.)

## Paso 6 — Exportar a PDF (opcional, a pedido)

Cuando el usuario pida el PDF, el documento PDF se arma con **dos partes**:
una **explicación para el usuario final** al inicio, seguida del spec técnico.

1. **Intro para el usuario final — NO va en el `.md` del spec.** Redactarla en un
   archivo aparte `yyyymmdd-<slug>-intro-usuario.md`, usando
   `templates/intro-usuario.md`. Es texto **no técnico**, dirigido al usuario de
   la aplicación, explicando en detalle **qué se implementa** en este
   requerimiento, para qué le sirve y cómo lo notará. Nada de tablas de datos,
   rutas ni nombres internos.
2. **Generar el PDF** anteponiendo la intro al spec:
   ```
   <python-con-markdown-y-xhtml2pdf> build_pdf.py \
     <intro-usuario.md> <spec.md> <yyyymmdd-<slug>.pdf>
   ```
   - Usar un intérprete que tenga `markdown` + `xhtml2pdf` (p. ej. el venv del
     proyecto: `.venv\Scripts\python.exe`).
   - **Fallbacks** si esas libs no están: `pandoc intro.md spec.md -o salida.pdf`
     (requiere motor PDF), o `npx md-to-pdf` sobre el combinado.
3. El PDF queda junto al spec en la carpeta de specs. El `.md` del spec **sigue
   sin** la intro de usuario: la intro solo existe en su propio archivo y en el
   PDF.

---

## Templates canónicos

El formato vive en archivos, para que la salida sea idéntica siempre:
- `templates/spec-feature.md` — spec de feature (historia de usuario).
- `templates/spec-fix.md` — spec de fix (bug / corrección).

Rellenar los `<placeholders>`, borrar los comentarios guía, y **no alterar la
estructura ni la numeración de secciones**.

**BDD obligatorio.** Toda spec incluye una sección de **Criterios de aceptación
en Gherkin español** (Dado / Cuando / Entonces): camino feliz por cada RF, casos
de error y al menos un escenario de **regresión**. Es la base de los tests de
aceptación y nunca se omite.

## Notas

- El listado del Paso 2 son **decisiones funcionales/de negocio**, no detalles
  técnicos: es lo que el usuario debe validar.
- No implementar nada en esta skill; solo producir el spec.
- Mantener español (Chile), con acentos correctos.
