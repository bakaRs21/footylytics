from Database import get_session
from scripts.models import Users as users
from typing import List


def get_all_users(limit: int = 50) -> List[users]:
    session = get_session()
    try:
        users = session.query(users).limit(limit).all()
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
    finally:
        session.close()

def create_user(name: str):
    session = get_session()
    try:
        user = users(name=name)
        session.add(user)
        session.commit()
        print(f"User created successfully: {user}")
    except Exception as e:
        session.rollback()
        print(f"Error creating user: {e}")
    finally:
        session.close()

async def delete_user(user_id: int):
    session = get_session()
    try:
        user = session.query(users).filter(users.id == user_id)
        if user:
            session.delete(user)
            session.commit()
            return {"message": "User deleted successfully"}
        else:
            return {"message": "User not found"}
    except Exception as e:
        session.rollback()
        print(f"Error deleting user: {e}")
    finally:
        session.close()
