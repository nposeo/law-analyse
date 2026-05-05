"""Test suite for PDF parser."""
import pytest
from pathlib import Path
from app.services.pdf_parser import UkrainianLawParser, parse_law_pdf


def test_article_pattern_detection():
    """Test article boundary detection."""
    sample_text = """
    Стаття 1. Загальні положення

    Цей закон регулює відносини у сфері освіти.

    Стаття 2. Визначення термінів

    У цьому Законі терміни вживаються у такому значенні.
    """

    parser = UkrainianLawParser("")
    parser.full_text = sample_text
    boundaries = parser.detect_article_boundaries(sample_text)

    assert len(boundaries) == 2
    assert boundaries[0][2] == "1"  # Article number
    assert boundaries[1][2] == "2"


def test_hierarchy_parsing():
    """Test parsing of article hierarchy."""
    article_text = """
    Стаття 5. Структура

    1. Перша частина
    2. Друга частина

    1) Перший пункт
    2) Другий пункт

    а) Підпункт а
    б) Підпункт б
    """

    parser = UkrainianLawParser("")
    structure = parser.parse_hierarchy(article_text)

    assert len(structure["parts"]) == 2
    assert len(structure["points"]) == 2
    assert len(structure["subpoints"]) == 2


def test_empty_pdf():
    """Test handling of empty or invalid input."""
    parser = UkrainianLawParser("")
    parser.full_text = ""

    articles = parser.extract_articles()
    assert len(articles) == 0


def test_article_count():
    """Test article counting."""
    sample_text = """
    Стаття 1. Перша
    Стаття 2. Друга
    Стаття 3. Третя
    """

    parser = UkrainianLawParser("")
    parser.full_text = sample_text
    count = parser.get_article_count()

    assert count == 3


@pytest.mark.skip(reason="Requires actual PDF file")
def test_real_pdf_parsing():
    """Test parsing real Ukrainian law PDF."""
    # This test requires downloading actual law PDF
    pdf_path = Path("tests/fixtures/test_law.pdf")

    if not pdf_path.exists():
        pytest.skip("Test PDF not found")

    articles = parse_law_pdf(str(pdf_path))

    assert len(articles) > 0
    assert articles[0].article_number is not None
    assert articles[0].full_text != ""
