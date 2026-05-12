from fastapi import FastAPI
from controllers import auth_controller
from controllers import admin_controller
from exceptions.auth_exception import AuthException
from handlers.exception_handler import auth_exception_handler
app = FastAPI()

app.include_router(
    auth_controller.router
)

app.include_router(
    admin_controller.router
)

app.add_exception_handler(
    AuthException,
    auth_exception_handler
)
