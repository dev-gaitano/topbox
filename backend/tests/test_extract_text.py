from pathlib import Path

import pytest

from app.utils import extract_text

FIXTURE_PDF = Path(__file__).parent / "fixtures" / "sample_brand.pdf"
KNOWN_TEXT = "Industry"


def test_extract_text_returns_non_empty_string():
    result = extract_text(FIXTURE_PDF)

    assert isinstance(result, str)
    assert KNOWN_TEXT in result


def test_extract_text_raises_on_wrong_path(tmp_path):
    path = tmp_path / "someFile.pdf"
    with pytest.raises(FileNotFoundError, match=f"file '{path}' does not exist"):
        extract_text(path)


def test_extract_text_raises_on_empty_string():
    with pytest.raises(ValueError, match="pdf_path cannot be empty"):
        extract_text("")


@pytest.mark.parametrize(
    "bad_input",
    [
        123,
        None,
        ["sample.pdf"],
        {"path": "sample.pdf"},
    ],
)
def test_extract_text_raises_on_invalid_type(bad_input):
    with pytest.raises(TypeError):
        extract_text(bad_input)


def test_extract_text_raises_on_non_pdf(tmp_path):
    fake_txt = tmp_path / "document.txt"
    fake_txt.write_text("I am not a PDF")

    with pytest.raises(ValueError, match="file must be a PDF"):
        extract_text(str(fake_txt))
