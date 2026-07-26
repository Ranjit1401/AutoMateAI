"""Registers every tool exactly once. Importing this module (done from
app/main.py at startup) populates the shared tool_registry."""
from app.tools.budget_tool import BudgetCalculatorTool
from app.tools.calendar_tool import CalendarTool
from app.tools.currency_tool import CurrencyConverterTool
from app.tools.flight_tool import FlightTool
from app.tools.gmail_tool import GmailTool
from app.tools.hotel_tool import HotelTool
from app.tools.maps_tool import MapsTool
from app.tools.pdf_tool import PDFGeneratorTool
from app.tools.registry import tool_registry
from app.tools.restaurant_tool import RestaurantTool
from app.tools.weather_tool import WeatherTool
from app.tools.webhook_tool import WebhookTriggerTool
from app.tools.booking_tool import BookingTool

for tool_cls in (
    WeatherTool,
    FlightTool,
    HotelTool,
    MapsTool,
    RestaurantTool,
    BudgetCalculatorTool,
    CurrencyConverterTool,
    PDFGeneratorTool,
    BookingTool,
    WebhookTriggerTool,
    GmailTool,
    CalendarTool,
):
    tool_registry.register(tool_cls())
