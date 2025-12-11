import polars as pl

async def get_all_users(conn):
    try:
        rows = await conn.fetch("SELECT id, name FROM Users;")
        return dict(rows)
    except Exception as e:
        return print(f"Error fetching users: {e}")

async def create_user(conn, name: str):
    async with conn.transaction():
        try:
            row = await conn.fetchrow("INSERT INTO Users (name) VALUES ($1) RETURNING id,name;", name)
            print(f"Inserted user: {row}")
        except EncodingWarning as e:
            return print(f"Encoding error: {e}")
            
        except Exception as e:
            return print(f"Error inserting user: {e}")
            
        return dict(row)

async def delete_user(conn, user_id: int):
    async with conn.transaction():
        try:
            row = await conn.fetchrow("DELETE FROM Users WHERE id = $1 RETURNING id,name;", user_id)
            if row is None:
                return print(f"User with id {user_id} not found.")
            else:
                await conn.execute(
                    f"SELECT setval('public.users_id_seq', {row['id']-1})",
                )
                return print(f"Successfully deleted user {row}")
        except Exception as e:
            return print(f"Error deleting user: {e}")