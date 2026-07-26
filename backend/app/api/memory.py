from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.memory import MemoryCreate, MemoryOut
from app.services import memory_service

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.get("", response_model=list[MemoryOut])
def list_memory(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return memory_service.list_memories(db, user.id)


@router.post("", response_model=MemoryOut, status_code=201)
def create_memory(payload: MemoryCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entry = memory_service.add_memory(db, user.id, payload.content, payload.category)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{memory_id}", status_code=204)
def delete_memory(memory_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted = memory_service.delete_memory(db, user.id, memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory entry not found")
    db.commit()
