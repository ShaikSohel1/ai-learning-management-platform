"""
Conversation Memory Module.

Manages multi-turn conversation memory per user session in memory.
Supports adding messages, retrieving contextual window, and resetting history (DELETE /ai/history).
"""

from typing import Dict, List, Any
import threading
from datetime import datetime


class ConversationMessage:
    def __init__(self, role: str, content: str):
        self.role = role  # 'user' or 'assistant'
        self.content = content
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }


class ConversationMemoryStore:
    """Thread-safe multi-user conversation history memory store."""

    def __init__(self, max_history_per_user: int = 20) -> None:
        self._store: Dict[int, List[ConversationMessage]] = {}
        self.max_history_per_user = max_history_per_user
        self._lock = threading.Lock()

    def add_user_message(self, user_id: int, content: str) -> None:
        self._append_message(user_id, ConversationMessage(role="user", content=content))

    def add_ai_message(self, user_id: int, content: str) -> None:
        self._append_message(user_id, ConversationMessage(role="assistant", content=content))

    def _append_message(self, user_id: int, msg: ConversationMessage) -> None:
        with self._lock:
            if user_id not in self._store:
                self._store[user_id] = []
            self._store[user_id].append(msg)
            # Enforce max context window limit
            if len(self._store[user_id]) > self.max_history_per_user:
                self._store[user_id] = self._store[user_id][-self.max_history_per_user :]

    def get_history(self, user_id: int) -> List[Dict[str, Any]]:
        with self._lock:
            messages = self._store.get(user_id, [])
            return [m.to_dict() for m in messages]

    def format_history_for_prompt(self, user_id: int) -> str:
        """Formats historical messages into text block for prompt builder context."""
        with self._lock:
            messages = self._store.get(user_id, [])
            if not messages:
                return "No previous conversation context."

            formatted = []
            for msg in messages:
                prefix = "User:" if msg.role == "user" else "Assistant:"
                formatted.append(f"{prefix} {msg.content}")
            return "\n".join(formatted)

    def clear_history(self, user_id: int) -> bool:
        """Clears conversation history for the given user."""
        with self._lock:
            if user_id in self._store:
                del self._store[user_id]
                return True
            return False


memory_store = ConversationMemoryStore()
