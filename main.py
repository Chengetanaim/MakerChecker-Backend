from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemyseeder import ResolvingSeeder
from sqlmodel import Session, SQLModel

from app import database
from app.routes import auth, roles, todos, users

app = FastAPI(
    title="MakerChecker",
    description="Maker Checker",
)

""" Middlewares"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""Seeder"""

# TODO: I am not yet sure if this code should be here.

SQLModel.metadata.create_all(database.engine)

# seeder = ResolvingSeeder(session=db_session)
# new_entities = seeder.load_entities_from_json_file("app/seeding/data.json")
# db_session.commit()
# db_session.close()


""" Routers """
# It adds all the routes to the app.

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(roles.router)
