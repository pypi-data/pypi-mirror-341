"""Constants for the ut-scrape package."""

from __future__ import annotations

from typing import Final

from fastapi.security import APIKeyHeader

# ----- Security -----

ACCESS_TOKEN: Final = "koneko"  # noqa: S105  # just playing
API_KEY: Final = "koneko"
API_KEY_NAME: Final = "X-API-Key"

api_key_header: Final = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
