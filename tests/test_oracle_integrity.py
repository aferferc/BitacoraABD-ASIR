"""El documento original de Oracle debe conservarse byte a byte."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_oracle_original_intacto():
    sums = (ROOT / "integrity" / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert sums, "integrity/SHA256SUMS está vacío"
    for line in sums:
        expected, rel = line.split(None, 1)
        data = (ROOT / rel.strip().lstrip("*")).read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected, (
            f"{rel} ha cambiado. El original de Oracle no debe editarse; "
            "corrige en un documento aparte (ver revision.md)."
        )


def test_oracle_conserva_crlf_y_titulo():
    data = (ROOT / "docs/practicas/01-servidores-clientes/01-oracle/instalacion.md").read_bytes()
    assert data.startswith("# Instalación de Oracle Database 26ai Enterprise en Debian 13\r\n".encode("utf-8"))
    assert not data.startswith(b"---")  # sin front matter añadido
