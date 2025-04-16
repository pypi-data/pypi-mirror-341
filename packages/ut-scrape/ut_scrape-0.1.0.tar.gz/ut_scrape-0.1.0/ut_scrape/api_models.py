"""API response models for Untappd Scraper."""

from datetime import date, datetime  # noqa: F401  # used by Pydantic rebuild
from typing import TypedDict

import pydantic
from pydantic.dataclasses import dataclass as pydantic_dataclass
from untappd_scraper.structs.web import (
    WebActivityBeer,
    WebUserHistoryBeer,
    WebUserHistoryVenue,
    WebVenueMenuBeer,
)


class BeerDetailsResponse(TypedDict):
    """Beer details response."""

    beer_id: int
    name: str
    brewery: str
    style: str
    global_rating: float


PydanticWebUserHistoryBeer = pydantic_dataclass(WebUserHistoryBeer, frozen=True)
pydantic.dataclasses.rebuild_dataclass(PydanticWebUserHistoryBeer)

PydanticWebUserHistoryVenue = pydantic_dataclass(WebUserHistoryVenue, frozen=True)
pydantic.dataclasses.rebuild_dataclass(PydanticWebUserHistoryVenue)


PydanticWebVenueMenuBeer = pydantic_dataclass(WebVenueMenuBeer, frozen=True)
pydantic.dataclasses.rebuild_dataclass(PydanticWebVenueMenuBeer)

PydanticWebActivityBeer = pydantic_dataclass(WebActivityBeer, frozen=True)
pydantic.dataclasses.rebuild_dataclass(PydanticWebActivityBeer)


class VenueFromNameResponse(TypedDict):
    """Venue search response."""

    venue_id: int | None
    venue_name: str | None
    venue_address: str | None
    search_string: str
