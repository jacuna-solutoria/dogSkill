# Changelog — delegar-calidad

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.0.0 - 2026-06-10
- Versión inicial. Rol subagente revisor de calidad (solo lectura): revisa el
  cambio buscando malas prácticas y entrega hallazgos priorizados, sin corregir.
  Subagente distinto del de seguridad (`delegar-seguridad`); el orquestador
  (`delegar-codigo`) lo invoca y delega las correcciones a un codificador.
