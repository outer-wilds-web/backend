from uuid import UUID
from config.config import connect_to_db

connection, cursor = connect_to_db()


def get_last_position(id: UUID):
    try:
        cursor.execute(
            """
            SELECT * 
            FROM positions
            WHERE id = %s
            ORDER BY time DESC
            LIMIT 1
            """,
            (str(id),)
        )
        return cursor.fetchone()
    except Exception as e:
        print(
            f"Erreur lors de la recherche de la dernière position pour l'ID {id}: {e}")
        return None


def get_all_last_positions(ship_ids: list[UUID]):
    try:
        # Requête pour récupérer la dernière position pour chaque navire
        cursor.execute(
            """
            SELECT DISTINCT ON (id) id, x, y, z, time
            FROM positions
            WHERE id = ANY(%s)
            ORDER BY id, time DESC
            """,
            (ship_ids,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des dernières positions : {e}")
        return []


def get_positions(id: UUID):
    try:
        cursor.execute(
            """
            SELECT * 
            FROM positions
            WHERE id = %s
            ORDER BY time DESC
            """,
            (str(id),)
        )
        return cursor.fetchall()  # Retourne toutes les lignes
    except Exception as e:
        print(
            f"Erreur lors de la récupération des positions pour l'ID {id}: {e}")
        return []


def get_all_positions(ids: list[UUID]):
    try:
        # Requête SQL pour récupérer toutes les positions pour les IDs donnés
        cursor.execute(
            """
            SELECT id, x, y, z, time
            FROM positions
            WHERE id = ANY(%s)
            ORDER BY id, time ASC
            """,
            (ids,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des positions : {e}")
        return []