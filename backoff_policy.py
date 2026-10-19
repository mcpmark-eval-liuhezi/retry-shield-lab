"""Jittered exponential backoff policy module for retry-shield-lab.

Computes retry delays using full-jitter exponential backoff, so that retries
against flaky services do not stampede them.

This is prototype-quality demo code.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterator, Optional


MAX_BACKOFF_CAP_DEFAULT: float = 30.0
DEFAULT_MULTIPLIER: float = 2.0
DEFAULT_BASE_DELAY: float = 0.1
DEFAULT_MAX_ATTEMPTS: int = 8


@dataclass
class BackoffPolicy:
    """Configuration for a jittered exponential backoff policy.

    Attributes:
        base_delay: Delay in seconds for the first retry.
        multiplier: Growth factor applied per attempt.
        max_backoff_cap: Upper bound on any single computed delay.
        max_attempts: Maximum number of attempts the policy yields delays for.
        seed: Optional seed for deterministic jitter (useful in tests).
    """

    base_delay: float = DEFAULT_BASE_DELAY
    multiplier: float = DEFAULT_MULTIPLIER
    max_backoff_cap: float = MAX_BACKOFF_CAP_DEFAULT
    max_attempts: int = DEFAULT_MAX_ATTEMPTS
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        if self.base_delay <= 0:
            raise ValueError("base_delay must be positive")
        if self.multiplier <= 1:
            raise ValueError("multiplier must be greater than 1")
        if self.max_backoff_cap <= 0:
            raise ValueError("max_backoff_cap must be positive")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        # Full-jitter is stateless, so a module-level Random is fine here;
        # seed support is kept for deterministic tests and demos.
        self._rng = random.Random(self.seed)

    def delay_for(self, attempt: int) -> float:
        """Return the jittered delay in seconds before the given attempt.

        ``attempt`` is zero-indexed: 0 is the first retry.

        Raises:
            ValueError: If ``attempt`` is negative.
        """
        if attempt < 0:
            raise ValueError("attempt must be non-negative")

        # Exponential schedule capped at max_backoff_cap.
        candidate = self.base_delay * (self.multiplier ** attempt)
        capped = min(candidate, self.max_backoff_cap)

        # Full jitter: uniform in [0, capped] (AWS-style).
        return self._rng.uniform(0.0, capped)

    def delays(self) -> Iterator[float]:
        """Yield jittered delays for each retry attempt up to max_attempts."""
        for attempt in range(self.max_attempts):
            yield self.delay_for(attempt)
