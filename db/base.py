# app/db/base.py
# 1. Import Base
from db.base_class import Base
# 2. Import tất cả các model để SQLAlchemy "đăng ký" chúng vào Base.metadata
from models.user_model import User
from models.task_model import Task
# Nếu sau này có thêm model mới, xếp hàng ở đây:
# from models.project_model import Project
