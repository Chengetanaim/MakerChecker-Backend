from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/roles", tags=["Roles"])

from .. import models, schemas, database


@router.post("/")
def create_roles(db: Session = Depends(database.get_db)):
    for role_name in schemas.RoleType:
        role = db.query(models.Role).filter(models.Role.name == role_name.value).first()
        if role:
            continue
        db_role = models.Role(name=role_name.value)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    return {"message": "Roles created successfully"}


@router.get("/")
def get_roles(db: Session = Depends(database.get_db)):
    for role_name in schemas.RoleType:
        role = db.query(models.Role).filter(models.Role.name == role_name.value).first()
        if role:
            continue
        db_role = models.Role(name=role_name.value)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    roles = db.query(models.Role).all()
    return roles
