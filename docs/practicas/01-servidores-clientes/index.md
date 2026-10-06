# Práctica 1 - Servidores y Clientes

**ABD PRÁCTICA 26/27 · Instalación de Servidores y Clientes**

<span class="estado estado--desarrollo">En desarrollo</span> · Duración estimada: **3 semanas** · Puntuación máxima: **50 puntos**

## Objetivo

Aprender la instalación y configuración de diferentes servidores y clientes de bases de datos.

## Puntuación

| Parte | Puntos |
|---|---|
| Responsabilidad individual | 30 |
| Responsabilidad grupal | 15 |
| Ejecución de roles | 5 |
| **Total** | **50** |

## Requisitos generales

- Tras instalar cada servidor, crear una base de datos con **al menos tres tablas o colecciones** y poblarla adecuadamente.
- Crear un usuario con los privilegios necesarios para acceder remotamente a los datos.
- Compartir la información de conexión con el grupo cuando sea necesario, pero **nunca publicar contraseñas reales en el blog**.
- Los clientes deben estar en **máquinas diferentes** de los servidores.
- Documentar toda la configuración.
- Aportar pruebas del funcionamiento remoto.
- Entregar el código de las aplicaciones y pruebas de funcionamiento.

!!! question "Consulta pendiente al profesor"
    El requisito de «tres tablas o colecciones» no se aplica igual a sistemas con otro modelo de datos (por ejemplo Redis, Memcached, Neo4j o Cassandra). **No se ha decidido cómo interpretarlo**: se trasladará al profesor a través del portavoz y la respuesta se anotará aquí.

## Responsabilidades individuales comunes

Cada uno de los tres alumnos debe instalar, con acceso remoto desde la red local:

- Oracle 23ai o superior sobre Debian 13 o superior.
- PostgreSQL.
- MySQL.
- MongoDB.

Una instalación compartida no sustituye automáticamente a estas tres responsabilidades individuales.

## Responsabilidades por alumno

=== "Alumno 1"

    - Instalar Cassandra y demostrar su funcionamiento básico.
    - Aplicación web que conecte con **MongoDB** desde un cliente remoto tras autenticarse, muestre las colecciones accesibles para el usuario y permita consultar los documentos de alguna colección.
    - Opcional: demostrar NoSQL Injection en un laboratorio autorizado, explicar mitigaciones y demostrar la corrección.

=== "Alumno 2"

    - Instalar Redis y demostrar su funcionamiento básico.
    - Aplicación web que conecte con **MySQL** desde un cliente remoto tras autenticarse, muestre las tablas accesibles y permita consultar registros.
    - Opcional: demostrar SQL Injection en un laboratorio autorizado, explicar mitigaciones y demostrar la corrección.

=== "Alumno 3"

    - Instalar Neo4j y demostrar su funcionamiento básico.
    - Aplicación web que conecte con **PostgreSQL** tras autenticarse, respetando el requisito de cliente remoto, muestre las tablas accesibles y permita consultar registros.
    - Opcional: demostrar SQL Injection en un laboratorio autorizado, explicar mitigaciones y demostrar la corrección.

Quién es Alumno 1, 2 y 3 está **pendiente de asignar** (ver [Organización y seguimiento](../../organizacion.md)).

## Responsabilidad grupal

- Instalación, uso básico y explicación de **CouchDB**.
- Instalación, uso básico y explicación de **Memcached**.
- **SQL Developer** como cliente remoto de Oracle mediante conexión TNS.
- Vídeo de instalación de una herramienta web de administración de **PostgreSQL** y demostración desde un cliente remoto.
- Vídeo equivalente para **MySQL**.
- Vídeo equivalente para **MongoDB**.
- Videocomparativa de los SGBD no relacionales utilizados (MongoDB, Cassandra, Redis, Neo4j, CouchDB y Memcached): ventajas, inconvenientes y casos de uso.

## Roles

| Rol | Funciones |
|---|---|
| Capitán | Planificar, coordinar y facilitar la circulación de información. |
| Portavoz | Trasladar dudas al profesor y comunicar las respuestas al grupo. |
| Secretario | Comprobar que la documentación sea completa, clara y correcta. |

## Rúbrica

**Oracle:** parámetros de arranque en SPFILE · nombre de instancia y servicio · arranque automático · listener · TNSNAMES.ORA.

**Aplicaciones:** pantalla de autenticación · configuración de conexión · acceso según permisos · modificaciones del código · pruebas.

**Sistemas no relacionales:** instalación · configuración inicial · gestión de usuarios cuando corresponda · creación de datos · inserción · consulta.

**Inyección SQL / NoSQL (opcional):** definición · variantes · demostración controlada · corrección · prueba posterior a la corrección.

## Apartados y documentación

| Apartado | Estado | Documentación |
|---|---|---|
| Oracle | <span class="estado estado--desarrollo">En desarrollo</span> | [Oracle Database 26ai](01-oracle/index.md) |
| PostgreSQL | <span class="estado estado--pendiente">Pendiente</span> | Sin documentos todavía |
| MySQL | <span class="estado estado--pendiente">Pendiente</span> | Sin documentos todavía |
| MongoDB | <span class="estado estado--pendiente">Pendiente</span> | Sin documentos todavía |
| Cassandra, Redis, Neo4j | <span class="estado estado--pendiente">Pendiente</span> | Sin documentos todavía |
| CouchDB y Memcached | <span class="estado estado--pendiente">Pendiente</span> | Sin documentos todavía |
| Vídeos y comparativa | <span class="estado estado--pendiente">Pendiente</span> | Sin documentos todavía |

Los apartados nuevos aparecen en el menú en cuanto se sube su carpeta con algún `.md` (ver [guía de contribución](../../contribuir.md)).
