"""Real Google Maps tool: geocoding + directions between two places."""
from app.providers.google_maps_provider import google_maps_provider
from app.tools.base import BaseTool, ToolError


class MapsTool(BaseTool):
    name = "maps"
    description = "Gets directions (distance/duration/steps) between two locations via Google Maps."

    def execute(self, origin: str, destination: str, mode: str = "driving") -> dict:
        try:
            return google_maps_provider.directions(origin=origin, destination=destination, mode=mode)
        except Exception as exc:  # noqa: BLE001
            raise ToolError(f"Directions lookup failed: {exc}") from exc
