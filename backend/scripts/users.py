import models
import Database as db

users = models.Users

def get_all_users():
    session = db.get_session()
    try:
        users = session.query(users).all()
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
    finally:
        session.close()

def create_user(name: str):
    session = db.get_session()
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
    session = db.get_session()
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

print(get_all_users())