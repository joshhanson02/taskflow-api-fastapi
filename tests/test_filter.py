from db.database import SessionLocal
from models.user_model import User

db = SessionLocal()

user = db.query(User).filter(User.username == "hieu").first()
print(user.email)
