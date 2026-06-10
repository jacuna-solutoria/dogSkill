# Changelog — delegar-seguridad

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.0.0 - 2026-06-10
- Versión inicial. Rol subagente revisor de seguridad (solo lectura): revisa el
  cambio siguiendo OWASP (inyección, autorización, aislamiento de tenant,
  secretos, exposición de datos, etc.) y entrega hallazgos priorizados por
  severidad, sin corregir. Subagente distinto del de calidad (`delegar-calidad`);
  el orquestador (`delegar-codigo`) lo invoca y delega las correcciones a un
  codificador.
