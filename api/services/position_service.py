from uuid import UUID

from api.models.Ship import Ship, Ship
from api.models.Position import Position
from api.repositories import position_repository
from config.config import get_logger

logger = get_logger()


def get_position(id: UUID) -> Position:
    """Retrieve the latest position for a given entity (ship or planet) by ID.

    Args:
        id (UUID): The unique identifier of the entity.

    Returns:
        Position: The latest position of the entity.
        None: If no position is found.
    """
    logger.info("Fetching the latest position for entity ID: %s", id)
    result = position_repository.get_position(id)

    if not result:
        logger.warning("No position found for entity ID: %s", id)
        return None

    position = Position(
        id=result[0],
        x=result[1],
        y=result[2],
        z=result[3],
        time=result[4],
    )
    logger.debug(
        "Latest position retrieved for entity ID %s: %s", id, position)
    return position


def get_history_positions(id: UUID) -> list[Position]:
    """Retrieve the position history for a given entity (ship or planet) by ID.

    Args:
        id (UUID): The unique identifier of the entity.

    Returns:
        list[Position]: A list of historical positions for the entity.
        []: If no positions are found.
    """
    logger.info("Fetching position history for entity ID: %s", id)
    results = position_repository.get_history_positions(id)

    if not results:
        logger.warning("No position history found for entity ID: %s", id)
        return []

    positions = [
        Position(
            id=row[0],
            x=row[1],
            y=row[2],
            z=row[3],
            time=row[4],
        )
        for row in results
    ]
    logger.debug(
        "Position history retrieved for entity ID %s: %s", id, positions)
    return positions


def add_position(position: Position) -> Position:
    """Add a new position entry for a given entity (ship or planet).

    Args:
        position (Position): The position details to add.

    Returns:
        Position: The added position if successful.
        None: If the position could not be added.
    """
    logger.info("Adding a new position for entity ID: %s", position.id)
    rows_inserted = position_repository.add_position(position)

    if rows_inserted == 1:
        logger.info(
            "Position added successfully for entity ID: %s", position.id)
        return position
    else:
        logger.error("Failed to add position for entity ID: %s", position.id)
        return None
