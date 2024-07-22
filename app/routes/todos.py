from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, Security

router = APIRouter(prefix="/todos", tags=["Todos"])

from .. import models, schemas, oauth2, database


@router.get("/", response_model=list[schemas.Todo])
def get_todos(
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Security(
        oauth2.get_current_active_user, scopes=["read"]
    ),
):
    return db.query(models.Todo).offset(skip).limit(limit).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Todo)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_active_user, scopes=["create"]
    ),
):
    db_todo = models.Todo(**todo.model_dump(), owner_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
