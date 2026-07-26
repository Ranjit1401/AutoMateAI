"""Live currency conversion via the free, keyless Frankfurter API
(https://www.frankfurter.app, backed by European Central Bank reference
rates). No API key required, so this works out of the box."""
import requests

from app.tools.base import BaseTool, ToolError

_FRANKFURTER_URL = "https://api.frankfurter.app/latest"


class CurrencyConverterTool(BaseTool):
    name = "currency_converter"
    description = "Converts an amount between two currencies using live exchange rates."

    def execute(self, amount: float, from_currency: str, to_currency: str) -> dict:
        from_currency, to_currency = from_currency.upper(), to_currency.upper()

        if from_currency == to_currency:
            return {"amount": amount, "from": from_currency, "to": to_currency, "converted": amount, "rate": 1.0}

        try:
            response = requests.get(
                _FRANKFURTER_URL,
                params={"amount": amount, "from": from_currency, "to": to_currency},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise ToolError(f"Currency conversion failed: {exc}") from exc

        rates = data.get("rates", {})
        if to_currency not in rates:
            raise ToolError(f"No rate available for {from_currency} -> {to_currency}")

        converted = rates[to_currency]
        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "converted": converted,
            "rate": converted / amount if amount else None,
            "date": data.get("date"),
        }
