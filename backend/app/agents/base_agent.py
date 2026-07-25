from abc import ABC
from app.core.llm import llm


class BaseAgent(ABC):

    def __init__(self):
        self.llm = llm