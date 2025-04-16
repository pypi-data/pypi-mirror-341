"""Expose Untappd Scraper via Reflex backend API."""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Any

import reflex as rx
from fastapi import (
    Depends,
    HTTPException,
    Query,  # Being checked at runtime
    Security,
)
from untappd_scraper.beer import Beer
from untappd_scraper.user import User
from untappd_scraper.user_beer_history import UserHistoryResponse  # noqa: TC002  # FastAPI
from untappd_scraper.venue import Venue
from ut_scrape.api_models import (
    BeerDetailsResponse,
    PydanticWebActivityBeer,
    PydanticWebUserHistoryVenue,
    PydanticWebVenueMenuBeer,
    VenueFromNameResponse,
)
from ut_scrape.constants import ACCESS_TOKEN, API_KEY, api_key_header

if TYPE_CHECKING:
    from collections.abc import Collection

    from reflex.event import EventSpec

app = rx.App()
assert app.api

# ----- Helpers -----


def to_list(obj: Collection) -> list[dict[str, Any]]:
    """Convert a collection to a dictionary."""
    return [asdict(o) for o in obj]


def verify_key(api_key: str = Security(api_key_header)) -> None:
    """Verify the API key."""
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")


def verify_access_token(access: str = Query(..., description="Simple access token")) -> None:
    """Verify the access token."""
    if access != ACCESS_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid access token")


app.api.router.dependencies.append(Depends(verify_access_token))

# ----- Endpoints -----


async def beer_details(beer_id: int) -> BeerDetailsResponse:
    """Get details for a beer."""
    beer = Beer(beer_id)

    return {
        "beer_id": beer.beer_id,
        "name": beer.name,
        "brewery": beer.brewery,
        "style": beer.style,
        "global_rating": beer.global_rating,
    }


async def user_activity(user_id: str) -> list[dict[str, Any]]:
    """Get activity for a user."""
    user = User(user_id)

    return to_list(user.activity())


async def user_beer_history(user_id: str) -> UserHistoryResponse:
    """Get beer history for a user."""
    user = User(user_id)

    return user.beer_history()


async def user_brewery_history(
    user_id: str,
    brewery_id: int,
    max_resorts: int = Query(
        0, ge=0, le=13, description="Number of re-sorts to try to get more beers"
    ),
) -> UserHistoryResponse:
    """Get beer history for a user from a particular brewery.

    Args:
        user_id (str): User ID
        brewery_id (int): Brewery ID
        max_resorts (int): Number of re-sorts to try to get more beers
    """
    user = User(user_id)

    return user.brewery_history(brewery_id=brewery_id, max_resorts=max_resorts)


async def user_recent_venues(user_id: str) -> list[dict[str, Any]]:
    """Get recent activity for a user."""
    user = User(user_id)

    return to_list(user.venue_history())


async def venue_activity(venue_id: int) -> list[dict[str, Any]]:
    """Get activity for a venue."""
    venue = Venue(venue_id)

    return to_list(venue.activity())


async def venue_from_name(venue_name: str = Query(...)) -> VenueFromNameResponse:
    """Get venue ID from name.

    Returns:
        dict[str,int|str]: venue ID if found, else 0
        int: venue ID if found, else 0
    """
    venue = Venue.from_name(venue_name)

    if venue:
        return {
            "venue_id": venue.venue_id,
            "venue_name": venue.name,
            "venue_address": venue.address,
            "search_string": venue_name,
        }
    return {
        "venue_id": None,
        "venue_name": None,
        "venue_address": None,
        "search_string": venue_name,
    }


async def venue_menus(venue_id: int) -> dict[str, list]:
    """Get menu(s) for a venue.

    Returns:
        dict[str, list]: menu name (or "checkin") and a list of beers in that menu
    """
    venue = Venue(venue_id)

    venue_menus: dict[str, list] = {}

    if menus := venue.menus():
        for menu in menus:
            venue_menus[f"{menu.selection} / {menu.name}"] = to_list(menu.beers)
    else:
        venue_menus["checkin"] = to_list(venue.activity())

    return venue_menus


app.api.add_api_route("/beer_details/{beer_id}", beer_details, tags=["beer"])

app.api.add_api_route(
    "/user_activity/{user_id}",
    user_activity,
    tags=["user"],
    response_model=list[PydanticWebActivityBeer],
)
app.api.add_api_route("/user_beer_history/{user_id}", user_beer_history, tags=["user"])
app.api.add_api_route(
    "/user_beer_history/{user_id}/{brewery_id}", user_brewery_history, tags=["user"]
)
app.api.add_api_route(
    "/user_recent_venues/{user_id}",
    user_recent_venues,
    tags=["user"],
    response_model=list[PydanticWebUserHistoryVenue],
)

app.api.add_api_route(
    "/venue_activity/{venue_id}",
    venue_activity,
    tags=["venue"],
    response_model=list[PydanticWebActivityBeer],
)
app.api.add_api_route("/venue_from_name", venue_from_name, tags=["venue"])
app.api.add_api_route(
    "/venue_menus/{venue_id}",
    venue_menus,
    tags=["venue"],
    response_model=dict[str, list[PydanticWebVenueMenuBeer | PydanticWebActivityBeer]],
)

# ----- State -----


class State(rx.State):
    """State for uniques query."""

    user_name: str = ""
    brewery_id: int
    max_resorts: int = 0

    results: list

    @rx.event
    def unique_submit(self, form_data: dict[str, Any]) -> EventSpec:
        """Handle form submission."""
        self.user_name = form_data["user_name"]
        self.brewery_id = int(form_data["brewery_id"])
        self.max_resorts = int(form_data["max_resorts"])

        return self.query()

    def query(self) -> EventSpec:
        """Run the query."""
        # url = URL(f"/user_recent_beers/{self.user_name}").copy_merge_params(
        #     {"brewery_id": self.brewery_id, "max_resorts": self.max_resorts}
        # )

        # resp = rx.fetch

        return rx.toast.error("I haven't implemented this yet!")


# ----- Front end -----
@rx.page(route="/uniques", title="User uniques")
def home() -> rx.Component:
    """Simple play home page."""
    return rx.container(
        rx.heading("Uniques", size="6"),
        rx.vstack(
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="user", name="user_name"
                    ),  # , value=State.user_name),
                    rx.input(
                        placeholder="brewery id",
                        name="brewery_id",
                        type="number",
                        # value=State.brewery_id,
                    ),
                    rx.input(
                        placeholder="max resorts",
                        name="max_resorts",
                        type="number",
                        # value=State.max_resorts,
                    ),
                    rx.button("Submit", type="submit"),
                ),
                on_submit=State.unique_submit,
                reset_on_submit=False,
            ),
            rx.divider(),
        ),
    )
