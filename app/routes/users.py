from fastapi import APIRouter, HTTPException, Depends, Security, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])

from .. import models, schemas, oauth2, database, utils


@router.get("/{id}", response_model=schemas.User)
def get_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_active_user, scopes=["read"]
    ),
):
    return db.query(models.User).filter(models.User.id == user_id).first()


@router.get(
    "/{email}",
    response_model=schemas.User,
)
def get_user_by_email(
    email: str,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_active_user, scopes=["read"]
    ),
):
    return db.query(models.User).filter(models.User.email == email).first()


@router.get("/", response_model=list[schemas.User])
def get_users(
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Security(
        oauth2.get_current_active_user, scopes=["read"]
    ),
):
    return db.query(models.User).offset(skip).limit(limit).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(
        email=user.email, role_id=user.role_id, password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
