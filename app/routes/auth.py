from typing import List, Literal, TypedDict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import exceptions

from .. import database, models, oauth2, schemas, utils

router = APIRouter()

roles_scopes = {
    "user": ["read"],
    "admin": ["read", "create", "delete", "update"],
}


@router.post("/login", response_model=schemas.Token)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter_by(email=credentials.username).first()
    if not user:
        raise exceptions.UnauthorizedException401("The user does not exist")

    is_password_valid = user.verify_password(credentials.password)
    if not is_password_valid:
        raise exceptions.UnauthorizedException401("Email or password is invalid")

    role = db.query(models.Role).filter(models.Role.id == user.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You need to be assigned a role in order to login.",
        )
    user_scopes = roles_scopes[role.name]
    access_token = oauth2.create_access_token(
        {"user_id": user.id, "scopes": user_scopes}
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user}


""" Auth Permissions and Groups"""


permissions_type = Literal["read", "update", "delete", "create"]
permissions = [
    {"content_type": "todos", "permissions": ["read", "update", "create", "delete"]}
]


def create_content_type(content_type: models.ContentType, db: Session):
    content_type = models.ContentType(*content_type.model_dump())
    db.add(content_type)
    db.commit()
    return content_type


def add_permissions(
    permissions: List[permissions_type], content_type: models.ContentType, db: Session
):
    for permission in permissions:
        new_permission = models.Permission(
            name=permission, description=f"Can {permission} {content_type.model}"
        )
        db.add(new_permission)
        db.commit()
        db.refresh()


class ContentPermission(TypedDict):
    content_type: models.ContentType
    permissions: List[permissions_type]


def create_content_type_permissions(permissions: List[ContentPermission], db: Session):
    for permission in permissions:
        content_type = create_content_type({"model": permission.content_type}, db)
        add_permissions(permission.permissions, content_type, db)
