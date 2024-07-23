from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from sqlalchemy.orm import sessionmaker
# from sqlalchemyseeder import ResolvingSeeder
from sqlmodel import SQLModel

from app import database
from app.routes import auth, roles, todos, users

app = FastAPI(
    title="MakerChecker",
    description="Maker Checker",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLModel.metadata.create_all(database.engine)

# Configure the seeder
# SQLModel.metadata.create_all(database.engine)
# session = sessionmaker(autocommit=False, autoflush=False, bind=database.engine)
# seeder = ResolvingSeeder(session)
# new_entities = seeder.load_entities_from_json_file("app/seeding/data.json")
# session.commit()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(roles.router)
