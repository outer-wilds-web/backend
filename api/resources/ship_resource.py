from uuid import UUID
from typing import List
from fastapi import APIRouter, Request, status, Depends, HTTPException

from api.dependancies import auth_required
from api.exceptions import AlreadyExistsException

from api.models.Ship import ShipForCreate, Ship
from api.models.Position import Position
from api.services import ship_service, user_service, position_service
from config.config import get_logger


logger = get_logger()

router = APIRouter(
    prefix="/ships",
    tags=["Ship"]
)


@router.get("", response_model=list[Ship], summary="Retrieve all ships")
def get_ships() -> list[Ship]:
    """Fetch a list of all ships.

    Returns:
        list[Ship]: A list of all ships in the database.
    """
    logger.info("Fetching all ships.")
    ships = ship_service.get_ships()
    logger.debug("Retrieved %d ships.", len(ships))
    return ships


@router.post("", response_model=Ship, summary="Create a new ship", dependencies=[Depends(auth_required)])
def create_ship(ship: ShipForCreate, request: Request) -> Ship:
    """Create a new ship.

    Args:
        ship (ShipForCreate): The ship details.
        request (Request): The HTTP request, used to get the current user.

    Returns:
        Ship: The created ship.

    Raises:
        HTTPException: If the user is not authorized or the ship owner is not found.
    """
    current_user = request.state.user
    logger.info("Attempting to create a ship for user ID: %s", current_user.id)
    if current_user.id != ship.owner and "admin" not in current_user.roles:
        logger.warning(
            "Unauthorized ship creation attempt by user ID: %s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    if not user_service.get_user_by_id(ship.owner):
        logger.warning("Ship owner with ID %s not found.", ship.owner)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ship owner not found"
        )
    try:
        created_ship = ship_service.create_ship(ship)
        logger.info("Ship created successfully for owner ID: %s", ship.owner)
        return created_ship
    except AlreadyExistsException as e:
        logger.warning("Failed to create ship: %s", str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{ship_id}", response_model=Ship, summary="Retrieve a ship by ID")
def get_ship(ship_id: UUID) -> Ship:
    """Fetch a specific ship by its unique ID.

    Args:
        ship_id (UUID): The unique identifier of the ship.

    Returns:
        Ship: The ship details.

    Raises:
        HTTPException: If the ship is not found.
    """
    logger.info("Fetching ship with ID: %s", ship_id)
    ship = ship_service.get_ship(ship_id)
    if not ship:
        logger.warning("Ship with ID %s not found.", ship_id)
        raise HTTPException(status_code=404, detail="Ship not found")
    logger.debug("Ship retrieved: %s", ship)
    return ship


@router.get("/name/{ship_name}", response_model=Ship, summary="Retrieve a ship by name")
def get_ship_by_name(ship_name: str) -> Ship:
    """Fetch a specific ship by its name.

    Args:
        ship_name (str): The name of the ship.

    Returns:
        Ship: The ship details.

    Raises:
        HTTPException: If the ship is not found.
    """
    logger.info("Fetching ship with name: %s", ship_name)
    ship = ship_service.get_ship_by_name(ship_name)
    if not ship:
        logger.warning("Ship with name %s not found.", ship_name)
        raise HTTPException(status_code=404, detail="Ship not found")
    logger.debug("Ship retrieved: %s", ship)
    return ship


@router.get("/user/{user_id}", response_model=list[Ship], summary="Retrieve ships by owner ID")
def get_ships_by_owner(user_id: UUID) -> list[Ship]:
    """Fetch all ships owned by a specific user.

    Args:
        user_id (UUID): The unique identifier of the user.

    Returns:
        list[Ship]: The list of ships owned by the user.

    Raises:
        HTTPException: If no ships are found for the user.
    """
    logger.info("Fetching ships for user ID: %s", user_id)
    ships = ship_service.get_ships_by_owner(user_id)
    if not ships:
        logger.warning("No ships found for user ID %s.", user_id)
        raise HTTPException(status_code=404, detail="Ships not found")
    logger.debug("Ships retrieved for user ID %s: %s", user_id, ships)
    return ships


@router.get("/position/{ship_id}", response_model=Position, summary="Retrieve a ship's position by ID")
def get_ship_position(ship_id: UUID) -> Position:
    """Fetch the position of a specific ship by its unique ID.

    Args:
        ship_id (UUID): The unique identifier of the ship.

    Returns:
        Position: The position details of the ship.

    Raises:
        HTTPException: If the ship is not found.
    """
    logger.info("Fetching position for ship with ID: %s", ship_id)
    ship = ship_service.get_ship(ship_id)
    if not ship:
        logger.warning("Ship with ID %s not found.", ship_id)
        raise HTTPException(status_code=404, detail="Ship not found")
    position = position_service.get_position(ship_id)
    logger.debug("Position retrieved for ship ID %s: %s", ship_id, position)
    return position


@router.get("/position/name/{ship_name}", response_model=Position, summary="Retrieve a ship's position by name")
def get_ship_position_by_name(ship_name: str) -> Position:
    """Fetch the position of a specific ship by its name.

    Args:
        ship_name (str): The name of the ship.

    Returns:
        Position: The position details of the ship.

    Raises:
        HTTPException: If the ship is not found.
    """
    logger.info("Fetching position for ship with name: %s", ship_name)
    ship = ship_service.get_ship_by_name(ship_name)
    if not ship:
        logger.warning("Ship with name %s not found.", ship_name)
        raise HTTPException(status_code=404, detail="Ship not found")
    position = position_service.get_position(ship.id)
    logger.debug("Position retrieved for ship name %s: %s",
                 ship_name, position)
    return position


@router.get("/positions/{ship_id}", response_model=List[Position], summary="Retrieve a ship's position history by ID")
def get_ship_history_positions(ship_id: UUID) -> List[Position]:
    """Fetch the position history of a specific ship by its unique ID.

    Args:
        ship_id (UUID): The unique identifier of the ship.

    Returns:
        List[Position]: The position history of the ship.

    Raises:
        HTTPException: If the ship is not found.
    """
    logger.info("Fetching position history for ship with ID: %s", ship_id)
    ship = ship_service.get_ship(ship_id)
    if not ship:
        logger.warning("Ship with ID %s not found.", ship_id)
        raise HTTPException(status_code=404, detail="Ship not found")
    positions = position_service.get_history_positions(ship_id)
    logger.debug("Position history retrieved for ship ID %s: %s",
                 ship_id, positions)
    return positions


@router.get("/positions/name/{ship_name}", response_model=List[Position], summary="Retrieve a ship's position history by name")
def get_ship_history_positions_by_name(ship_name: str) -> List[Position]:
    """Fetch the position history of a specific ship by its name.

    Args:
        ship_name (str): The name of the ship.

    Returns:
        List[Position]: The position history of the ship.

    Raises:
        HTTPException: If the ship is not found.
    """
    logger.info("Fetching position history for ship with name: %s", ship_name)
    ship = ship_service.get_ship_by_name(ship_name)
    if not ship:
        logger.warning("Ship with name %s not found.", ship_name)
        raise HTTPException(status_code=404, detail="Ship not found")
    positions = position_service.get_history_positions(ship.id)
    logger.debug("Position history retrieved for ship name %s: %s",
                 ship_name, positions)
    return positions
