"""AI extraction service with adversarial review."""
from typing import Dict, Optional
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.core.config import get_settings
from app.core.prompts import EXTRACTION_PROMPT, CRITIQUE_AND_FINALIZE_PROMPT
from app.models.schemas import NormExtraction

settings = get_settings()


class AdversarialReviewChain:
    """2-agent chain for extracting norms with adversarial review."""

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.0):
        """Initialize the chain with LLM."""
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=settings.openai_api_key
        )

        # Create structured output LLM
        self.structured_llm = self.llm.with_structured_output(NormExtraction)

        # Create prompts
        self.extraction_prompt = ChatPromptTemplate.from_template(EXTRACTION_PROMPT)
        self.critique_prompt = ChatPromptTemplate.from_template(CRITIQUE_AND_FINALIZE_PROMPT)

    def extract_initial(self, article_text: str, article_id: str, title: str) -> Dict:
        """
        Step 1: Generate initial extraction.

        Args:
            article_text: Full text of the article
            article_id: Article number
            title: Article title

        Returns:
            Initial extraction dict
        """
        # Create chain with structured output
        chain = self.extraction_prompt | self.structured_llm

        # Invoke with article context
        result = chain.invoke({
            "article_text": article_text,
            "article_id": article_id,
            "title": title or "Без назви"
        })

        return result.dict()

    def critique_and_finalize(
        self,
        article_text: str,
        initial_extraction: Dict
    ) -> NormExtraction:
        """
        Step 2: Critique initial extraction and produce final version.

        Args:
            article_text: Original article text
            initial_extraction: Initial extraction from step 1

        Returns:
            Final NormExtraction with corrections
        """
        # Create chain with structured output
        chain = self.critique_prompt | self.structured_llm

        # Invoke with article and initial extraction
        result = chain.invoke({
            "article_text": article_text,
            "initial_extraction": str(initial_extraction)
        })

        return result

    def process_article(
        self,
        article_text: str,
        article_id: str,
        title: Optional[str] = None
    ) -> Dict:
        """
        Process article through full 2-agent adversarial review.

        Args:
            article_text: Full text of the article
            article_id: Article number
            title: Article title (optional)

        Returns:
            Final extraction with metadata
        """
        # Step 1: Initial extraction
        initial = self.extract_initial(article_text, article_id, title)

        # Step 2: Critique and finalize
        final = self.critique_and_finalize(article_text, initial)

        # Add extraction metadata
        extraction_data = final.dict()
        extraction_data["extraction_metadata"] = {
            "model": "gpt-4o",
            "timestamp": datetime.utcnow().isoformat(),
            "review_chain": "2-agent",
            "initial_extraction": initial
        }

        return extraction_data


def extract_norm_from_article(
    article_text: str,
    article_id: str,
    title: Optional[str] = None
) -> Dict:
    """
    Convenience function to extract norm from article.

    Args:
        article_text: Full text of the article
        article_id: Article number
        title: Article title (optional)

    Returns:
        Extracted norm data
    """
    chain = AdversarialReviewChain()
    return chain.process_article(article_text, article_id, title)
