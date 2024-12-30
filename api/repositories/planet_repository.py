from uuid import UUID
from config.config import connect_to_db

connection, cursor = connect_to_db()


def get_planets():
    try:
        cursor.execute("SELECT * FROM planets")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des planets: {e}")
        return None


def get_planet(planet_id: UUID):
    try:
        cursor.execute("SELECT * FROM planets WHERE id = %s",
                       (str(planet_id),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche de la planet par ID: {e}")
        return None


def get_planet_by_name(planet_name: str):
    try:
        cursor.execute("SELECT * FROM planets WHERE name = %s",
                       (str(planet_name),))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la recherche de la planet par ID: {e}")
        return None


def create(planet: dict):
    try:
        cursor.execute(
            """
            INSERT INTO planets (id, name)
            VALUES (%s, %s)
            """,
            (str(planet['id']), str(planet['name']))
        )
        connection.commit()

        return cursor.rowcount, str(planet['id'])
    except Exception as e:
        print(f"Erreur lors de la création de la planet: {e}")
        return None
