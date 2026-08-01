"""
Retry Handler Module.

Implements exponential backoff execution logic for transient errors (429 Rate Limits, 500/503 Server Errors,
network timeouts, connection drops) when communicating with external LLM APIs.
Excludes non-retryable client errors (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found).
"""

import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar

from app.ai.providers.base_provider import ProviderUnavailableException
from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")

NON_RETRYABLE_STATUS_CODES = {400, 401, 403, 404}
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class RetryHandler:
    """Executes callables with exponential backoff retries on transient errors."""

    def __init__(
        self,
        max_retries: int = settings.AI_MAX_RETRIES,
        initial_delay: float = 1.0,
        backoff_factor: float = settings.AI_BACKOFF_FACTOR
    ) -> None:
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor

    def execute(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """
        Executes function with exponential backoff retries.
        Passes through ProviderUnavailableException when provider models are exhausted.
        """
        delay = self.initial_delay
        last_exception = None

        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except ProviderUnavailableException:
                raise
            except Exception as exc:
                last_exception = exc
                status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)

                if status_code in NON_RETRYABLE_STATUS_CODES:
                    logger.error(
                        f"Non-retryable client error (HTTP {status_code}) encountered on attempt {attempt}/{self.max_retries}: {exc}"
                    )
                    raise

                is_retryable = (
                    status_code in RETRYABLE_STATUS_CODES
                    or status_code is None
                    or isinstance(exc, (TimeoutError, ConnectionError, ValueError))
                )

                if not is_retryable or attempt == self.max_retries:
                    logger.error(
                        f"Max retry attempts ({attempt}/{self.max_retries}) reached or non-retryable error: {exc}"
                    )
                    raise

                logger.warning(
                    f"Transient failure (HTTP {status_code or 'Network/Timeout'}) on attempt {attempt}/{self.max_retries}: {exc}. Retrying in {delay:.2f}s..."
                )
                time.sleep(delay)
                delay *= self.backoff_factor

        if last_exception:
            raise last_exception
        raise RuntimeError("Retry handler exhausted retries without exception context.")


retry_handler = RetryHandler()
