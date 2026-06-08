# Changelog — analizar-solicitud

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.0.1 - 2026-06-08
- La Fase 2 deja de duplicar el formato de commit: ahora referencia la skill `commit`, con fallback a un commit normal si no está disponible.
- La convención de rama y la higiene de git se referencian a la skill `iniciar-solicitud` en lugar de repetirse.
- Se simplifican notas redundantes sobre la salida por consola.

## 1.0.0 - 2026-06-08
- Versión inicial: análisis de solicitud (solo lectura) + ejecución opcional de la decisión.
- La salida (acción ejecutada y texto al cliente) se entrega por consola; no se registra en bitácora ni sistemas externos.
