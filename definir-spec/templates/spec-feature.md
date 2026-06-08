<!--
  FORMATO CANÓNICO — Spec de Feature. Rellenar los <placeholders> y borrar estos
  comentarios. NO cambiar la estructura de secciones ni su numeración: la salida
  debe ser idéntica en formato todas las veces. Quitar filas/secciones opcionales
  solo si de verdad no aplican.
-->
# Documento de Especificación de Requerimiento

## <Producto> — <Título del requerimiento>

| Campo | Valor |
|-------|-------|
| Solicitud | #<id o "—"> |
| Título original | <título tal como llegó> |
| Producto / Módulo | <producto / dominio> |
| Fecha | <YYYY-MM-DD> |
| Estado | Especificación para revisión (pendiente de aprobación) |
| Marco legal | <normas aplicables, si corresponde — si no, quitar fila> |
| Insumo | <fuente del requerimiento, si corresponde — si no, quitar fila> |

---

# 1 — Descripción del requerimiento (nivel usuario)

## 1.1 Contexto
<situación actual y por qué surge la necesidad>

## 1.2 Qué se necesita
<el cambio en lenguaje de negocio, sin tecnicismos>

## 1.3 Escenarios cubiertos
- **<escenario A>:** <descripción>
- **<escenario B>:** <descripción>

## 1.4 Cómo lo verá el usuario
<recorrido por actor (ej. usuario final, administrador), en pasos numerados>

## 1.5 Decisiones adoptadas
<asunciones funcionales ya validadas con el usuario — una por fila>

| Decisión | Detalle |
|----------|---------|
| <decisión> | <detalle> |

## 1.6 Fuera de alcance
- <lo que explícitamente NO entra>

---

# 2 — Especificación técnica

## 2.1 Clasificación del cambio

| Atributo | Valor |
|----------|-------|
| Tipo | <Nuevo feature / Mejora / etc.> |
| Impacta flujo / comportamiento | <Sí/No — detalle> |
| Impacta datos / esquema / procesos | <Sí/No — detalle> |
| Tamaño estimado | <Chico / Mediano / Grande> |

## 2.2 Requerimientos funcionales

| ID | Requerimiento |
|----|---------------|
| RF-01 | <requerimiento verificable> |
| RF-02 | <...> |

## 2.3 Casos de uso

### CU-01 — <nombre>
- **Actor:** <actor>
- **Precondición:** <...>
- **Flujo:** <pasos>
- **Postcondición:** <...>

## 2.4 Criterios de aceptación (BDD / Gherkin)
<!--
  Escenarios en Gherkin español (Dado / Cuando / Entonces). Un escenario por
  comportamiento verificable, mapeado a los RF de §2.2. Incluir SIEMPRE al menos
  un escenario de regresión (lo que NO debe cambiar) y los caminos de error.
  Son la base de los tests de aceptación.
-->
```gherkin
Característica: <nombre del feature>

  Escenario: <camino feliz — RF-01>
    Dado <contexto/precondición>
    Cuando <acción del actor>
    Entonces <resultado observable esperado>

  Escenario: <caso de error / validación>
    Dado <contexto>
    Cuando <acción inválida>
    Entonces <mensaje/comportamiento de rechazo>

  Escenario: <regresión — comportamiento existente intacto>
    Dado <estado previo>
    Cuando <acción que ya existía>
    Entonces <se mantiene el comportamiento anterior>
```

## 2.5 Modelo de datos / cambios técnicos
<tablas/columnas nuevas o modificadas, rutas, servicios; o "Sin cambios de datos">

## 2.6 Consideraciones
- **Regresión:** <comportamiento existente a preservar>
- **Seguridad:** <validación, autorización, aislamiento — OWASP>
- **Migración:** <si aplica>
