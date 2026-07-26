"""Assigns each planner step to the specialized agent best suited to
execute it. Rule-based (not an LLM call) by design — this is a
deterministic routing decision, not something that benefits from
generation, and keeping it rule-based means it's fast, free, and
testable without mocking an LLM."""

import re

from app.agents.base_agent import BaseAgent
from app.schemas.supervisor import AgentTask, SupervisorResponse

# Ordered so the first matching keyword wins — more specific terms first.
_KEYWORD_ROUTES: list[tuple[str, str]] = [
    ("restaurant", "restaurant"),
    ("food", "restaurant"),
    ("dining", "restaurant"),
    ("eat", "restaurant"),
    ("budget", "budget"),
    ("cost", "budget"),
    ("price", "budget"),
    ("direction", "maps"),
    ("route", "maps"),
    ("distance", "maps"),
    ("navigat", "maps"),
    ("book", "booking"),
    ("reserv", "booking"),
    ("itinerary", "itinerary"),
    ("schedule", "itinerary"),
    ("day plan", "itinerary"),
    ("activities", "research"),
    ("research", "research"),
    ("explore", "research"),
]


class SupervisorAgent(BaseAgent):
    def decide(self, goal: str, steps: list[str]) -> SupervisorResponse:
        tasks = [AgentTask(agent=self._route(step), action=step) for step in steps]
        return SupervisorResponse(tasks=tasks)

    @staticmethod
    def _route(step: str) -> str:
        lowered = step.lower()
        for keyword, agent in _KEYWORD_ROUTES:
            # Word-boundary match: a plain substring check would let "eat"
            # match inside "weather", misrouting weather questions to the
            # restaurant agent. \b enforces the keyword stands as its own
            # word (or word-start, for stems like "reserv" / "navigat").
            if re.search(rf"\b{re.escape(keyword)}", lowered):
                return agent
        return "travel"
