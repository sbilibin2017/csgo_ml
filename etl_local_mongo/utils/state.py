from typing import Any

import dateutil.parser
import redis


class State:
    """Class for fixing and receiving etl status."""

    def __init__(self, redisclient: redis.Redis) -> None:
        self.redisclient = redisclient

    def add(self, key: str, value: Any) -> None:
        """Update status."""
        self.redisclient.sadd(key, value)

    def get(self, key: str) -> Any:
        """Get status."""
        try:
            return self.redisclient.smembers(key)
        except Exception:
            return None
