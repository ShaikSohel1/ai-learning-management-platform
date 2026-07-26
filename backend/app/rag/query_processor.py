"""
Query Processor & Intent Understanding Module.

Normalizes user search queries, expands domain abbreviations, detects query intent,
extracts key phrases, and formulates optimized search queries for hybrid retrieval.
"""

import re
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

# Common enterprise abbreviation mapping
ABBREVIATION_MAP: Dict[str, str] = {
    "lms": "learning management system",
    "hr": "human resources",
    "sop": "standard operating procedure",
    "qa": "quality assurance",
    "api": "application programming interface",
    "db": "database",
    "auth": "authentication",
    "jwt": "json web token",
    "pto": "paid time off",
    "devops": "development operations cloud",
    "ci/cd": "continuous integration continuous deployment",
    "pr": "pull request code review",
    "sla": "service level agreement",
}

# Stop words to remove when extracting keywords
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "to", "from", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "any", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "s", "t",
    "can", "will", "just", "don", "should", "now", "what", "our", "my",
    "us", "tell", "me", "about", "give", "please"
}


class ProcessedQuery:
    def __init__(
        self,
        original_query: str,
        normalized_query: str,
        optimized_query: str,
        intent: str,
        keywords: List[str],
        expanded_terms: List[str]
    ):
        self.original_query = original_query
        self.normalized_query = normalized_query
        self.optimized_query = optimized_query
        self.intent = intent
        self.keywords = keywords
        self.expanded_terms = expanded_terms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "optimized_query": self.optimized_query,
            "intent": self.intent,
            "keywords": self.keywords,
            "expanded_terms": self.expanded_terms,
        }


class QueryProcessor:
    """Processes, normalizes, and expands raw user questions for semantic and keyword retrieval."""

    def process(self, query: str) -> ProcessedQuery:
        if not query:
            return ProcessedQuery("", "", "", "general", [], [])

        raw = query.strip()
        # Lowercase & clean punctuation
        cleaned = re.sub(r"[^\w\s/]", " ", raw.lower())
        tokens = cleaned.split()

        # Detect intent
        intent = self._detect_intent(raw.lower(), tokens)

        # Expand abbreviations & collect expanded terms
        expanded_terms: List[str] = []
        expanded_tokens: List[str] = []

        for token in tokens:
            if token in ABBREVIATION_MAP:
                expanded_val = ABBREVIATION_MAP[token]
                expanded_terms.append(f"{token}->{expanded_val}")
                expanded_tokens.append(expanded_val)
            else:
                expanded_tokens.append(token)

        # Extract keywords (filtering stop words)
        keywords = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]

        # Construct optimized query string for vector & keyword search
        optimized_parts = keywords + [t for t in expanded_tokens if t not in keywords]
        optimized_query = " ".join(dict.fromkeys(optimized_parts))

        normalized_query = " ".join(tokens)

        return ProcessedQuery(
            original_query=raw,
            normalized_query=normalized_query,
            optimized_query=optimized_query or raw,
            intent=intent,
            keywords=keywords,
            expanded_terms=expanded_terms,
        )

    def _detect_intent(self, text: str, tokens: List[str]) -> str:
        """Categorizes query intent into: policy, technical, procedure, or general."""
        if any(w in text for w in ["policy", "rule", "leave", "holiday", "benefit", "pto", "allowance", "salary", "reimbursement"]):
            return "policy"
        elif any(w in text for w in ["how to", "step", "guide", "workflow", "process", "sop", "procedure", "setup"]):
            return "procedure"
        elif any(w in text for w in ["code", "api", "database", "python", "sql", "config", "architecture", "docker", "bug", "error"]):
            return "technical"
        else:
            return "general"


query_processor = QueryProcessor()
