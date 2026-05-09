from db.database import SessionLocal
from models.user_model import User

db = SessionLocal()

user = db.query(User).first()
db.delete(user)
db.commit()
