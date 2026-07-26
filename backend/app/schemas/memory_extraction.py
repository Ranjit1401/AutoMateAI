from pydantic import BaseModel, Field


class MemoryExtraction(BaseModel):
    has_durable_fact: bool = Field(
        description="True only if the message states a durable fact/preference worth remembering "
        "across future conversations (e.g. 'I'm vegetarian', 'I live in Mumbai'). "
        "False for one-off requests, questions, or small talk."
    )
    fact: str | None = Field(default=None, description="The fact, restated concisely in third person, if any.")
    category: str = Field(default="general", description="Short category label, e.g. 'dietary', 'location', 'preference'.")
