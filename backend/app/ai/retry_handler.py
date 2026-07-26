"""
Retry Handler Module.

Implements exponential backoff execution logic for transient errors (429 Rate Limits, 500 Server Errors,
network timeouts, connection drops) when communicating with external LLM APIs.
"""

import logging
import time
from typing import Callable, TypeVar, Any
import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RetryHandler:
    """Executes callables with exponential backoff retries on transient errors."""

    def __init__(
        self,
        max_retries: int = settings.GEMINI_MAX_RETRIES,
        initial_delay: float = 1.0,
        backoff_factor: float = settings.GEMINI_BACKOFF_FACTOR
    ) -> None:
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor

    def execute(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """
        Executes function with exponential backoff retries.

        Handles HTTP 429, 500, 502, 503, 504 status codes and network exceptions.
        """
        delay = self.initial_delay
        last_exception = None

        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except (httpx.HTTPStatusError, httpx.RequestError, TimeoutError, ValueError) as exc:
                last_exception = exc
                
                # Check status code if available
                status_code = getattr(getattr(exc, "response", None), "status_code", None)
                
                is_transient = True
                if status_code and status_code not in (429, 500, 502, 503, 504):
                    # Client errors like 400 Bad Request or 401 Unauthorized are non-retryable
                    is_transient = False

                if not is_transient or attempt == self.max_retries:
                    logger.error(
                        f"Non-retryable or max attempts ({attempt}/{self.max_retries}) reached for error: {exc}"
                    )
                    raise exc

                logger.warning(
                    f"Retryable attempt {attempt}/{self.max_retries} failed with error: {exc}. Retrying in {delay:.2f}s..."
                )
                time.sleep(delay)
                delay *= self.backoff_factor

        if last_exception:
            raise last_exception
        raise RuntimeError("Retry handler exhausted retries without exception context.")


retry_handler = RetryHandler()
