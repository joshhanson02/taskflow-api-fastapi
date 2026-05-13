from fastapi import FastAPI
from controllers import auth_controller, admin_controller, task_controller
from exceptions.auth_exception import AuthException
from handlers.exception_handler import auth_exception_handler
from db.database import Base, engine
from models.user_model import User
from models.task_model import Task
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(
    auth_controller.router
)

app.include_router(
    admin_controller.router
)

app.include_router(
    task_controller.router
)

app.add_exception_handler(
    AuthException,
    auth_exception_handler
)
