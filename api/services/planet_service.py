from uuid import UUID
from api.models.Planet import Planet
from repositories import planet_repository


def get_planets() -> list[Planet]:
    planets = planet_repository.get_planets()

    if not planets:
        return []

    return [Planet(
        id=UUID(planet[0])
    ) for planet in planets]


def get_planet() -> Planet:
    planet = planet_repository.get_planet()

    if not planet:
        return None

    return Planet(
        id=UUID(planet[0])
    )
