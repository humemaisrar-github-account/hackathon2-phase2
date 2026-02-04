from sqlmodel import Session, select
from src.database.database import engine
from src.models.user import User
import uuid

print("Checking user ID type in database...")

with Session(engine) as session:
    user = session.exec(select(User).where(User.email == "testnew@example.com")).first()
    if user:
        print(f"User ID: {user.id}")
        print(f"User ID type: {type(user.id)}")

        # Test comparison
        url_user_id = "4f79bcaa-0e63-4f86-9f6e-9133dd05642e"
        print(f"URL ID: {url_user_id}")
        print(f"URL ID type: {type(url_user_id)}")

        print(f"Direct comparison (user.id == url_user_id): {user.id == url_user_id}")
        print(f"Convert string to UUID: {user.id == uuid.UUID(url_user_id)}")
        print(f"Convert user.id to string: {str(user.id) == url_user_id}")
    else:
        print("User not found")