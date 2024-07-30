from typing import overload

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from app.validators.user import NewUser

router = APIRouter(prefix="/users", tags=["Users"])

from app import database, models, oauth2, schemas, utils


@router.get("/{id}", response_model=schemas.User)
def get_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        #     oauth2.get_current_active_user, scopes=["read"]
    ),
):
    return db.query(models.User).filter(models.User.id == user_id).first()


@router.get(
    "/{email}",
    response_model=schemas.User,
)
@overload
def get_user(
    email: str,
    db: Session = Depends(database.get_db),
    # current_user: schemas.User = Security(
    #     oauth2.get_current_active_user, scopes=["read"]
    # ),
):
    return db.query(models.User).filter(models.User.email == email).first()


@router.get("/", response_model=list[models.User])
def get_users(
    db: Session = Depends(database.get_db),
    limit: int = 100,
    # current_user: schemas.User = Security(
    #     oauth2.get_current_active_user, scopes=["read"]
    # ),
):
    return db.query(models.User).limit(limit).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.User)
def create_user(
    user: NewUser,
    db: Session = Depends(database.get_db),
    auth: models.User = Depends(oauth2.get_session),
):
    new_user = models.User(email=user.email)
    new_user.set_password(user.password)
    db.add(new_user)

    # new_user.assign_groups(user.groups)
    # new_user.assign_permissions(user.permissions)

    db.commit()
    db.refresh(new_user)
    return new_user
