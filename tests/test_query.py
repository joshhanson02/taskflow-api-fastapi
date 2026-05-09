from db.database import SessionLocal
from models.user_model import User

db = SessionLocal()

users = db.query(User).all()

for user in users:
    print(user.username, user.email)
