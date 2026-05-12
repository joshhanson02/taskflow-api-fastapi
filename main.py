from fastapi import FastAPI
from controllers import auth_controller
from controllers import admin_controller
app = FastAPI()

app.include_router(
    auth_controller.router
)

app.include_router(
    admin_controller.router
)
