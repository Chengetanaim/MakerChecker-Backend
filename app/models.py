import enum

from sqlmodel import Field, Relationship, SQLModel


class ContentType(SQLModel, table=True):
    """
    #### This model represents the content type of a model.

    For example, if you have a model called `Permissions` that is defined as follows:

    ```
    class Permissions(SQLModel, table=True):
        id: int = Field(primary_key=True)
        name: str
        description: str
    ```

    You have to add:

    ```
    app_label = "permissions"
    model = "Permission"
    ```
    """

    __tablename__ = "contenttypes"

    id: int | None = Field(default=None, primary_key=True)
    app_label: str
    model: str

    def __repr__(self) -> str:
        return f"{self.app_label}.{self.model}"


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str

    content_type_id: int | None = Field(default=None, foreign_key="contenttypes.id")
    content_type: ContentType | None = Relationship(back_populates="permissions")

    def __repr__(self) -> str:
        return f"{self.name}"


class UserPermission(SQLModel, table=True):
    __tablename__ = "userpermissions"

    permission_id: int | None = Field(foreign_key="permissions.id", primary_key=True)
    permission: Permission | None = Relationship(back_populates="userpermissions")

    user_id: int | None = Field(foreign_key="users.id", primary_key=True)
    user: "User" = Relationship(back_populates="userpermissions")

    def __repr__(self) -> str:
        return f"{self.permission.name}"


class UserGroup(SQLModel, table=True):
    __tablename__ = "usergroups"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    permissions: list["Permission"] = Relationship(back_populates="group")

    def __repr__(self) -> str:
        return f"{self.name}"


class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str
    is_active: bool = True
    role: Role = Field(default=Role.USER)

    group_id: int | None = Field(default=None, foreign_key="usergroups.id")
    group: UserGroup | None = Relationship(back_populates="users")

    permissions: list["UserPermission"] = Relationship(back_populates="user")
    todos: list["Todo"] = Relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f"{self.email}"


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str

    owner_id: int | None = Field(default=None, foreign_key="users.id")
    owner: User | None = Relationship(back_populates="todos")

    def __repr__(self) -> str:
        return f"{self.title}"
