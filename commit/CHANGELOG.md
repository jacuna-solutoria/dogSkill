# Changelog — commit

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.1.0 - 2026-06-10
- Se agrega un **gate de pruebas, calidad y seguridad** antes de commitear: si el
  commit toca código, recordar confirmar que existen pruebas que cubren el cambio
  y la suite pasa (`delegar-test`), y que pasó revisión de `delegar-calidad` y
  `delegar-seguridad` (hallazgos corregidos o justificados). Recordatorio, no
  bloqueo; no aplica a commits sin código.

## 1.0.1 - 2026-06-08
- Se generaliza el ejemplo de commit a un dominio neutro (login), sin referencias a proyectos.

## 1.0.0 - 2026-06-08
- Versión inicial.
