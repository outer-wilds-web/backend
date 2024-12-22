from config.config import connect_to_db
from api.services import user_service
from api.models.User import UserForCreate

def create_users_table():
    connection, cursor = connect_to_db()
    if connection is None or cursor is None:
        print("Erreur de connexion à la base de données.")
        return

    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        username VARCHAR(255),
        hashed_password VARCHAR(255) NOT NULL,
        roles TEXT[]
    )
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'users' créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création de la table 'users': {e}")
    finally:
        cursor.close()
        connection.close()

def initialize_db():
    admin_email = "admin@example.com"
    admin_password = "adminpassword"
    username = "admin"

    # Vérifier si l'administrateur existe déjà
    existing_admin = user_service.find_user_by_email(admin_email)
    if existing_admin:
        print("L'administrateur existe déjà.")
        return

    # Créer un nouvel utilisateur administrateur
    admin_user = UserForCreate(
        email=admin_email,
        password=admin_password,
        username=username
    )

    # Créer l'utilisateur dans la base de données
    created_admin = user_service.create_user(admin_user)
    
    print("created_admin: ", created_admin)

    # Accorder les droits d'administrateur
    user_service.grant_admin(created_admin.id)

    print("Administrateur créé avec succès.")

if __name__ == "__main__":
    create_users_table()
    initialize_db()