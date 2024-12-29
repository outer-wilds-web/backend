from uuid import UUID
from config.config import connect_to_db

connection, cursor = connect_to_db()


def get_planets():
    try:
        cursor.execute("SELECT * FROM planets")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des navires: {e}")
        return None


def get_planet(planet_id: UUID):
    try:
        cursor.execute("SELECT * FROM planets WHERE id = %s",
                       (str(planet_id),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche du navire par ID: {e}")
        return None
