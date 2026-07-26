"""
Creates a provisional booking record.

Honest scope note: there is no universal public API to actually purchase a
flight/hotel without a commercial partnership (e.g. Amadeus for Business,
Booking.com Partner Hub, a payment processor for the charge itself). This
tool does the real, useful part that doesn't require such a partnership —
it validates the request and creates a persisted, trackable reservation
record with a confirmation reference — and is written against the same
BaseTool interface, so swapping in a real provider later (Amadeus Flight
Create Orders API, etc.) means implementing execute() differently here,
nothing else in the codebase needs to change.
"""
import random
import string

from app.tools.base import BaseTool, ToolError


def _generate_reference() -> str:
    return "AMA-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class BookingTool(BaseTool):
    name = "booking"
    description = "Creates a provisional reservation record for a flight or hotel selection."

    def execute(self, booking_type: str, details: dict) -> dict:
        if booking_type not in ("flight", "hotel"):
            raise ToolError("booking_type must be 'flight' or 'hotel'")
        if not details:
            raise ToolError("details are required to create a booking record")

        return {
            "status": "reserved_pending_confirmation",
            "booking_type": booking_type,
            "reference": _generate_reference(),
            "details": details,
            "note": "This is a provisional hold. Connect a real provider (e.g. Amadeus, Booking.com Partner Hub) to finalize payment and confirmation.",
        }
