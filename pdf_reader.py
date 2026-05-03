from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(pdf_path: str | Path) -> str:
    """Extrae texto plano concatenando todas las paginas del PDF."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    pages_text: list[str] = []

    for page in reader.pages:
        pages_text.append(page.extract_text() or "")

    return "\n\n".join(pages_text).strip()


def clamp_text(text: str, max_chars: int = 12000) -> str:
    """Recorta el texto para mantener prompts manejables en modelos locales."""
    if max_chars <= 0:
        return text
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[...text truncated for context window...]"
