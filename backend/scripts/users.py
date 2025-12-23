from Database import get_session
from scripts.models import Users as users
from typing import List


def get_all_users(limit: int = 50) -> List[users]:
    session = get_session()
    try:
        all_users = session.query(users).limit(limit).all()
        if not all_users:
            print("No users found")
        return all_users
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
        return {f"message": "{name} created"}
    except Exception as e:
        session.rollback()
        print(f"Error creating user: {e}")
    finally:
        session.close()

def delete_user(user_id: int):
    session = get_session()
    try:
        user = session.query(users).filter(users.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return {"message": "User deleted successfully"}
        else:
            return {"message": "User not found"}
    except Exception as e:
        session.rollback()
        print(f"Error deleting user: {e}")
        return {"message": "Internal error"}
    finally:
        session.close()
