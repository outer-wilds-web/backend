from uuid import UUID
from typing import List
from fastapi import APIRouter, HTTPException

from api.models.Planet import Planet
from api.models.Position import Position
from api.services import planet_service, position_service
from config.config import get_logger

logger = get_logger()

router = APIRouter(
    prefix="/planets",
    tags=["Planet"]
)


@router.get("", response_model=list[Planet], summary="Retrieve all planets")
def get_planets() -> list[Planet]:
    """Fetch a list of all planets.

    Returns:
        list[Planet]: A list of all planets in the database.
    """
    logger.info("Fetching all planets.")
    planets = planet_service.get_planets()
    logger.debug("Retrieved %d planets.", len(planets))
    return planets


@router.get("/{planet_id}", response_model=Planet, summary="Retrieve a planet by ID")
def get_planet(planet_id: UUID) -> Planet:
    """Fetch a specific planet by its unique ID.

    Args:
        planet_id (UUID): The unique identifier of the planet.

    Returns:
        Planet: The planet details.

    Raises:
        HTTPException: If the planet is not found.
    """
    logger.info("Fetching planet with ID: %s", planet_id)
    planet = planet_service.get_planet(planet_id)
    if not planet:
        logger.warning("Planet with ID %s not found.", planet_id)
        raise HTTPException(status_code=404, detail="Planet not found")
    logger.debug("Planet retrieved: %s", planet)
    return planet


@router.get("/name/{planet_name}", response_model=Planet, summary="Retrieve a planet by name")
def get_planet_by_name(planet_name: str) -> Planet:
    """Fetch a specific planet by its name.

    Args:
        planet_name (str): The name of the planet.

    Returns:
        Planet: The planet details.

    Raises:
        HTTPException: If the planet is not found.
    """
    logger.info("Fetching planet with name: %s", planet_name)
    planet = planet_service.get_planet_by_name(planet_name)
    if not planet:
        logger.warning("Planet with name %s not found.", planet_name)
        raise HTTPException(status_code=404, detail="Planet not found")
    logger.debug("Planet retrieved: %s", planet)
    return planet


@router.get("/position/{planet_id}", response_model=Position, summary="Retrieve a planet's position by ID")
def get_planet_position(planet_id: UUID) -> Position:
    """Fetch the position of a specific planet by its unique ID.

    Args:
        planet_id (UUID): The unique identifier of the planet.

    Returns:
        Position: The position details of the planet.

    Raises:
        HTTPException: If the planet is not found.
    """
    logger.info("Fetching position for planet with ID: %s", planet_id)
    planet = planet_service.get_planet(planet_id)
    if not planet:
        logger.warning("Planet with ID %s not found.", planet_id)
        raise HTTPException(status_code=404, detail="Planet not found")
    position = position_service.get_position(planet_id)
    logger.debug("Position retrieved for planet ID %s: %s",
                 planet_id, position)
    return position


@router.get("/position/name/{planet_name}", response_model=Position, summary="Retrieve a planet's position by name")
def get_planet_position_by_name(planet_name: str) -> Position:
    """Fetch the position of a specific planet by its name.

    Args:
        planet_name (str): The name of the planet.

    Returns:
        Position: The position details of the planet.

    Raises:
        HTTPException: If the planet is not found.
    """
    logger.info("Fetching position for planet with name: %s", planet_name)
    planet = planet_service.get_planet_by_name(planet_name)
    if not planet:
        logger.warning("Planet with name %s not found.", planet_name)
        raise HTTPException(status_code=404, detail="Planet not found")
    position = position_service.get_position(planet.id)
    logger.debug("Position retrieved for planet name %s: %s",
                 planet_name, position)
    return position


@router.get("/positions/{planet_id}", response_model=List[Position], summary="Retrieve a planet's position history by ID")
def get_planet_history_positions(planet_id: UUID) -> List[Position]:
    """Fetch the position history of a specific planet by its unique ID.

    Args:
        planet_id (UUID): The unique identifier of the planet.

    Returns:
        List[Position]: The position history of the planet.

    Raises:
        HTTPException: If the planet is not found.
    """
    logger.info("Fetching position history for planet with ID: %s", planet_id)
    planet = planet_service.get_planet(planet_id)
    if not planet:
        logger.warning("Planet with ID %s not found.", planet_id)
        raise HTTPException(status_code=404, detail="Planet not found")
    positions = position_service.get_history_positions(planet_id)
    logger.debug("Position history retrieved for planet ID %s: %s",
                 planet_id, positions)
    return positions


@router.get("/positions/name/{planet_name}", response_model=List[Position], summary="Retrieve a planet's position history by name")
def get_planet_history_position_by_name(planet_name: str) -> List[Position]:
    """Fetch the position history of a specific planet by its name.

    Args:
        planet_name (str): The name of the planet.

    Returns:
        List[Position]: The position history of the planet.

    Raises:
        HTTPException: If the planet is not found.
    """
    logger.info(
        "Fetching position history for planet with name: %s", planet_name)
    planet = planet_service.get_planet_by_name(planet_name)
    if not planet:
        logger.warning("Planet with name %s not found.", planet_name)
        raise HTTPException(status_code=404, detail="Planet not found")
    positions = position_service.get_history_positions(planet.id)
    logger.debug("Position history retrieved for planet name %s: %s",
                 planet_name, positions)
    return positions
