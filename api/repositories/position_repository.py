from uuid import UUID
from api.models.Position import Position

from config.config import connect_to_db
from config.config import get_logger

logger = get_logger()


# Establish database connection
connection, cursor = connect_to_db()


def get_position(id: UUID):
    """Retrieve the latest position for a given entity by ID.

    Args:
        id (UUID): The unique identifier of the entity.

    Returns:
        tuple: The latest position details as a tuple.
        None: If no position is found or an error occurs.
    """
    try:
        logger.info("Fetching the latest position for entity ID: %s", id)
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
        result = cursor.fetchone()
        logger.debug(
            "Latest position retrieved for entity ID %s: %s", id, result)
        return result
    except Exception as e:
        logger.error("Error retrieving latest position for ID %s: %s", id, e)
        return None


def get_history_positions(id: UUID):
    """Retrieve the position history for a given entity by ID.

    Args:
        id (UUID): The unique identifier of the entity.

    Returns:
        list: A list of all position entries for the entity.
        []: If no positions are found or an error occurs.
    """
    try:
        logger.info("Fetching position history for entity ID: %s", id)
        cursor.execute(
            """
            SELECT * 
            FROM positions
            WHERE id = %s
            ORDER BY time DESC
            """,
            (str(id),)
        )
        results = cursor.fetchall()
        logger.debug(
            "Position history retrieved for entity ID %s: %s", id, results)
        return results
    except Exception as e:
        logger.error("Error retrieving position history for ID %s: %s", id, e)
        return []


def add_position(position: Position):
    """Insert a new position entry into the `positions` table.

    Args:
        position (Position): The position details to insert.

    Returns:
        int: The number of rows inserted (1 if successful).
        None: If an error occurs.
    """
    try:
        logger.info("Inserting a new position for entity ID: %s", position.id)
        cursor.execute(
            """
            INSERT INTO positions (id, x, y, z, time)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (str(position.id), position.x, position.y, position.z, position.time)
        )
        connection.commit()
        logger.info(
            "Position inserted successfully for entity ID: %s", position.id)
        return cursor.rowcount
    except Exception as e:
        logger.error("Error inserting position for ID %s: %s", position.id, e)
        return None
