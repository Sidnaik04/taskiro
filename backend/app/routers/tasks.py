from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db, Base, engine
from .. import crud, schemas
from ..services.ai import prioritize

# Create tables on first run (for tutorial simplicity; in prod use Alembic)
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/tasks", tags=["tasks"])


# create task route
@router.post("", response_model=schemas.TaskOut)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, payload)


# get task by id route
@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# list all the tasks route
@router.get("", response_model=list[schemas.TaskOut])
def list_tasks(
    q: str | None = Query(None, description="Search by title"),
    ai: bool = Query(False, description="AI-prioritized order"),
    db: Session = Depends(get_db),
):
    tasks = [t for t in crud.list_tasks(db, q)]
    if ai and tasks:
        serial = [
            {
                "id": str(t.id),
                "title": t.title,
                "description": t.description or "",
                "deadline": t.deadline.isoformat(),
            }
            for t in tasks
        ]
        order = prioritize(serial)
        by_id = {str(t.id): t for t in tasks}
        ordered = [by_id[i] for i in order["ordered_ids"] if i in by_id]
        return ordered
    return tasks


# update task route
@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: UUID, payload: schemas.TaskUpdate, db: Session = Depends(get_db)
):
    task = crud.update_task(db, task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task


# delete task route
@router.delete("/{task_id}")
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    ok = crud.delete_task(db, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
