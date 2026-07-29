"""
Centralized Structured Logging Module.

Provides JSON-formatted structured logging for requests, responses, database transactions,
errors, and AI tool execution latency.
"""

import logging
import sys
from typing import Any


class StructuredLogger:
    """Configures and handles structured JSON logging."""

    def __init__(self, name: str = "ai_lms") -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_request(self, method: str, path: str, client_ip: str) -> None:
        self.logger.info(f"HTTP_REQUEST method={method} path={path} client={client_ip}")

    def log_response(self, method: str, path: str, status_code: int, latency_ms: float) -> None:
        self.logger.info(
            f"HTTP_RESPONSE method={method} path={path} status={status_code} latency={latency_ms:.2f}ms"
        )

    def log_ai_execution(self, agent_name: str, tool_name: str, latency_ms: float, status: str) -> None:
        self.logger.info(
            f"AI_EXECUTION agent='{agent_name}' tool='{tool_name}' status={status} latency={latency_ms:.2f}ms"
        )

    def log_error(self, error_msg: str, context: dict[str, Any] | None = None) -> None:
        self.logger.error(f"ERROR_LOG msg='{error_msg}' context={context or {}}")


structured_logger = StructuredLogger()
