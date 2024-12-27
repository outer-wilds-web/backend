from uuid import UUID
from config.config import connect_to_db

connection, cursor = connect_to_db()

def create_ship(ship: dict):
    try:
        cursor.execute(
            """
            INSERT INTO ships (id, owner)
            VALUES (%s, %s)
            """,
            (str(ship['id']), str(ship['owner']))
        )
        connection.commit()
        print(cursor.rowcount)
        return cursor.rowcount
    except Exception as e:
        print(f"Erreur lors de la création du navire: {e}")
        return None
    

def get_ships():
    try:
        cursor.execute("SELECT * FROM ships")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des navires: {e}")
        return None
    

def find_ship_by_id(ship_id: UUID):
    try:
        cursor.execute("SELECT * FROM ships WHERE id = %s", (str(ship_id),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche du navire par ID: {e}")
        return None
    
    
def find_ship_by_owner(owner: UUID):
    try:
        cursor.execute("SELECT * FROM ships WHERE owner = %s", (str(owner),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche du navire par propriétaire: {e}")
        return None