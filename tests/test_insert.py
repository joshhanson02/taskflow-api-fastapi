from db.database import SessionLocal
from models.user_model import User

db = SessionLocal()

new_user = User(
    username="hieu",
    email="trunghieuidol02@gmail.com",
    password="123456"
)

db.add(new_user)
db.commit()

print("User inserted successfully")
