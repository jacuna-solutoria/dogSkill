# Changelog — solicitud-higiene

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.0.0 - 2026-06-10
- Versión inicial. Higiene de git al tomar una solicitud (verificar rama, pull,
  manejo de rama en curso con los casos continuación/reemplazo/paralelo→`worktree`).
  Surge al separar la antigua `iniciar-solicitud` en la cadena `solicitud-*`
  (higiene → análisis → ejecución → respuesta). No crea la rama de trabajo ni
  modifica código.
