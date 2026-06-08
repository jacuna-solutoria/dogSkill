<!--
  FORMATO CANÓNICO — Spec de Fix (bug / corrección). Rellenar los <placeholders>
  y borrar estos comentarios. NO cambiar la estructura ni la numeración: la salida
  debe ser idéntica en formato todas las veces.
-->
# Documento de Especificación de Corrección

## <Producto> — <Título del fix>

| Campo | Valor |
|-------|-------|
| Solicitud | #<id o "—"> |
| Título original | <título tal como llegó> |
| Producto / Módulo | <producto / dominio> |
| Fecha | <YYYY-MM-DD> |
| Severidad | <baja / media / alta> |
| Estado | Especificación para revisión (pendiente de aprobación) |

---

# 1 — Problema (nivel usuario)

## 1.1 Síntoma observado
<qué ve el usuario que está mal>

## 1.2 Cuándo ocurre
<pasos para reproducir / condiciones que lo disparan>

## 1.3 Comportamiento esperado vs actual
- **Esperado:** <...>
- **Actual:** <...>

## 1.4 Impacto
<a quién afecta, con qué frecuencia, gravedad>

---

# 2 — Análisis técnico

## 2.1 Causa raíz
<la causa real, no el síntoma — lógica concreta responsable>

## 2.2 Archivos / componentes afectados y por qué

| Archivo / componente | Cambio | Por qué |
|----------------------|--------|---------|
| <ruta (función/ruta/template)> | <qué se modifica> | <motivo> |

## 2.3 Corrección propuesta
<el enfoque de la corrección>

## 2.4 Criterios de aceptación (BDD / Gherkin)
<!--
  Escenario que reproduce el bug y describe el comportamiento correcto tras el
  fix; más al menos un escenario de regresión. Son la base del test que valida
  la corrección.
-->
```gherkin
Característica: <área afectada>

  Escenario: <el bug, ya corregido>
    Dado <condiciones que reproducían el error>
    Cuando <acción que lo disparaba>
    Entonces <comportamiento correcto esperado (ya no falla)>

  Escenario: <regresión — lo que debe seguir funcionando>
    Dado <estado previo>
    Cuando <acción relacionada>
    Entonces <comportamiento intacto>
```

## 2.5 Fuera de alcance
- <lo que NO se aborda en esta corrección>
