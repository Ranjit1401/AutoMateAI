class MasterAgent:

    def detect_task(self, text: str):

        text = text.lower()

        if "trip" in text:
            return "travel"

        if "travel" in text:
            return "travel"

        if "flight" in text:
            return "travel"

        if "hotel" in text:
            return "travel"

        if "email" in text:
            return "email"

        if "calendar" in text:
            return "calendar"

        if "code" in text:
            return "coding"

        return "general"