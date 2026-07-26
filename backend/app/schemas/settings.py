from pydantic import BaseModel


class PreferencesOut(BaseModel):
    preferred_model: str
    theme: str
    notifications_enabled: bool
    extra: dict | None

    model_config = {"from_attributes": True}


class PreferencesUpdate(BaseModel):
    preferred_model: str | None = None
    theme: str | None = None
    notifications_enabled: bool | None = None
    extra: dict | None = None
