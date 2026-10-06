"""Construye el sitio de producción y lo comprueba bajo /BitacoraABD-ASIR/."""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import check_site

ROOT = Path(__file__).resolve().parent.parent
BASE = "/BitacoraABD-ASIR/"


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    out = tmp_path_factory.mktemp("build") / "site"
    res = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-d", str(out)],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    # Los avisos propios (WARNING) no deben existir; el aviso informativo de Material no cuenta.
    assert "WARNING" not in (res.stdout + res.stderr)
    return out


def test_paginas_principales_existen(site):
    for rel in ("index.html", "equipo/index.html", "organizacion/index.html", "contribuir/index.html",
                "practicas/index.html", "practicas/01-servidores-clientes/index.html",
                "practicas/01-servidores-clientes/01-oracle/instalacion/index.html",
                "practicas/01-servidores-clientes/01-oracle/revision/index.html", "404.html"):
        assert (site / rel).is_file(), rel


def test_enlaces_recursos_y_ancla_bajo_ruta_base(site):
    assert check_site.check_links(site, BASE) == []


def test_404_coherente(site):
    assert check_site.check_404(site, BASE) == []


def test_sin_secretos_ni_archivos_internos(site):
    assert check_site.check_secrets(site) == []
    for name in (".env", "mkdocs.yml", "requirements.txt", ".git"):
        assert not (site / name).exists()


def test_oracle_publicado_con_mismo_contenido(site):
    page = (site / "practicas/01-servidores-clientes/01-oracle/instalacion/index.html").read_text(encoding="utf-8")
    assert "Instalación de Oracle Database 26ai Enterprise en Debian 13" in page
    assert "CV_ASSUME_DISTID" in page


def test_sin_recursos_externos(site):
    index = (site / "index.html").read_text(encoding="utf-8")
    assert "fonts.googleapis.com" not in index
    assert "google-analytics" not in index


def test_documento_nuevo_se_publica_sin_tocar_navegacion(tmp_path):
    work = tmp_path / "proyecto"
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(".venv", "site", ".git", "__pycache__", ".pytest_cache"))
    nuevo = work / "docs/practicas/02-prueba/01-apartado/Instalación con tilde.md"
    nuevo.parent.mkdir(parents=True)
    nuevo.write_text("Sin título.\n\n## Subtítulo\n", encoding="utf-8")
    out = tmp_path / "site"
    res = subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict", "-d", str(out)],
                         cwd=work, capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "WARNING" not in res.stdout + res.stderr
    idx = (out / "practicas/index.html").read_text(encoding="utf-8")
    assert "Prueba" in idx                      # tarjeta de la práctica nueva
    assert "Instalación con tilde" in idx       # documento sin H1: etiqueta desde el nombre
    assert (out / "practicas/02-prueba/01-apartado/Instalación con tilde/index.html").is_file() or \
        any("tilde" in str(p) for p in out.rglob("index.html"))
    assert check_site.check_links(out, BASE) == []
