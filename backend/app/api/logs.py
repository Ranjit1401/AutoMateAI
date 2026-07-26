from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.log import LogOut
from app.services import log_service

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("", response_model=list[LogOut])
def list_logs(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return log_service.list_logs(db, user.id)
