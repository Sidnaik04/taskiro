from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from . import models, schemas


# create
def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


# read by id
def get_task(db: Session, task_id: UUID) -> models.Task | None:
    return db.get(models.Task, task_id)


# read all
def list_tasks(db: Session, q: str | None = None) -> list[models.Task]:
    stmt = select(models.Task).order_by(models.Task.created_at.desc())
    if q:
        stmt = stmt.where(models.Task.title.ilike(f"%{q}%"))
    return list(db.scalars(stmt).all())


# update
def update_task(
    db: Session, task_id: UUID, data: schemas.TaskUpdate
) -> models.Task | None:
    task = get_task(db, task_id)
    if not task:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task


# delete
def delete_task(db: Session, task_id: UUID) -> bool:
    task = get_task(db, task_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True
