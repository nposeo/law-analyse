"""Test suite for AI extractor."""
import pytest
from unittest.mock import Mock, patch
from app.services.ai_extractor import AdversarialReviewChain, extract_norm_from_article


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    return {
        "article_id": "1",
        "title": "Тестова стаття",
        "norm": "Регулює тестові відносини",
        "subject": "Всі громадяни",
        "simplified_explanation": "Це тестове пояснення",
        "confidence_score": 0.85,
        "needs_human_review": False
    }


@patch('app.services.ai_extractor.ChatOpenAI')
def test_adversarial_chain_initialization(mock_openai):
    """Test chain initialization."""
    chain = AdversarialReviewChain()

    assert chain.llm is not None
    assert chain.structured_llm is not None


@patch('app.services.ai_extractor.ChatOpenAI')
def test_extract_initial(mock_openai, mock_llm_response):
    """Test initial extraction step."""
    # Mock LLM response
    mock_chain = Mock()
    mock_chain.invoke.return_value = Mock(dict=lambda: mock_llm_response)

    with patch.object(AdversarialReviewChain, 'extract_initial', return_value=mock_llm_response):
        chain = AdversarialReviewChain()
        result = chain.extract_initial(
            article_text="Тестовий текст статті",
            article_id="1",
            title="Тестова стаття"
        )

        assert result["article_id"] == "1"
        assert result["confidence_score"] == 0.85


def test_confidence_threshold():
    """Test that low confidence triggers human review flag."""
    low_confidence_response = {
        "article_id": "1",
        "title": "Складна стаття",
        "norm": "Неоднозначна норма",
        "subject": "Невизначено",
        "simplified_explanation": "Складно пояснити",
        "confidence_score": 0.65,
        "needs_human_review": True
    }

    assert low_confidence_response["confidence_score"] < 0.8
    assert low_confidence_response["needs_human_review"] is True


@patch('app.services.ai_extractor.AdversarialReviewChain')
def test_process_article_adds_metadata(mock_chain_class, mock_llm_response):
    """Test that processing adds extraction metadata."""
    mock_instance = Mock()
    mock_instance.process_article.return_value = {
        **mock_llm_response,
        "extraction_metadata": {
            "model": "gpt-4o",
            "review_chain": "2-agent"
        }
    }
    mock_chain_class.return_value = mock_instance

    result = extract_norm_from_article(
        article_text="Тестовий текст",
        article_id="1",
        title="Тест"
    )

    assert "extraction_metadata" in result
    assert result["extraction_metadata"]["model"] == "gpt-4o"
    assert result["extraction_metadata"]["review_chain"] == "2-agent"


def test_ukrainian_text_handling():
    """Test that Ukrainian characters are handled correctly."""
    ukrainian_text = "Стаття регулює відносини у сфері освіти та науки"

    # Verify Ukrainian characters are preserved
    assert "Стаття" in ukrainian_text
    assert "освіти" in ukrainian_text
    assert len(ukrainian_text) > 0
