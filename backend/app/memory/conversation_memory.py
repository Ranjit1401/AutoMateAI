from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ConversationMemory:
    session_id: str
    history: List[Dict[str, str]] = field(default_factory=list)

    def add_user_message(self, message: str):
        self.history.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(self, message: str):
        self.history.append({
            "role": "assistant",
            "content": message
        })

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()