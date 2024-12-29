from uuid import UUID
from config.config import connect_to_db

connection, cursor = connect_to_db()


def create_user(user: dict):
    try:
        cursor.execute(
            """
            INSERT INTO users (id, username, email, hashed_password, roles)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (str(user['id']), user['username'], user['email'],
             user['hashed_password'], user['roles'])
        )
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur: {e}")
        return None


def get_users():
    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs: {e}")
        return None


def find_user_by_email(email: str):
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche de l'utilisateur par email: {e}")
        return None


def find_user_by_id(user_id: UUID):
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche de l'utilisateur par ID: {e}")
        return None


def update_user(user_id: UUID, user: dict):
    try:
        cursor.execute(
            """
            UPDATE users
            SET username = %s, email = %s, roles = %s
            WHERE id = %s
            """,
            (user['username'], user['email'], user['roles'], str(user_id))
        )
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'utilisateur: {e}")
        return None


def delete_user(user_id: UUID):
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (str(user_id),))
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Erreur lors de la suppression de l'utilisateur: {e}")
        return None
