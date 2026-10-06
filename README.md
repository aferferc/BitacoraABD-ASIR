# Bitácora ABD

**Laboratorio de Base de Datos · 2.º ASIR · IES Gonzalo Nazareno · Curso 2026/27**

Blog técnico del grupo formado por **Rube, Alfredo y Juan Carlos** para documentar las prácticas de Base de Datos. Es un sitio estático (MkDocs + Material for MkDocs) que se publica en GitHub Pages.

- Web prevista: <https://juankafdez05.github.io/BitacoraABD-ASIR/> (solo estará operativa cuando el despliegue termine correctamente)
- Licencia: pendiente de acordar.

## Qué hace (y qué no)

Hace: menú generado automáticamente desde `docs/`, buscador, modo claro/oscuro, copiar código, tablas y bloques de aviso, página 404, tests y publicación automática desde `main`.

No hace: no tiene servidor propio, panel de administración, registro de lectores ni analítica. No ejecuta las aplicaciones de las prácticas.

## Cómo se organiza

```text
BitacoraABD-ASIR/
├── docs/                       ← TODO lo que se publica
│   ├── index.md  equipo.md  organizacion.md  contribuir.md
│   ├── assets/                 ← CSS y logotipo
│   └── practicas/
│       └── 01-servidores-clientes/
│           ├── index.md
│           └── 01-oracle/ (index.md, instalacion.md, revision.md)
├── hooks/autonav.py            ← genera el menú solo
├── overrides/404.html          ← página 404
├── plantillas/                 ← plantilla opcional (no se publica)
├── tests/  tools/              ← pruebas y comprobaciones
├── integrity/SHA256SUMS        ← huella del documento original de Oracle
├── mkdocs.yml                  ← configuración de la web
└── .github/workflows/pages.yml ← validación y publicación
```

El código de las aplicaciones de las prácticas irá **fuera de `docs/`** (por ejemplo `apps/mongodb/`, `apps/mysql/`, `apps/postgresql/`), cada una con sus instrucciones y dependencias, separadas de las del blog.

---

## A. Cambiar contenido

**Subir un `.md` es suficiente**: no hace falta front matter, ni editar menús, ni HTML.

Ejemplos de rutas:

| Quiero… | Dónde pongo el archivo |
|---|---|
| Añadir un documento | `docs/practicas/01-servidores-clientes/02-postgresql/instalacion.md` |
| Añadir un apartado | Carpeta nueva `docs/practicas/01-servidores-clientes/03-mysql/` con algún `.md` dentro |
| Añadir una práctica | Carpeta nueva `docs/practicas/02-nombre/` con algún `.md` dentro |
| Añadir un subapartado | `docs/practicas/01-servidores-clientes/02-postgresql/rube/instalacion.md` |
| Resumen de un apartado | `index.md` dentro de la carpeta (opcional) |

Reglas del menú:

- El **primer `#`** del archivo es su título (los `#` dentro de bloques de código no cuentan). Sin `#`, se usa el nombre del archivo.
- `01-`, `02-`… ordenan y no se muestran.
- Las carpetas vacías, las de imágenes (`capturas/`, `imagenes/`, `assets/`…), los archivos ocultos y las carpetas que empiezan por `_` no salen en el menú.
- Los enlaces simbólicos **no se publican**.
- `docs/practicas/index.md` se genera solo; si algún día se escribe uno a mano, manda el escrito.

**Imágenes**: junto al documento, p. ej. `capturas/postgres-remoto.png`, con texto alternativo: `![Conexión remota desde el cliente](capturas/postgres-remoto.png)`.

**Vídeos**: se enlazan, no se suben. **Código**: se enlaza con la dirección de GitHub. Ejemplos y pasos desde la web de GitHub y desde terminal en [`docs/contribuir.md`](docs/contribuir.md).

**Estados y revisiones**: se anotan a mano en `docs/organizacion.md` (Pendiente, En desarrollo, En revisión, Validado). Un `.md` subido no es «Validado» por existir.

