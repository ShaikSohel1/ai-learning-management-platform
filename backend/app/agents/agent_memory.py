"""
Shared Agent Memory Module.

Stores user goals, completed tasks, previous agent recommendations, and conversation turn history.
Prevents repeating duplicate questions or redundant agent calls across sessions.
"""

from datetime import datetime, UTC
import threading
from typing import Dict, List, Any, Optional


class SharedAgentMemory:
    """Thread-safe memory store managing multi-agent decision history."""

    def __init__(self) -> None:
        self._memory: Dict[int, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def record_decision(
        self,
        user_id: int,
        agent_name: str,
        decision_summary: str,
        output_data: Dict[str, Any]
    ) -> None:
        with self._lock:
            if user_id not in self._memory:
                self._memory[user_id] = {
                    "completed_tasks": [],
                    "decisions": [],
                    "last_updated": datetime.now(UTC).isoformat()
                }

            self._memory[user_id]["decisions"].append({
                "agent_name": agent_name,
                "summary": decision_summary,
                "data": output_data,
                "timestamp": datetime.now(UTC).isoformat()
            })
            self._memory[user_id]["last_updated"] = datetime.now(UTC).isoformat()

    def get_memory_summary(self, user_id: int) -> Dict[str, Any]:
        with self._lock:
            return self._memory.get(user_id, {
                "completed_tasks": [],
                "decisions": [],
                "last_updated": ""
            })

    def clear_memory(self, user_id: int) -> None:
        with self._lock:
            if user_id in self._memory:
                del self._memory[user_id]


agent_memory_store = SharedAgentMemory()
