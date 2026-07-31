"""
Regression Test Suite for Abbreviation-Aware Context Compressor.
Verifies that sentence boundary detection never splits on common honorifics and abbreviations:
- Mr., Dr., Mrs., Prof., Inc., U.S., U.K., etc.
"""

import unittest
from app.rag.context_compressor import ContextCompressor, context_compressor
from app.schemas.knowledge import KnowledgeCitation


class TestContextCompressorAbbreviations(unittest.TestCase):
    def setUp(self):
        self.compressor = context_compressor

    def test_sentence_splitter_abbreviations(self):
        cases = [
            ("The CEO of Sohel Tech is Mr. Iron Man.", "The CEO of Sohel Tech is Mr. Iron Man."),
            ("The CEO is Dr. Stephen Strange.", "The CEO is Dr. Stephen Strange."),
            ("Mrs. Jane Doe manages HR.", "Mrs. Jane Doe manages HR."),
            ("Prof. Alan Turing founded the field. He was born in London.", "Prof. Alan Turing founded the field."),
            ("Acme Inc. is headquartered in New York.", "Acme Inc. is headquartered in New York."),
            ("The U.S. office opens at 9 AM.", "The U.S. office opens at 9 AM."),
            ("The U.K. office opens at 8 AM.", "The U.K. office opens at 8 AM."),
        ]

        for full_text, expected_sentence in cases:
            sentences = self.compressor._split_sentences(full_text)
            self.assertGreaterEqual(len(sentences), 1)
            self.assertEqual(sentences[0], expected_sentence)

    def test_compress_citations_preserves_full_entity(self):
        citation = KnowledgeCitation(
            document_name="Company_Profile.txt",
            chunk_index=0,
            similarity_score=0.95,
            snippet="The CEO of Sohel Tech is Mr. Iron Man. The cafeteria closes at 4 PM."
        )

        compressed = self.compressor.compress_citations(
            citations=[citation],
            query_keywords=["ceo", "sohel", "tech"]
        )

        self.assertIn("Mr. Iron Man", compressed)
        self.assertNotIn("The cafeteria closes at 4 PM", compressed)


if __name__ == "__main__":
    unittest.main()
