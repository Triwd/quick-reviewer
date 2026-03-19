from __future__ import annotations

import re
from pathlib import Path


_HEADING_PATTERN = re.compile(r"^(?:#{1,3}\s|第.+章|第.+节|\d+\.\d*\s)", re.MULTILINE)

_CHUNK_LIMIT = 20_000
_OVERLAP = 500


def read_paper(file_path: Path) -> str:
    """Read paper content from file. Supports .txt, .md, .pdf, .docx."""
    file_path = file_path.resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix in (".txt", ".md"):
        return file_path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        return _read_pdf(file_path)

    if suffix in (".doc", ".docx"):
        return _read_docx(file_path)

    raise ValueError(f"Unsupported file format: {suffix}")


def _read_pdf(file_path: Path) -> str:
    try:
        import pymupdf
    except ImportError:
        raise ImportError(
            "pymupdf is required for PDF support. "
            "Install it with: pip install quick-reviewer[pdf]"
        )

    doc = pymupdf.open(str(file_path))
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n\n".join(pages)


def _read_docx(file_path: Path) -> str:
    try:
        import docx
    except ImportError:
        raise ImportError(
            "python-docx is required for DOCX support. "
            "Install it with: pip install quick-reviewer[docx]"
        )

    doc = docx.Document(str(file_path))
    return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())


def chunk_text(text: str) -> list[str]:
    """Split text into chunks if it exceeds the chunk limit.

    Splits by headings first, then by size. Adjacent chunks overlap ~500 chars.
    """
    if len(text) <= _CHUNK_LIMIT:
        return [text]

    # Split by headings
    sections = _split_by_headings(text)

    # Merge small sections, split large ones
    chunks: list[str] = []
    current = ""

    for section in sections:
        if len(current) + len(section) <= _CHUNK_LIMIT:
            current += section
        else:
            if current:
                chunks.append(current)
            if len(section) > _CHUNK_LIMIT:
                # Split large section by paragraphs
                chunks.extend(_split_by_paragraphs(section))
            else:
                current = section
                continue
            current = ""

    if current:
        chunks.append(current)

    # Add overlap between adjacent chunks
    if len(chunks) > 1:
        chunks = _add_overlap(chunks)

    return chunks


def _split_by_headings(text: str) -> list[str]:
    """Split text at heading boundaries."""
    positions = [m.start() for m in _HEADING_PATTERN.finditer(text)]

    if not positions:
        return [text]

    # Ensure we start from 0
    if positions[0] != 0:
        positions.insert(0, 0)

    sections = []
    for i, pos in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        sections.append(text[pos:end])

    return sections


def _split_by_paragraphs(text: str) -> list[str]:
    """Split a large section by paragraphs, respecting chunk limit."""
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= _CHUNK_LIMIT:
            current = current + "\n\n" + para if current else para
        else:
            if current:
                chunks.append(current)
            current = para

    if current:
        chunks.append(current)

    return chunks


def _add_overlap(chunks: list[str]) -> list[str]:
    """Add overlap between adjacent chunks for context continuity."""
    result = [chunks[0]]
    for i in range(1, len(chunks)):
        prev = chunks[i - 1]
        overlap = prev[-_OVERLAP:] if len(prev) > _OVERLAP else prev
        result.append(overlap + "\n" + chunks[i])
    return result
