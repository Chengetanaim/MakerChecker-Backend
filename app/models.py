import enum
from dataclasses import dataclass
from datetime import datetime

from sqlmodel import Field, SQLModel

from app import utils


@dataclass()
class ContentType(SQLModel, table=True):
    """
    #### This model represents the content type of a model.

    For example:
    For the `Permissions` model as follows:

    ```py
    class Permissions(SQLModel, table=True):
        id: int = Field(primary_key=True)
        name: str
        description: str
    ```

    You need to create a `content-type` entry so that it creates
    permissions for that model in the database.


    ```py
    content_type = ContentType(model="Permissions")
    ```
    """

    __tablename__ = "contenttypes"

    id: int | None = Field(default=None, primary_key=True)
    model: str


# read:users : Can read all users.
# add:users  : Can add new users.
# delete:users : Can delete users.
# update: users : Can update users.


@dataclass()
class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str

    content_type_id: int | None = Field(default=None, foreign_key="contenttypes.id")


# Checkers


@dataclass()
class PermissionsGroup(SQLModel, table=True):
    __tablename__ = "permissions_groups"

    id: int | None = Field(default=None, primary_key=True)
    name: str


# Admin: read:users
# Admin: write:users


@dataclass()
class UserGroup(SQLModel, table=True):
    __tablename__ = "users_groups"

    group_id: int | None = Field(
        default=None, foreign_key="permissions_groups.id", primary_key=True
    )

    permission_id: int | None = Field(
        default=None, foreign_key="permissions.id", primary_key=True
    )


# Tawanda read:users


@dataclass()
class UserPermission(SQLModel, table=True):
    __tablename__ = "users_permissions"

    permission_id: int | None = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)


class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"


@dataclass()
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str = Field(nullable=False)
    is_active: bool = True
    role: Role = Field(default=Role.USER)

    group_id: int | None = Field(default=None, foreign_key="users_groups.group_id")

    def set_password(self, password: str) -> "User":
        if password:
            self.password = utils.hash_password(password)
            return self

    def verify_password(self, password: str) -> "User":
        password_context = utils.CryptContext(schemes=["bcrypt"], deprecated="auto")
        password_context.verify(self.password, password)
        return self


@dataclass()
class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str

    creator_id: int | None = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default=datetime.now)
