---
name: revisar-coderabbit
metadata:
  version: "1.0.0"
description: >-
  Triaje y cierre de las observaciones de CodeRabbit en un PR/merge request a
  partir de su URL. Parte 1: por cada observación valida si aplica y la encamina
  (corregir delegando / pedir issue a CodeRabbit / responder por qué no aplica).
  Parte 2: sobre las observaciones aún abiertas, comenta qué se implementó,
  etiqueta @coderabbitai y pide marcarlas resueltas. Usar cuando se entregue la
  URL de un PR con review de CodeRabbit para procesar.
---

# Revisar PR — observaciones de CodeRabbit

Procesa el review automático de **CodeRabbit** sobre un PR/MR, dado su URL. Son
dos fases: **triaje + corrección** (Parte 1) y **cierre de pendientes** (Parte 2).

Quien ejecuta esta skill es el **orquestador**: **no escribe código a mano**.
Toda corrección de código se delega a un subagente codificador (`delegar-codigo`)
y las pruebas a un subagente distinto (`delegar-test`). El orquestador valida.

## Requisitos

- La URL del PR (de ahí salen `owner`, `repo`, `number`).
- Autenticación contra GitHub — ver abajo.

## Autenticación — token del `.env` primero, `gh` de fallback

1. **Buscar un token en el `.env`** del proyecto (nombres típicos:
   `GITHUB_TOKEN`, `GH_TOKEN`, o un PAT del repo). Si existe, usarlo
   directamente contra la **API REST de GitHub** con `curl` — así **no hace
   falta `gh`**:
   ```
   curl -s -H "Authorization: Bearer $TOKEN" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/repos/{owner}/{repo}/pulls/{number}/comments
   ```
2. **Si no hay token en el `.env`**, usar **`gh`** (con su propia auth):
   ```
   gh api repos/{owner}/{repo}/pulls/{number}/comments
   ```
   Si `gh` tampoco está disponible/autenticado, avisar al usuario (instalar con
   `winget install --id GitHub.cli` y `gh auth login`).

No imprimir el valor del token en logs ni en el chat.

## Leer las observaciones

CodeRabbit deja **comentarios inline** sobre el diff y, a veces, comentarios de
PR. Recuperarlos (filtrar autor `coderabbitai`), con `curl`+token o con `gh`:

```
# inline (review):   /repos/{owner}/{repo}/pulls/{number}/comments
# de PR (issue):     /repos/{owner}/{repo}/issues/{number}/comments
# datos del PR:      gh pr view <url> --json number,headRefName,baseRefName,url
```

Guardar para cada observación: `id`, `path`, `line`, cuerpo, y si ya está
marcada resuelta/outdated.

## Parte 1 — Triaje de cada observación

Para **cada** observación de CodeRabbit, decidir **una** de tres vías según si
aplica realmente a los cambios de este PR:

**A) Aplica a lo modificado → corregir, sin comentar en el PR.**
- Es una observación válida sobre código que este PR tocó.
- **Delegar la corrección** al subagente codificador (`delegar-codigo`); si
  necesita test, al de pruebas (`delegar-test`). El orquestador valida y corre
  la suite.
- **No** se responde el comentario en el PR: el fix queda en el código del
  branch; CodeRabbit lo detecta al re-analizar. (El cierre explícito es la
  Parte 2.)

**B) No aplica porque es código NO modificado en este PR, pero es un error o
deuda técnica real → pedir a CodeRabbit que cree una issue.**
- Solo si efectivamente es un bug/deuda legítimo (no ruido). Si no lo es, va a la
  vía C.
- Responder el comentario etiquetando a `@coderabbitai` y pidiéndole **crear la
  issue** (verificar el comando vigente de CodeRabbit, p. ej. "@coderabbitai
  create an issue for this"). No abrir la issue a mano salvo que CodeRabbit no
  pueda.

**C) No corresponde ni como fix de este PR ni como issue → responder en el
review con explicación técnica.**
- Responder el propio comentario con el **por qué técnico** de no abordarlo en
  este contexto (falso positivo, fuera de scope intencional, decisión de diseño,
  patrón ya existente, etc.). Claro y respetuoso, en español.

Responder a un comentario inline (con token o con `gh`):
```
# con token:
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/{owner}/{repo}/pulls/{number}/comments/{comment_id}/replies \
  -d '{"body":"<texto>"}'
# con gh:
gh api repos/{owner}/{repo}/pulls/{number}/comments/{comment_id}/replies -f body="<texto>"
```

### Regla de oro de la Parte 1
- Vía A (aplica) → **se corrige, NO se comenta**.
- Vías B y C (no aplica) → **se comenta** (pedir issue / explicar), **no se toca
  el código**.
- Nunca cambiar código por una observación que no aplica solo para "callar" al bot.

## Parte 2 — Cierre de las observaciones abiertas

Tras aplicar las correcciones de la Parte 1 (idealmente con el branch ya
pusheado para que CodeRabbit reanalice):

1. Volver a leer las observaciones y quedarse con las que **siguen abiertas /
   no marcadas como resueltas** por el bot.
2. Por cada una que se corrigió (vía A), agregar un **nuevo comentario** que:
   - Describa brevemente **qué cambio se implementó** para resolverla (qué
     archivo/función y el porqué).
   - Etiquete a **`@coderabbitai`** y le pida **marcarla como resuelta**
     (`resolved`). Verificar el comando vigente (p. ej. "@coderabbitai resolve").
3. Las observaciones de vías B/C ya quedaron respondidas en Parte 1 — no se
   re-comentan.

## Notas

- Distinguir comentarios de **CodeRabbit** de los de humanos: esta skill solo
  procesa los del bot.
- No usar `confirm/alert/prompt` ni nada de UI — es flujo de PR vía `gh`.
- No hacer push ni merge sin autorización explícita del usuario.
- Si el PR no es de un repo con CodeRabbit configurado, avisar en vez de asumir.