**Documento de Oracle**: `docs/practicas/01-servidores-clientes/01-oracle/instalacion.md` es el original del grupo y **no se edita**. Una prueba comprueba su huella (`integrity/SHA256SUMS`). Si se decide actualizarlo a propósito, hay que regenerar la huella: `sha256sum docs/practicas/01-servidores-clientes/01-oracle/instalacion.md` y actualizar ese archivo, explicándolo en el commit.

## B. Cambiar configuración

- Nombre, colores y funciones: `mkdocs.yml` y `docs/assets/extra.css`.
- Orden de la raíz del menú: `extra.autonav.top_order` en `mkdocs.yml`.
- Excluir algo de la **publicación**: `exclude_docs` en `mkdocs.yml`. Excluirlo del **menú** es otra cosa (carpetas de recursos o que empiecen por `_`).
- Versiones: `requirements.txt` (fijadas) y `requirements.lock.txt` (copia exacta de lo probado).

### Desarrollo local (Linux)

```bash
git clone https://github.com/juankafdez05/BitacoraABD-ASIR.git
cd BitacoraABD-ASIR
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

En Windows (PowerShell): `.venv\Scripts\Activate.ps1` en lugar de `source .venv/bin/activate`.

Todos los comandos siguientes son de **terminal** (no son SQL):

```bash
mkdocs serve                       # previsualizar en http://127.0.0.1:8000/BitacoraABD-ASIR/
python -m pytest -q                # ejecutar las pruebas
mkdocs build --strict              # construir producción en site/
python tools/check_site.py site    # comprobar enlaces, recursos y secretos
```

Al construir, Material for MkDocs imprime un aviso informativo sobre MkDocs 2.0. No afecta a este proyecto porque `mkdocs` está fijado en la versión 1.6.1; no actualices `mkdocs` sin revisar ese aviso.

## C. Publicar

La publicación es automática: cada cambio que llega a `main` ejecuta `.github/workflows/pages.yml` (pruebas → construcción → despliegue). Las *pull requests* solo se validan y **no** publican.

Primera vez, desde el ordenador (necesita [GitHub CLI](https://cli.github.com/), `gh auth login` y confirmar la creación del repositorio público):

```bash
bash tools/publicar.sh
```

Si prefieres hacerlo a mano: crea el repositorio vacío en GitHub, súbelo con `git push -u origin main` y en **Settings → Pages → Build and deployment → Source** elige **GitHub Actions**. El campo *Custom domain* se deja **vacío**.

### Fallos comunes

| Síntoma | Qué es | Qué hacer |
|---|---|---|
| El workflow ni arranca; error de sintaxis en `pages.yml` | YAML | Revisar la línea indicada en la pestaña *Actions*. |
| Falla *Instalar dependencias* | Dependencias | Leer el registro; comprobar `requirements*.txt`. |
| Falla *Ejecutar pruebas* | Pruebas | Ejecutar `python -m pytest -q` en local y leer el mensaje. Si falla la huella de Oracle, alguien ha editado el original. |
| Falla *Construir el sitio* | Compilación | Ejecutar `mkdocs build --strict`: suele ser un enlace roto o una imagen que no existe. |
| `Resource not accessible` / error en `deploy` | Permisos | Comprobar que Pages usa **GitHub Actions** como origen. |
| *Waiting for a runner to pick up this job* | Espera de un runner | No significa que haya un error en los archivos ni que esté validado: el trabajo aún no ha empezado. Espera; no lances ejecuciones nuevas una tras otra, porque se encolan. |
| Sitio sin estilos o enlaces rotos al publicar | Rutas | Comprobar que `site_url` en `mkdocs.yml` termina en `/BitacoraABD-ASIR/`. |
| Fallo sin causa clara en archivos | Servicio | Consultar <https://www.githubstatus.com/> antes de concluir nada. |

## Qué no debe publicarse

Contraseñas reales, tokens, claves privadas (`.pem`, `.key`), `.env`, copias de seguridad, volcados con datos reales y capturas con información privada. El `.gitignore`, `exclude_docs` y las pruebas ayudan, pero no sustituyen a revisar lo que se sube.
