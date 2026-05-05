"""PDF parser for Ukrainian legal documents."""
import re
from typing import List, Dict, Tuple, Optional
import pdfplumber
from dataclasses import dataclass


@dataclass
class ParsedArticle:
    """Parsed article data."""
    article_number: str
    title: Optional[str]
    full_text: str
    hierarchy_path: List[str]


class UkrainianLawParser:
    """Parser for Ukrainian law PDFs."""

    # Regex patterns for Ukrainian legal documents
    ARTICLE_PATTERN = r'Стаття\s+(\d+)\.?\s*(.*?)(?=\n|$)'
    PART_PATTERN = r'(?:^|\n)(\d+)\.?\s+'
    POINT_PATTERN = r'(?:^|\n)(\d+)\)\s+'
    SUBPOINT_PATTERN = r'(?:^|\n)([а-я])\)\s+'

    def __init__(self, pdf_path: str):
        """Initialize parser with PDF path."""
        self.pdf_path = pdf_path
        self.full_text = ""

    def extract_text(self) -> str:
        """Extract all text from PDF."""
        text_parts = []

        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

        self.full_text = "\n".join(text_parts)
        return self.full_text

    def detect_article_boundaries(self, text: str) -> List[Tuple[int, int, str, str]]:
        """
        Detect article boundaries in text.

        Returns:
            List of (start_pos, end_pos, article_number, title) tuples
        """
        boundaries = []

        # Find all article matches
        for match in re.finditer(self.ARTICLE_PATTERN, text, re.MULTILINE):
            start_pos = match.start()
            article_number = match.group(1)
            title = match.group(2).strip() if match.group(2) else ""
            boundaries.append((start_pos, article_number, title))

        # Calculate end positions
        result = []
        for i, (start, number, title) in enumerate(boundaries):
            if i < len(boundaries) - 1:
                end = boundaries[i + 1][0]
            else:
                end = len(text)
            result.append((start, end, number, title))

        return result

    def parse_hierarchy(self, article_text: str) -> Dict[str, any]:
        """
        Parse hierarchical structure within an article.

        Returns:
            Dict with parts, points, and subpoints
        """
        structure = {
            "parts": [],
            "points": [],
            "subpoints": []
        }

        # Find parts (Частина)
        for match in re.finditer(self.PART_PATTERN, article_text, re.MULTILINE):
            structure["parts"].append({
                "number": match.group(1),
                "position": match.start()
            })

        # Find points (Пункт)
        for match in re.finditer(self.POINT_PATTERN, article_text, re.MULTILINE):
            structure["points"].append({
                "number": match.group(1),
                "position": match.start()
            })

        # Find subpoints (Підпункт)
        for match in re.finditer(self.SUBPOINT_PATTERN, article_text, re.MULTILINE):
            structure["subpoints"].append({
                "letter": match.group(1),
                "position": match.start()
            })

        return structure

    def build_hierarchy_path(self, article_number: str, structure: Dict) -> List[str]:
        """
        Build hierarchy path for article.

        Example: ['1'] or ['1', '1.1', '1.1.a']
        """
        path = [article_number]

        # For MVP, we'll keep it simple - just article number
        # Can be extended later to include parts/points
        if structure["parts"]:
            path.append(f"{article_number}.{len(structure['parts'])}")

        return path

    def extract_articles(self) -> List[ParsedArticle]:
        """
        Extract all articles from PDF.

        Returns:
            List of ParsedArticle objects
        """
        if not self.full_text:
            self.extract_text()

        boundaries = self.detect_article_boundaries(self.full_text)
        articles = []

        for start, end, number, title in boundaries:
            article_text = self.full_text[start:end].strip()
            structure = self.parse_hierarchy(article_text)
            hierarchy_path = self.build_hierarchy_path(number, structure)

            articles.append(ParsedArticle(
                article_number=number,
                title=title if title else None,
                full_text=article_text,
                hierarchy_path=hierarchy_path
            ))

        return articles

    def get_article_count(self) -> int:
        """Get total number of articles in document."""
        if not self.full_text:
            self.extract_text()

        matches = re.findall(self.ARTICLE_PATTERN, self.full_text, re.MULTILINE)
        return len(matches)


def parse_law_pdf(pdf_path: str) -> List[ParsedArticle]:
    """
    Convenience function to parse a law PDF.

    Args:
        pdf_path: Path to PDF file

    Returns:
        List of parsed articles
    """
    parser = UkrainianLawParser(pdf_path)
    return parser.extract_articles()
