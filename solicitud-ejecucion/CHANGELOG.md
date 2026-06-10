# Changelog — solicitud-ejecucion

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.0.0 - 2026-06-10
- Versión inicial. Implementación del cambio recomendado por el análisis: crea la
  rama `T#<num>` (o reutiliza la del worktree), aplica solo lo definido sin
  contradecir la clasificación, valida y commitea (vía `commit`). Proviene de la
  Fase 2 (parte de ejecución) de la antigua `analizar-solicitud`, ahora en la
  cadena `solicitud-*`.
