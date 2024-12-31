from uuid import UUID
from config.config import connect_to_db

connection, cursor = connect_to_db()


def create_ship(ship: dict):
    try:
        cursor.execute(
            """
            INSERT INTO ships (id, owner, name)
            VALUES (%s, %s, %s)
            """,
            (str(ship['id']), str(ship['owner']), str(ship['name']))
        )
        connection.commit()

        return cursor.rowcount, str(ship['id'])
    except Exception as e:
        print(f"Erreur lors de la création du vaisseau: {e}")
        return None


def get_ships():
    try:
        cursor.execute("SELECT * FROM ships")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des vaisseaux: {e}")
        return None


def get_ship(ship_id: UUID):
    try:
        cursor.execute("SELECT * FROM ships WHERE id = %s", (str(ship_id),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche du vaisseau par ID: {e}")
        return None


def get_ship_by_name(ship_name):
    try:
        cursor.execute("SELECT * FROM ships WHERE name = %s",
                       (str(ship_name),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche du vaisseau par ID: {e}")
        return None


def get_owner(ship_id: UUID):
    try:
        cursor.execute("SELECT owner FROM ships WHERE id = %s",
                       (str(ship_id),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche du vaisseau par ID: {e}")
        return None


def get_ships_by_owner(owner: UUID):
    try:
        cursor.execute("SELECT * FROM ships WHERE owner = %s", (str(owner),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche du vaisseau par propriétaire: {e}")
        return None
