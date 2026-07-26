"""Deterministic trip-budget calculator. Pure computation (no external API),
combining flight/hotel pricing and a per-person daily spend estimate."""
from app.tools.base import BaseTool, ToolError

# Rough per-day per-person spend (food + local transport + misc), in the
# destination's local currency units, by budget tier.
DAILY_SPEND_BY_TIER = {"budget": 1200, "mid": 2500, "luxury": 6000}


class BudgetCalculatorTool(BaseTool):
    name = "budget_calculator"
    description = "Estimates total trip cost from flight price, hotel price/night, nights, travellers, and spend tier."

    def execute(
        self,
        flight_total: float,
        hotel_price_per_night: float,
        nights: int,
        travellers: int = 1,
        tier: str = "mid",
    ) -> dict:
        if tier not in DAILY_SPEND_BY_TIER:
            raise ToolError(f"Unknown tier '{tier}'. Choose one of: {', '.join(DAILY_SPEND_BY_TIER)}")
        if nights < 0 or travellers < 1:
            raise ToolError("nights must be >= 0 and travellers must be >= 1")

        daily_spend = DAILY_SPEND_BY_TIER[tier] * travellers * nights
        hotel_total = hotel_price_per_night * nights
        grand_total = flight_total + hotel_total + daily_spend

        return {
            "flight_total": flight_total,
            "hotel_total": hotel_total,
            "daily_spend_total": daily_spend,
            "grand_total": grand_total,
            "per_traveller": grand_total / travellers,
            "tier": tier,
            "nights": nights,
            "travellers": travellers,
        }
