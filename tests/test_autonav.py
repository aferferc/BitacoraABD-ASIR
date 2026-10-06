"""Pruebas de la navegación automática (hooks/autonav.py)."""
import os

import pytest

import autonav


def write(root, rel, text="# T\n"):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def flat(nav, out=None):
    out = [] if out is None else out
    for item in nav:
        if isinstance(item, str):
            out.append(item)
        else:
            for v in item.values():
                flat(v, out) if isinstance(v, list) else out.append(v)
    return out


def labels(nav):
    res = []
    for item in nav:
        if isinstance(item, dict):
            for k, v in item.items():
                res.append(k)
                if isinstance(v, list):
                    res.extend(labels(v))
    return res


# --- títulos -------------------------------------------------------------
def test_h1_basico_y_tildes():
    assert autonav.first_h1("texto\n# Instalación de Oracle\n") == "Instalación de Oracle"


def test_h1_dentro_de_bloque_de_codigo_se_ignora():
    md = "```bash\n# comentario de shell\n```\n\n# Título real\n"
    assert autonav.first_h1(md) == "Título real"


def test_h1_en_bloque_con_tildes_y_cuatro_comillas():
    md = "~~~\n# no\n~~~\n````md\n```\n# tampoco\n```\n````\n# Sí\n"
    assert autonav.first_h1(md) == "Sí"


def test_h1_con_crlf_y_front_matter():
    md = "---\ntitle: x\n---\r\n# Con CRLF\r\n"
    assert autonav.first_h1(md) == "Con CRLF"


def test_sin_h1_devuelve_none_y_h2_no_cuenta():
    assert autonav.first_h1("## Solo H2\ntexto") is None


def test_etiqueta_desde_nombre():
    assert autonav.clean_label("03-guia-rapida.md") == "Guia rapida"
    assert autonav.clean_label("02_instalación.md") == "Instalación"


# --- estructura ----------------------------------------------------------
def test_documento_nuevo_aparece_sin_editar_nada(tmp_path):
    write(tmp_path, "index.md", "# Inicio\n")
    nav = autonav.build_nav(tmp_path, ["index.md", "practicas"])
    assert "practicas/01-x/doc.md" not in flat(nav)
    write(tmp_path, "practicas/01-x/doc.md", "# Doc nuevo\n")
    nav = autonav.build_nav(tmp_path, ["index.md", "practicas"])
    assert "practicas/01-x/doc.md" in flat(nav)
    assert "Doc nuevo" in labels(nav)


def test_practica_nueva_y_subapartados_anidados(tmp_path):
    write(tmp_path, "practicas/02-otra/servidor/integrante/instalacion.md", "# Instalación\n")
    write(tmp_path, "practicas/02-otra/servidor/integrante/pruebas.md", "# Pruebas\n")
    nav = autonav.build_nav(tmp_path)
    assert "practicas/02-otra/servidor/integrante/instalacion.md" in flat(nav)
    assert {"Servidor": [{"Integrante": [
        {"Instalación": "practicas/02-otra/servidor/integrante/instalacion.md"},
        {"Pruebas": "practicas/02-otra/servidor/integrante/pruebas.md"}]}]} in flat_sections(nav)


def flat_sections(nav):
    out = []
    for item in nav:
        if isinstance(item, dict):
            for k, v in item.items():
                if isinstance(v, list):
                    out.append({k: v})
                    out.extend(flat_sections(v))
    return out


def test_orden_por_prefijo_numerico_y_no_alfabetico(tmp_path):
    for n in ("10-diez", "02-dos", "01-uno"):
        write(tmp_path, f"p/{n}.md", f"# {n}\n")
    write(tmp_path, "p/sin-prefijo.md", "# Sin prefijo\n")
    order = flat(autonav.build_nav(tmp_path))
    assert order == ["p/01-uno.md", "p/02-dos.md", "p/10-diez.md", "p/sin-prefijo.md"]


def test_los_prefijos_no_aparecen_en_etiquetas(tmp_path):
    write(tmp_path, "p/01-a/01-doc.md", "")  # sin H1
    ls = labels(autonav.build_nav(tmp_path))
    assert ls == ["P", "A", "Doc"]  # "P" es la carpeta raíz del ejemplo


def test_documento_sin_h1_usa_nombre_de_archivo(tmp_path):
    write(tmp_path, "p/01-configuración-inicial.md", "solo texto\n## H2\n")
    assert "Configuración inicial" in labels(autonav.build_nav(tmp_path))


def test_index_opcional_y_sin_duplicar(tmp_path):
    write(tmp_path, "p/01-con/index.md", "# Con resumen\n")
    write(tmp_path, "p/01-con/a.md", "# A\n")
    write(tmp_path, "p/02-sin/b.md", "# B\n")
    nav = autonav.build_nav(tmp_path)
    paths = flat(nav)
    assert paths.count("p/01-con/index.md") == 1
    assert "p/02-sin/index.md" not in paths
    sec = next(s for s in flat_sections(nav) if "Con resumen" in s)
    assert sec["Con resumen"][0] == "p/01-con/index.md"  # portada de la sección, no entrada extra
    assert "Sin" in labels(nav)


