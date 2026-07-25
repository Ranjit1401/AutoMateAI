from app.tools.base_tool import BaseTool


class HotelTool(BaseTool):

    def run(
        self,
        city: str,
        budget: int
    ):

        return {

            "hotel": "Sea View Resort",

            "price_per_night": 2800,

            "rating": 4.6

        }