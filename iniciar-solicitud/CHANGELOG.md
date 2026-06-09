# Changelog — iniciar-solicitud

Todas las versiones de esta skill. Formato basado en [SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

## 1.1.0 - 2026-06-09
- Paso 1: si ya estás en una rama `T#...`, antes de hacer checkout se pregunta cómo
  seguir con tres salidas explícitas: (1) continuación del mismo trabajo (no se
  cambia nada), (2) solicitud nueva que reemplaza el contexto → rama nueva desde la
  base, (3) solicitud nueva en paralelo → deriva a la skill `worktree` (no cambia
  de rama en la carpeta compartida).

## 1.0.1 - 2026-06-08
- Se generalizan los ejemplos de nombre de rama a un dominio neutro (login).

## 1.0.0 - 2026-06-08
- Versión inicial.
