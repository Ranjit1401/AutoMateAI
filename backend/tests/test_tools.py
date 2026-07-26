import pytest

from app.tools.base import ToolError
from app.tools.budget_tool import BudgetCalculatorTool
from app.tools.currency_tool import CurrencyConverterTool


def test_budget_calculator_computes_grand_total():
    result = BudgetCalculatorTool().execute(
        flight_total=10000, hotel_price_per_night=2000, nights=3, travellers=2, tier="mid",
    )
    assert result["hotel_total"] == 6000
    assert result["grand_total"] == 10000 + 6000 + (2500 * 2 * 3)
    assert result["per_traveller"] == result["grand_total"] / 2


def test_budget_calculator_rejects_unknown_tier():
    with pytest.raises(ToolError):
        BudgetCalculatorTool().execute(flight_total=0, hotel_price_per_night=0, nights=1, tier="platinum")


def test_currency_converter_same_currency_is_identity():
    result = CurrencyConverterTool().execute(amount=100, from_currency="inr", to_currency="INR")
    assert result["converted"] == 100
    assert result["rate"] == 1.0


def test_tool_registry_has_all_expected_tools():
    import app.tools  # noqa: F401 — registers tools
    from app.tools.registry import tool_registry

    expected = {
        "weather", "flight", "hotel", "maps", "restaurant",
        "budget_calculator", "currency_converter", "pdf_generator",
        "booking", "webhook_trigger",
    }
    assert expected.issubset(set(tool_registry.list_tools()))
