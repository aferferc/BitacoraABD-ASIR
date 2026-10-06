# Notas de revisión de la instalación de Oracle

Este documento **no sustituye ni corrige** [la guía original](instalacion.md), que se conserva sin cambios. Recoge lo que se ve al leerla y lo que queda por comprobar.

!!! info "Alcance"
    Revisión de lectura del texto. No se ha ejecutado ninguna instalación de Oracle para preparar este documento.

## Observaciones verificadas en el texto

Son hechos que se pueden comprobar leyendo la guía.

| Observación | Dónde |
|---|---|
| Usa marcadores `<PASSWORD>` en lugar de contraseñas reales. Es lo esperado para un documento público. | Secciones 3 y 6 |
| Pasa contraseñas como argumentos de comandos (`dbca`, `sqlplus system/<PASSWORD>@…`). Al ejecutarlo en un equipo real, esas contraseñas pueden quedar en el historial o en la lista de procesos. | Secciones 3 y 6 |
| Aplica `chmod -R 775 /u01`. Conviene documentar por qué se eligen esos permisos. | Sección 2 |
| No contiene capturas ni salidas de terminal reales. | Todo el documento |
| Cubre la instalación local y la verificación local; no incluye una prueba de acceso remoto desde otra máquina ni la conexión de SQL Developer por TNS, que pide la práctica. | Sección 6 |
| La guía indica que Debian no es una distribución certificada por Oracle y que se omiten comprobaciones del instalador. | Aviso inicial |

## Dudas pendientes de contrastar con la documentación oficial

Estas **no son correcciones**: son puntos a verificar antes de darlos por buenos.

1. Si el uso de `CV_ASSUME_DISTID=OL8` y `-ignorePrereqFailure` es adecuado para Oracle Database 26ai en Debian 13.
2. Si los valores de parámetros del kernel y límites del sistema coinciden con los que recomienda Oracle para esta versión.
3. Si es preferible la opción de la gold image tal como se describe o el instalador estándar.
4. Si los pasos de arranque automático con `systemd` son los adecuados para esta versión.
5. Si hay que abrir el puerto del listener en un cortafuegos para el acceso remoto desde la red local.

## Siguientes pasos

- Asignar un revisor (rol de secretario u otra persona del grupo).
- Añadir capturas y salidas reales cuando se ejecute la instalación.
- Registrar el resultado en [Organización y seguimiento](../../../organizacion.md).
