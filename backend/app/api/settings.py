from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User, UserPreference
from app.schemas.settings import PreferencesOut, PreferencesUpdate

router = APIRouter(prefix="/settings", tags=["Settings"])


def _get_or_create_preferences(db: Session, user_id: str) -> UserPreference:
    prefs = db.get(UserPreference, user_id)
    if prefs is None:
        prefs = UserPreference(user_id=user_id)
        db.add(prefs)
        db.flush()
    return prefs


@router.get("/preferences", response_model=PreferencesOut)
def get_preferences(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _get_or_create_preferences(db, user.id)


@router.put("/preferences", response_model=PreferencesOut)
def update_preferences(payload: PreferencesUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    prefs = _get_or_create_preferences(db, user.id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(prefs, field, value)
    db.commit()
    db.refresh(prefs)
    return prefs