def test_carpetas_vacias_y_de_recursos_no_aparecen(tmp_path):
    (tmp_path / "p/01-vacia").mkdir(parents=True)
    (tmp_path / "p/02-solo-imagenes/capturas").mkdir(parents=True)
    (tmp_path / "p/02-solo-imagenes/capturas/a.png").write_bytes(b"\x89PNG")
    write(tmp_path, "p/03-ok/doc.md", "# Doc\n")
    write(tmp_path, "p/03-ok/capturas/leeme.md", "# No soy un artículo\n")
    write(tmp_path, "p/03-ok/imagenes/otro.md", "# Tampoco\n")
    nav = autonav.build_nav(tmp_path)
    assert flat(nav) == ["p/03-ok/doc.md"]
    assert "Vacia" not in labels(nav)


def test_imagenes_no_son_articulos(tmp_path):
    write(tmp_path, "p/doc.md", "# Doc\n")
    (tmp_path / "p/captura.png").write_bytes(b"\x89PNG")
    assert flat(autonav.build_nav(tmp_path)) == ["p/doc.md"]


def test_titulos_iguales_en_secciones_distintas(tmp_path):
    write(tmp_path, "p/01-a/instalacion.md", "# Instalación\n")
    write(tmp_path, "p/02-b/instalacion.md", "# Instalación\n")
    nav = autonav.build_nav(tmp_path)
    assert flat(nav) == ["p/01-a/instalacion.md", "p/02-b/instalacion.md"]
    assert labels(nav).count("Instalación") == 2


def test_archivos_y_carpetas_ocultos_se_ignoran(tmp_path):
    write(tmp_path, "p/.oculto.md", "# Oculto\n")
    write(tmp_path, "p/.git-cosas/doc.md", "# Oculto 2\n")
    write(tmp_path, "p/_borradores/doc.md", "# Borrador\n")
    write(tmp_path, "p/visible.md", "# Visible\n")
    assert flat(autonav.build_nav(tmp_path)) == ["p/visible.md"]


def test_orden_superior_configurable_y_404_fuera(tmp_path):
    for f in ("index.md", "equipo.md", "contribuir.md", "404.md", "zeta.md"):
        write(tmp_path, f, f"# {f}\n")
    write(tmp_path, "practicas/a.md", "# A\n")
    nav = autonav.build_nav(tmp_path, ["index.md", "equipo.md", "practicas", "contribuir.md"])
    assert flat(nav) == ["index.md", "equipo.md", "practicas/a.md", "contribuir.md", "zeta.md"]
    assert "404.md" not in flat(nav)


def test_determinista(tmp_path):
    for n in ("b", "a", "c"):
        write(tmp_path, f"p/{n}.md", f"# {n}\n")
    assert autonav.build_nav(tmp_path) == autonav.build_nav(tmp_path)


# --- enlaces simbólicos --------------------------------------------------
@pytest.mark.skipif(not hasattr(os, "symlink"), reason="sin soporte de symlinks")
def test_enlaces_simbolicos_no_entran_ni_escapan(tmp_path):
    docs = tmp_path / "docs"
    outside = tmp_path / "fuera"
    write(outside, "secreto.md", "# Secreto\n")
    write(docs, "p/ok.md", "# OK\n")
    os.symlink(outside / "secreto.md", docs / "p/enlace.md")
    os.symlink(outside, docs / "p/carpeta")
    os.symlink(docs / "p/ok.md", docs / "p/copia-interna.md")
    nav = autonav.build_nav(docs)
    assert flat(nav) == ["p/ok.md"]


def test_on_files_elimina_symlinks(tmp_path):
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import get_files

    docs = tmp_path / "docs"
    outside = tmp_path / "fuera"
    write(outside, "secreto.md", "# Secreto\n")
    write(docs, "index.md", "# Inicio\n")
    os.symlink(outside / "secreto.md", docs / "enlace.md")
    cfg = MkDocsConfig()
    cfg.load_dict({"site_name": "t", "docs_dir": str(docs), "site_dir": str(tmp_path / "site")})
    files = get_files(cfg)
    assert files.get_file_from_path("enlace.md") is not None  # MkDocs lo vería
    out = autonav.on_files(files, cfg)
    assert out.get_file_from_path("enlace.md") is None
    assert out.get_file_from_path("index.md") is not None


# --- índice de prácticas generado ---------------------------------------
def test_indice_generado_determinista_y_sin_pisar_contenido(tmp_path):
    write(tmp_path, "practicas/01-uno/index.md", "# Práctica uno\n")
    write(tmp_path, "practicas/01-uno/a.md", "# A\n")
    write(tmp_path, "practicas/02-dos/b.md", "# B\n")
    text = autonav._practice_cards(tmp_path)
    assert text == autonav._practice_cards(tmp_path)
    assert text.startswith("# Prácticas")
    assert "[Práctica uno](01-uno/index.md)" in text
    assert "[Dos](02-dos/b.md)" in text
    nav = autonav.build_nav(tmp_path, virtual_h1={"practicas/index.md": "Prácticas"})
    assert flat(nav)[0] == "practicas/index.md"
    # Si el grupo escribe su propio index.md, el real manda.
    write(tmp_path, "practicas/index.md", "# Mi índice\n")
    nav = autonav.build_nav(tmp_path, virtual_h1={"practicas/index.md": "Prácticas"})
    assert "Mi índice" in labels(nav)
