from scripts.models_updated import Users as users
from typing import List
from sqlalchemy.orm import Session


def get_all_users(db: Session) -> List[users]:
    try:
        all_users = db.query(users).all()
        if not all_users:
            print("No users found")
        return all_users
    except Exception as e:
        print(f"Error fetching users: {e}")

def create_user(usr: str, db: Session):
    try:
        user = users(username=usr)
        db.add(user)
        db.commit()
        return {"message": f"{usr} created"}
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
    try:
        user = users(username=usr)
        db.add(user)
        db.commit()
        return {"message": f"{usr} created"}
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")

def delete_user(id: int, db: Session):
    try:
        user = db.query(users).filter(users.user_id == id).first()
        if user:
            db.delete(user)
            db.commit()
            return {"message": "User deleted successfully"}
        else:
            return {"message": "User not found"}
    except Exception as e:
        db.rollback()
        print(f"Error deleting user: {e}")
        return {"message": "Internal error"}
