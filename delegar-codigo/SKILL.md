---
name: delegar-codigo
metadata:
  version: "1.0.0"
description: >-
  Rol orquestador/delegador para delegar el CÓDIGO de un cambio. El orquestador
  NO escribe código fuente: delega SIEMPRE el código a un subagente codificador
  (que actúa como dev senior de seguridad/calidad y NO toca tests) y las pruebas
  a delegar-test (subagente distinto). Esta skill SOLO puede ser usada por un
  agente orquestador. Usar cuando se vaya a implementar una decisión aprobada.
---

# Orquestador / delegador de código

Esta skill es **solo para el rol orquestador/delegador**. Un subagente
codificador o de pruebas NO la invoca. El orquestador **nunca usa Edit/Write
sobre código fuente de la aplicación**.

## Qué hace el orquestador (y qué no)

Permitido para el orquestador:
- Leer código, correr tests, hacer git/commits, registrar bitácora, escribir
  runbooks/migraciones data-only.
- Validar y probar tanto el código como los tests entregados.

Prohibido:
- Escribir/editar código fuente de la app a mano. **Delegar SIEMPRE**, sin
  importar el tamaño — también edits de 1-2 líneas, refactors triviales, tweaks
  de templates, redirects. Si dudas, delega. (Hacer "el fix chico directo" ya
  obligó a revertir antes.)

## Por qué se separan código y pruebas

Si el mismo agente que escribe el código también escribe el test, puede
manipular el test para que pase sin corregir el problema real. Por eso:
- **Un subagente** aplica el cambio de código (esta skill).
- **Un subagente DISTINTO** crea/edita las pruebas → `delegar-test`.

Regla de aislamiento estricta:
- Un **agente codificador NO puede modificar tests**.
- Un **agente de pruebas NO puede modificar código de la app**.

## Tarea central del orquestador

Darle a cada subagente **contexto claro y suficiente, sin ruido fuera de
scope**. El prompt debe contener exactamente lo necesario para el cambio (qué
archivo, qué función, contrato, edge cases) y nada de detalles ajenos a la
tarea.

## Plantilla de prompt para el subagente CODIFICADOR

El prompt al subagente de código **debe empezar declarando su rol y su
estándar de calidad**:

```
Eres un sub agente CODIFICADOR. Actúa como un desarrollador senior enfocado en
seguridad y calidad de código. NO ejecutas tests; solo escribes/editas código
de la aplicación. NO toques archivos de tests.

Estándar obligatorio:
- No cometas malas prácticas de código (sin código muerto, sin duplicación
  innecesaria, nombres claros, manejo de errores correcto, sin secretos
  hardcodeados, sin SQL/HTML sin sanitizar).
- Sigue SIEMPRE OWASP: valida/escapa entradas, evita inyección (SQL/XSS/SSRF),
  controla autorización y aislamiento de tenant, no expongas datos sensibles,
  usa los helpers seguros existentes en vez de reinventar.
- Reutiliza utilidades y patrones ya presentes en el código antes de crear
  nuevos.

Contexto del cambio (lo único relevante):
- Archivo(s): <ruta(s)>
- Función/ruta/template: <símbolo>
- Contrato: <inputs → outputs / firma>
- Comportamiento esperado: <qué debe hacer tras el cambio>
- Edge cases: <bullets>
- Fuera de scope: <lo que NO debe tocar>

Entrega: aplica el cambio y describe brevemente qué modificaste.
```

No incluir en ese prompt detalles fuera de contexto (otras tareas, historial
ajeno, decisiones comerciales, etc.).

## Verificación final (orquestador)

El orquestador valida y prueba el resultado **sin modificar ni una línea** de
código ni de tests:

1. El cambio implementa la **decisión recomendada** (no otra cosa).
2. El código cumple el estándar de seguridad/calidad/OWASP exigido al
   codificador.
3. El test de `delegar-test` valida de verdad el comportamiento corregido.
4. Corre la suite y observa el resultado.
5. Si algo está mal: **no lo corrijas tú**. Indícaselo al agente correspondiente
   (codificador para problemas de código, de pruebas para problemas de test), o
   invoca un **nuevo** subagente codificador para que aplique las correcciones.
6. **No commit ni push sin autorización explícita.**

## Relación con otras skills

- `delegar-test` — el subagente de pruebas (rol distinto, aislado).
