# Guía de contribución

Para publicar un documento **basta con subir un archivo `.md`** a la carpeta correcta. No hay que tocar el menú, ni HTML, ni JavaScript, ni añadir cabeceras especiales.

## Cómo se organiza

```text
docs/practicas/
└── 01-servidores-clientes/        ← práctica
    ├── 02-postgresql/             ← apartado
    │   ├── instalacion.md         ← documento
    │   └── capturas/              ← imágenes (no salen en el menú)
    └── 03-mysql/
        └── index.md               ← resumen opcional del apartado
```

- Práctica → apartado → documento. Se pueden anidar más niveles (por ejemplo `servidor/integrante/instalacion.md`).
- El **primer título `#`** del archivo es el nombre que se ve en el menú. Si no hay ninguno, se usa el nombre del archivo.
- Un prefijo numérico (`01-`, `02-`) **sirve para ordenar** y no se muestra.
- `index.md` es opcional: si existe, es la portada del apartado.
- Las carpetas sin Markdown no aparecen.

## Subir un documento desde la web de GitHub

1. Entra en `https://github.com/juankafdez05/BitacoraABD-ASIR` e inicia sesión.
2. Navega por las carpetas hasta `docs/practicas/…` (haz clic en cada carpeta).
3. Pulsa **Add file** (arriba a la derecha) y elige **Upload files** para arrastrar tu `.md`, o **Create new file** para escribirlo allí. Para una carpeta nueva, en *Create new file* escribe `nombre-carpeta/archivo.md` en el nombre.
4. Abajo, en **Commit changes**, escribe un mensaje corto (por ejemplo `Añade instalación de PostgreSQL`).
5. Elige **Create a new branch** y abre una *pull request* si quieres que alguien lo revise antes; elige *Commit directly to the main branch* solo si no hace falta revisión. Al llegar a `main`, la web se publica sola en unos minutos.

## Subir un documento desde terminal

```bash
git clone https://github.com/juankafdez05/BitacoraABD-ASIR.git
cd BitacoraABD-ASIR
git switch -c documentacion-postgresql
mkdir -p docs/practicas/01-servidores-clientes/02-postgresql
cp ~/instalacion.md docs/practicas/01-servidores-clientes/02-postgresql/
git add docs/
git commit -m "Añade instalación de PostgreSQL"
git push -u origin documentacion-postgresql
```

Después abre una *pull request* desde la web de GitHub. Para ver el resultado antes, consulta el [README del repositorio](https://github.com/juankafdez05/BitacoraABD-ASIR#readme).

## Añadir una práctica nueva

Crea la carpeta `docs/practicas/02-nombre-de-la-practica/` y sube dentro al menos un `.md`. Aparecerá en el menú y en el [índice de prácticas](practicas/index.md) automáticamente.

## Imágenes

- Guárdalas junto al documento, por ejemplo en `capturas/`.
- Usa nombres sencillos: `postgresql-conexion-remota.png`.
- Escribe un texto alternativo que describa lo que se ve:

```markdown
![Conexión remota a PostgreSQL desde el cliente](capturas/postgresql-conexion-remota.png)
```

- **Antes de subir una captura**, revisa que no muestre contraseñas, tokens, correos personales ni direcciones privadas.

## Vídeos

Los vídeos **no se suben al repositorio**. Se enlazan desde un documento indicando título y objetivo:

```markdown
**Vídeo:** [Administración web de PostgreSQL](https://example.com/enlace) · Objetivo: mostrar la instalación y una conexión desde un cliente remoto.
```

## Enlazar código de las aplicaciones

El código de las aplicaciones vive fuera de `docs/`, en carpetas propias del repositorio. Desde un documento se enlaza con la dirección completa de GitHub:

```markdown
[Código de la aplicación](https://github.com/juankafdez05/BitacoraABD-ASIR/tree/main/apps/mysql)
```

## Estados y revisiones

El estado de cada tarea (Pendiente, En desarrollo, En revisión, Validado), su responsable, revisor y evidencia se anotan a mano en [Organización y seguimiento](organizacion.md). Un documento solo pasa a *Validado* cuando alguien distinto de quien lo escribió lo ha revisado.

## Plantilla opcional

No es obligatoria. Puedes copiarla de `plantillas/plantilla-documento.md` en el repositorio. Apartados sugeridos: objetivo, autor, entorno, versiones, requisitos, procedimiento, pruebas, problemas encontrados, soluciones, conclusiones y fuentes.

## Qué no se debe publicar

Contraseñas reales, tokens, claves privadas (`.pem`, `.key`), archivos `.env`, copias de seguridad, volcados de bases de datos con datos reales y capturas con información privada.
