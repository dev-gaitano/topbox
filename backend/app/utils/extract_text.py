import io
from pathlib import Path

import pymupdf


def extract_text(pdf_path: Path | str) -> str:
    path = Path(pdf_path)

    if not pdf_path:
        raise ValueError("pdf_path cannot be empty")

    if not path.exists():
        raise FileNotFoundError(f"file '{pdf_path}' does not exist")

    if path.suffix.lower() != ".pdf":
        raise ValueError("file must be a PDF")

    doc = pymupdf.open(path)
    out = io.BytesIO()

    for page in doc:
        text = page.get_text().encode("utf8")
        out.write(text)
        out.write(bytes((12,)))

    print(out.getvalue().decode("utf8"))
    return out.getvalue().decode("utf8")
