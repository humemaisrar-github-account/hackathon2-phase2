from sqlmodel import Session, select
from src.database.database import engine
from src.models.user import User

print("Checking users in database...")

with Session(engine) as session:
    users = session.exec(select(User)).all()
    print(f"Found {len(users)} users:")
    for user in users:
        print(f"  ID: {user.id} (type: {type(user.id)})")
        print(f"  Email: {user.email}")
        print()