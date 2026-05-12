from fastapi import APIRouter, Depends
from dependencies.auth_dependency import require_role
from models.user_model import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(
        require_role("admin")
    )
):
    return {
        "message": f"Welcome admin --{current_user.username}--"
    }
