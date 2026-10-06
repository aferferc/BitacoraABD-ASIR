"""Navegación automática para Bitácora ABD.

Construye el menú a partir de las carpetas y los archivos Markdown de docs/.
No hace falta front matter ni editar listas de navegación.

Reglas principales (ver README.md):
- El primer H1 fuera de bloques de código es el título del documento.
- Los prefijos numéricos (01-, 02_...) ordenan y no se muestran.
- index.md es opcional y actúa como portada de su sección.
- Carpetas sin Markdown, carpetas de recursos, archivos ocultos y enlaces
  simbólicos no entran en el menú (los enlaces simbólicos tampoco se publican).
"""
from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path

from mkdocs.structure.files import File, Files

log = logging.getLogger("mkdocs.hooks.autonav")

PREFIX_RE = re.compile(r"^(\d+)[-_.\s]+")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
ATX_RE = re.compile(r"^ {0,3}#[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$")
SETEXT_RE = re.compile(r"^ {0,3}=+[ \t]*$")

# Carpetas de recursos: nunca son secciones del menú.
RESOURCE_DIRS = {
    "assets", "img", "images", "imagenes", "imágenes", "recursos", "media",
    "videos", "vídeos", "adjuntos", "capturas", "stylesheets", "javascripts",
}
# Archivos de la raíz de docs/ que no deben salir en el menú.
SKIP_TOP_FILES = {"404.md"}

DEFAULT_TOP_ORDER = ["index.md", "equipo.md", "practicas", "organizacion.md", "contribuir.md"]
TOP_LABELS = {"index.md": "Inicio"}

PRACTICAS_DIR = "practicas"
PRACTICAS_INDEX = f"{PRACTICAS_DIR}/index.md"


