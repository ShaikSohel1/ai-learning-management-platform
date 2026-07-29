"""
Search History & Analytics Logger Module.

Maintains thread-safe user search history logs, execution latency metrics,
confidence scores, and aggregate knowledge base analytics.
"""

import threading
from datetime import UTC, datetime
from typing import Any


class SearchHistoryEntry:
    def __init__(
        self,
        entry_id: str,
        user_id: int,
        question: str,
        timestamp: str,
        response_time_ms: float,
        documents_used: list[str],
        confidence_score: float,
        rag_used: bool
    ):
        self.entry_id = entry_id
        self.user_id = user_id
        self.question = question
        self.timestamp = timestamp
        self.response_time_ms = response_time_ms
        self.documents_used = documents_used
        self.confidence_score = confidence_score
        self.rag_used = rag_used

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "user_id": self.user_id,
            "question": self.question,
            "timestamp": self.timestamp,
            "response_time_ms": round(self.response_time_ms, 2),
            "documents_used": self.documents_used,
            "confidence_score": round(self.confidence_score, 2),
            "rag_used": self.rag_used,
        }


class SearchHistoryStore:
    """Thread-safe search history logger and analytics tracker."""

    def __init__(self, max_history_per_user: int = 50) -> None:
        self._store: dict[int, list[SearchHistoryEntry]] = {}
        self.max_history_per_user = max_history_per_user
        self._lock = threading.Lock()

    def add_entry(
        self,
        user_id: int,
        question: str,
        response_time_ms: float,
        documents_used: list[str],
        confidence_score: float,
        rag_used: bool
    ) -> SearchHistoryEntry:
        import uuid
        entry = SearchHistoryEntry(
            entry_id=str(uuid.uuid4()),
            user_id=user_id,
            question=question,
            timestamp=datetime.now(UTC).isoformat(),
            response_time_ms=response_time_ms,
            documents_used=documents_used,
            confidence_score=confidence_score,
            rag_used=rag_used
        )

        with self._lock:
            if user_id not in self._store:
                self._store[user_id] = []
            self._store[user_id].insert(0, entry)  # Prepend newest
            if len(self._store[user_id]) > self.max_history_per_user:
                self._store[user_id] = self._store[user_id][: self.max_history_per_user]

        return entry

    def get_user_history(self, user_id: int) -> list[dict[str, Any]]:
        with self._lock:
            entries = self._store.get(user_id, [])
            return [e.to_dict() for e in entries]

    def clear_user_history(self, user_id: int) -> bool:
        with self._lock:
            if user_id in self._store:
                del self._store[user_id]
                return True
            return False

    def get_analytics_metrics(self) -> dict[str, Any]:
        """Calculates global search analytics metrics."""
        all_entries: list[SearchHistoryEntry] = []
        with self._lock:
            for user_entries in self._store.values():
                all_entries.extend(user_entries)

        if not all_entries:
            return {
                "total_searches": 0,
                "avg_response_time_ms": 0.0,
                "avg_confidence_score": 0.0,
                "rag_utilization_rate": 0.0,
                "recent_searches_count": 0,
            }

        total = len(all_entries)
        avg_time = sum(e.response_time_ms for e in all_entries) / total
        avg_conf = sum(e.confidence_score for e in all_entries) / total
        rag_count = sum(1 for e in all_entries if e.rag_used)

        return {
            "total_searches": total,
            "avg_response_time_ms": round(avg_time, 1),
            "avg_confidence_score": round(avg_conf, 1),
            "rag_utilization_rate": round((rag_count / total) * 100, 1),
            "recent_searches_count": total,
        }


search_history_store = SearchHistoryStore()
