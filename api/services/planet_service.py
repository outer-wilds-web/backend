from uuid import UUID
from api.models.Planet import Planet
from api.repositories import planet_repository


def get_planets() -> list[Planet]:
    planets = planet_repository.get_planets()

    if not planets:
        return []

    return [Planet(
        id=UUID(planet[0]),
        name=str(planet[1])
    ) for planet in planets]


def get_planet(planet_id: UUID) -> Planet:
    planet = planet_repository.get_planet(planet_id)

    if not planet:
        return None

    return Planet(
        id=UUID(planet[0]),
        name=str(planet[1])
    )


def get_planet_by_name(planet_name: str) -> Planet:
    planet = planet_repository.get_planet_by_name(planet_name)

    if not planet:
        return None

    return Planet(
        id=UUID(planet[0]),
        name=str(planet[1])
    )


def create(planet_name: str) -> Planet:
    planet: Planet = Planet(
        name=planet_name
    )
    planet_repository.create(planet.model_dump(by_alias=True))

    planet: Planet = get_planet_by_name(planet_name)
    return planet