# --------------------------------------------------------------------------
# Utilidades de texto
# --------------------------------------------------------------------------
def _plain(text: str) -> str:
    """Quita marcas Markdown sencillas de un título."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_]{1,3}", "", text)
    return text.strip()


def first_h1(text: str) -> str | None:
    """Devuelve el primer H1 válido (ignora bloques de código y front matter)."""
    lines = text.lstrip("\ufeff").splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() in ("---", "..."):
                i = j + 1
                break
    fence: tuple[str, int] | None = None
    prev = ""
    in_comment = False
    for line in lines[i:]:
        if in_comment:
            if "-->" in line:
                in_comment = False
            prev = ""
            continue
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence = (m.group(1)[0], len(m.group(1)))
            prev = ""
            continue
        if fence is not None:
            stripped = line.strip()
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= fence[1]:
                fence = None
            continue
        if line.lstrip().startswith("<!--") and "-->" not in line:
            in_comment = True
            continue
        if line.startswith(("    ", "\t")) and not prev.strip():
            prev = line
            continue  # bloque de código indentado
        m = ATX_RE.match(line)
        if m:
            title = _plain(m.group(1))
            if title:
                return title
        elif SETEXT_RE.match(line) and prev.strip() and not prev.startswith("#"):
            title = _plain(prev)
            if title:
                return title
        prev = line
    return None


def clean_label(name: str) -> str:
    """Etiqueta legible a partir de un nombre de archivo o carpeta."""
    stem = name[:-3] if name.lower().endswith(".md") else name
    stem = PREFIX_RE.sub("", stem)
    stem = re.sub(r"[-_]+", " ", stem).strip()
    return stem[:1].upper() + stem[1:] if stem else name


def sort_key(name: str) -> tuple:
    m = PREFIX_RE.match(name)
    base = unicodedata.normalize("NFKD", PREFIX_RE.sub("", name)).casefold()
    return (0, int(m.group(1)), base, name) if m else (1, 0, base, name)


# --------------------------------------------------------------------------
# Descubrimiento
# --------------------------------------------------------------------------
def _is_safe(path: Path, docs_root: Path) -> bool:
    """False para ocultos, enlaces simbólicos o rutas que salen de docs/."""
    if path.name.startswith(".") or path.is_symlink():
        return False
    try:
        path.resolve().relative_to(docs_root.resolve())
    except ValueError:
        return False
    return True


def _read_title(path: Path) -> str | None:
    try:
        return first_h1(path.read_bytes().decode("utf-8", errors="replace"))
    except OSError:
        return None


def _dir_entries(directory: Path, docs_root: Path):
    dirs, files = [], []
    for child in sorted(directory.iterdir(), key=lambda p: sort_key(p.name)):
        if not _is_safe(child, docs_root):
            continue
        if child.is_dir():
            if child.name.lower() in RESOURCE_DIRS or child.name.startswith("_"):
                continue
            dirs.append(child)
        elif child.suffix.lower() == ".md" and child.name.lower() != "index.md":
            files.append(child)
    return dirs, files


def _section(directory: Path, docs_root: Path, virtual_h1: dict[str, str]):
    """Devuelve (etiqueta, [hijos]) o None si la carpeta no tiene Markdown."""
    rel = directory.relative_to(docs_root).as_posix()
    index = directory / "index.md"
    has_index = index.is_file() and _is_safe(index, docs_root)
    index_rel = f"{rel}/index.md"
    dirs, files = _dir_entries(directory, docs_root)

    children = []
    for item in sorted(dirs + files, key=lambda p: sort_key(p.name)):
        if item.is_dir():
            sub = _section(item, docs_root, virtual_h1)
            if sub:
                children.append({sub[0]: sub[1]})
        else:
            irel = item.relative_to(docs_root).as_posix()
            children.append({_read_title(item) or clean_label(item.name): irel})

    virtual = (not has_index) and index_rel in virtual_h1
    if not children and not has_index and not virtual:
        return None  # carpeta vacía (o solo recursos): no aparece

    if has_index:
        label = _read_title(index) or clean_label(directory.name)
        children.insert(0, index_rel)
    elif virtual:
        label = virtual_h1[index_rel]
        children.insert(0, index_rel)
    else:
        label = clean_label(directory.name)
    return label, children


def build_nav(docs_dir: str | Path, top_order: list[str] | None = None,
              virtual_h1: dict[str, str] | None = None) -> list:
    """Construye la estructura `nav` de MkDocs a partir de docs/."""
    docs_root = Path(docs_dir)
    virtual_h1 = virtual_h1 or {}
    top_order = top_order or DEFAULT_TOP_ORDER
    entries: dict[str, object] = {}

    for child in sorted(docs_root.iterdir(), key=lambda p: sort_key(p.name)):
        if not _is_safe(child, docs_root):
            continue
        if child.is_dir():
            if child.name.lower() in RESOURCE_DIRS or child.name.startswith("_"):
                continue
            sec = _section(child, docs_root, virtual_h1)
            if sec:
                entries[child.name] = {sec[0]: sec[1]}
        elif child.suffix.lower() == ".md" and child.name not in SKIP_TOP_FILES:
            label = TOP_LABELS.get(child.name) or _read_title(child) or clean_label(child.name)
            entries[child.name] = {label: child.name}

    ordered = [entries.pop(k) for k in top_order if k in entries]
    ordered += [entries[k] for k in sorted(entries, key=sort_key)]
    return ordered


def count_documents(nav) -> int:
    total = 0
    for item in nav:
        if isinstance(item, str):
            total += 0 if item.endswith("index.md") else 1
        elif isinstance(item, dict):
            for value in item.values():
                total += count_documents(value) if isinstance(value, list) else (
                    0 if value.endswith("index.md") else 1)
    return total


# --------------------------------------------------------------------------
# Índice de prácticas generado (solo si el grupo no escribe practicas/index.md)
# --------------------------------------------------------------------------
GENERATED_H1 = "Prácticas"


def _practice_cards(docs_root: Path) -> str:
    base = docs_root / PRACTICAS_DIR
    out = [
        f"# {GENERATED_H1}",
        "",
        "Esta lista se genera automáticamente a partir de las carpetas de "
        "`docs/practicas/`. Cada práctica nueva aparece aquí sin tocar ningún "
        "archivo de navegación.",
        "",
    ]
    cards = []
    if base.is_dir():
        for d in sorted(base.iterdir(), key=lambda p: sort_key(p.name)):
            if not d.is_dir() or not _is_safe(d, docs_root) or d.name.lower() in RESOURCE_DIRS:
                continue
            sec = _section(d, docs_root, {})
            if not sec:
                continue
            label, children = sec
            n = count_documents([{label: children}])
            target = children[0] if isinstance(children[0], str) else None
            if target is None:
                first = children[0]
                target = next(iter(first.values()))
                while isinstance(target, list):
                    target = target[0] if isinstance(target[0], str) else next(iter(target[0].values()))
            href = Path(target).relative_to(PRACTICAS_DIR).as_posix()
            plural = "documento" if n == 1 else "documentos"
            cards.append(f"-   **[{label}]({href})**\n\n    {n} {plural} publicados.")
    if cards:
        out.append('<div class="grid cards" markdown>\n')
        out.extend(c + "\n" for c in cards)
        out.append("</div>")
    else:
        out.append("Todavía no hay prácticas publicadas.")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# Eventos de MkDocs
# --------------------------------------------------------------------------
def _top_order(config) -> list[str]:
    extra = config.get("extra") or {}
    return list((extra.get("autonav") or {}).get("top_order") or DEFAULT_TOP_ORDER)


def on_files(files: Files, config):
    docs_root = Path(config["docs_dir"])

    # 1) Seguridad: no publicar enlaces simbólicos ni nada fuera de docs/.
    for f in list(files):
        src = Path(f.abs_src_path) if f.abs_src_path else None
        # Solo se vigilan los archivos de docs/ (no los del tema ni los generados).
        if src is None or not f.src_dir or Path(f.src_dir) != docs_root:
            continue
        unsafe = False
        cur = src
        while cur != docs_root and cur != cur.parent:
            if cur.is_symlink():
                unsafe = True
                break
            cur = cur.parent
        if not unsafe:
            try:
                src.resolve().relative_to(docs_root.resolve())
            except ValueError:
                unsafe = True
        if unsafe:
            log.info("Se omite (enlace simbólico o fuera de docs/): %s", f.src_uri)
            files.remove(f)

    # 2) Índice de prácticas generado si el grupo no lo ha escrito.
    virtual: dict[str, str] = {}
    if (docs_root / PRACTICAS_DIR).is_dir() and files.get_file_from_path(PRACTICAS_INDEX) is None:
        content = _practice_cards(docs_root)
        files.append(File.generated(config, PRACTICAS_INDEX, content=content))
        virtual[PRACTICAS_INDEX] = GENERATED_H1

    # 3) Menú automático (se recalcula en cada compilación).
    config["nav"] = build_nav(docs_root, _top_order(config), virtual)
    return files
