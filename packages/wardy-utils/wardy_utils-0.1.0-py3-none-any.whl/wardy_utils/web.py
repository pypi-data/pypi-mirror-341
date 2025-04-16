"""General internet helpers."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

import hishel

logging.getLogger("hishel.controller").setLevel(logging.DEBUG)


class CachedClient(hishel.CacheClient):
    """Handle httpx client and hishel caching."""

    def __init__(
        self, *, force_cache: bool = False, cache_minutes: int = 30, timeout_seconds: int = 20
    ) -> None:
        """Initialize the client.

        Args:
            force_cache (bool): Force cache to be used on all pages.
            cache_minutes (int): Number of minutes to cache.
            timeout_seconds (int): Number of seconds to timeout.
        """
        cache: Final = timedelta(minutes=cache_minutes).total_seconds()
        timeout: Final = timedelta(seconds=timeout_seconds).total_seconds()

        self.storage = hishel.FileStorage(ttl=cache)
        self.controller = hishel.Controller(force_cache=force_cache)

        super().__init__(
            follow_redirects=True,
            storage=self.storage,
            controller=self.controller,
            timeout=timeout,
        )
