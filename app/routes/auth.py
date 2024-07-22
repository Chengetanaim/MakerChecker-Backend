from fastapi import APIRouter, status, Depends, HTTPException

from .. import schemas, database, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect",
        )

    is_password_correct = utils.verify_password(
        credentials.password, str(user.password)
    )
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect",
        )

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
