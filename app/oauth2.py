from datetime import UTC as datetimeUTC
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status  # type: ignore
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt  # type: ignore
from pydantic import ValidationError
from sqlalchemy.orm import Session

from . import database, models, schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_TIME_IN_MINUTES = 60


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={
        "read": "Read information about the current user",
        "create": "Read todos",
        "delete": "Create anything",
        "update": "Create anything",
    },
)


def create_access_token(token_data: dict):
    access_token_data = token_data.copy()
    access_token_expiry_date = datetime.now(datetimeUTC) + timedelta(
        ACCESS_TOKEN_EXPIRY_TIME_IN_MINUTES
    )

    access_token_data.update({"exp": access_token_expiry_date})
    jwt_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        jwt_payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = jwt_payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_scopes = jwt_payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, user_id=user_id)

    except (JWTError, ValidationError):
        raise credentials_exception

    user = db.query(models.User).filter_by(id=token_data.user_id).first()
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


def get_current_active_user(
    current_user: Annotated[schemas.User, Security(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active"
        )

    return current_user


# def get_current_active_admin_user(
#     current_user: schemas.UserOut = Depends(get_current_active_user),
# ):
#     if not current_user.is_admin:
#         raise Error400("User is not an admin")

#     return current_user


def get_session():
    return database.SessionLocal()
