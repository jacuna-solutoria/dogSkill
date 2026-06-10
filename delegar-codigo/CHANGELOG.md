# Changelog — delegar-codigo

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.1.0 - 2026-06-10
- Se aclara que el **orquestador es siempre el agente principal** (el que chatea
  con el usuario), no uno spawneado aparte. Se agrega la fase de **revisión**: el
  orquestador delega calidad y seguridad a subagentes distintos y solo lectura
  (`delegar-calidad`, `delegar-seguridad`) y delega las correcciones de los
  hallazgos a nuevos subagentes codificadores, re-revisando hasta dejar en verde
  antes del commit.

## 1.0.0 - 2026-06-08
- Versión inicial.
