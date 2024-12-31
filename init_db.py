from config.config import connect_to_db, get_logger
from api.services import user_service
from api.models.User import UserForCreate

logger = get_logger()


def create_users_table():
    """Create the 'users' table in the database if it doesn't exist."""
    connection, cursor = connect_to_db()
    if connection is None or cursor is None:
        logger.error("Failed to connect to the database.")
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
        logger.info("'users' table created successfully.")
    except Exception as e:
        logger.exception("Error creating 'users' table: %s", e)
    finally:
        cursor.close()
        connection.close()


def create_ships_table():
    """Create the 'ships' table in the database if it doesn't exist."""
    connection, cursor = connect_to_db()
    if connection is None or cursor is None:
        logger.error("Failed to connect to the database.")
        return

    create_table_query = """
    CREATE TABLE IF NOT EXISTS ships (
        id UUID PRIMARY KEY,
        owner UUID,
        name VARCHAR(255)
    )
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        logger.info("'ships' table created successfully.")
    except Exception as e:
        logger.exception("Error creating 'ships' table: %s", e)
    finally:
        cursor.close()
        connection.close()


def create_planets_table():
    """Create the 'planets' table in the database if it doesn't exist."""
    connection, cursor = connect_to_db()
    if connection is None or cursor is None:
        logger.error("Failed to connect to the database.")
        return

    create_table_query = """
    CREATE TABLE IF NOT EXISTS planets (
        id UUID PRIMARY KEY,
        name VARCHAR(255)
    )
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        logger.info("'planets' table created successfully.")
    except Exception as e:
        logger.exception("Error creating 'planets' table: %s", e)
    finally:
        cursor.close()
        connection.close()


def create_positions_table():
    """Create the 'positions' table in the database if it doesn't exist."""
    connection, cursor = connect_to_db()
    if connection is None or cursor is None:
        logger.error("Failed to connect to the database.")
        return

    create_table_query = """
    CREATE TABLE IF NOT EXISTS positions (
        id UUID,
        x FLOAT,
        y FLOAT,
        z FLOAT,
        time TIMESTAMP(3),
        PRIMARY KEY (id, time)
    )
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        logger.info("'positions' table created successfully.")
    except Exception as e:
        logger.exception("Error creating 'positions' table: %s", e)
    finally:
        cursor.close()
        connection.close()


def initialize_db():
    """Initialize the database with an admin user if not already present."""
    admin_email = "admin@example.com"
    admin_password = "adminpassword"
    username = "admin"

    # Check if the admin user already exists
    existing_admin = user_service.get_user_by_email(admin_email)
    if existing_admin:
        logger.info("Admin user already exists.")
        return

    # Create a new admin user
    admin_user = UserForCreate(
        email=admin_email,
        password=admin_password,
        username=username
    )

    # Add the admin user to the database
    try:
        created_admin = user_service.create_user(admin_user)
        logger.info("Admin user created successfully: %s", created_admin)
        # Grant admin rights
        user_service.grant_admin(created_admin.id)
        logger.info("Admin rights granted successfully.")
    except Exception as e:
        logger.exception("Error initializing admin user: %s", e)


if __name__ == "__main__":
    create_users_table()
    create_ships_table()
    create_planets_table()
    create_positions_table()
    initialize_db()
