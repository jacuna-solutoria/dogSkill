# Changelog — solicitud-analisis

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.0.0 - 2026-06-10
- Versión inicial. Análisis solo lectura de una solicitud (clasificación + detalle
  + recomendación), con la salida escrita en `analisis.md` (scratch, agregado a
  `info/exclude` para no commitearlo) que `worktree` puede copiar a una carpeta
  nueva y así no re-analizar. Reúne el análisis de las antiguas `iniciar-solicitud`
  y `analizar-solicitud` (Fase 1) en la cadena `solicitud-*`.
