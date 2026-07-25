from app.tools.base_tool import BaseTool


class FlightTool(BaseTool):

    def run(
        self,
        source: str,
        destination: str,
        budget: int
    ):

        # Mock Data

        return {

            "airline": "IndiGo",

            "price": 5200,

            "departure": "09:30",

            "arrival": "11:15"

        }