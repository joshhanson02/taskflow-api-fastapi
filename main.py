from fastapi import FastAPI
from controllers import auth_controller, admin_controller, task_controller
from exceptions.auth_exception import AuthException
from handlers.exception_handler import auth_exception_handler
from db.database import Base, engine
from models.user_model import User
from models.task_model import Task
from core.logger import *
from middleware.logging_middleware import *

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "API chạy rồi đấy, bạn có thể test bằng cách truy cập đường dẫn /docs nhé"}


app.add_middleware(LoggingMiddleware)

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

logger.info("Application started")
