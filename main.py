from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import database, models


from app.routes import auth, todos, users, roles


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

models.Base.metadata.create_all(bind=database.engine)


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(roles.router)
