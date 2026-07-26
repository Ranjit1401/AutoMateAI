"""Real restaurant discovery via Google Places Nearby Search."""
from app.providers.google_maps_provider import google_maps_provider
from app.tools.base import BaseTool, ToolError


class RestaurantTool(BaseTool):
    name = "restaurant"
    description = "Finds highly-rated restaurants near a destination via Google Places."

    def execute(self, destination: str, cuisine: str | None = None, radius_m: int = 3000) -> list[dict]:
        try:
            location = google_maps_provider.geocode(destination)
            places = google_maps_provider.nearby_places(
                lat=location["lat"],
                lng=location["lng"],
                place_type="restaurant",
                radius_m=radius_m,
                keyword=cuisine,
            )
        except Exception as exc:  # noqa: BLE001
            raise ToolError(f"Restaurant search failed: {exc}") from exc

        places.sort(key=lambda p: (p.get("rating") or 0), reverse=True)
        return places[:8]
