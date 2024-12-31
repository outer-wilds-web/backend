from uuid import UUID

from api.exceptions import AlreadyExistsException
from api.models.Ship import Ship, ShipForCreate, Ship
from api.repositories import ship_repository


def create_ship(ship: ShipForCreate) -> Ship:
    if get_ship_by_name(ship.name):
        raise AlreadyExistsException("Ship already exists")

    ship: Ship = Ship(
        owner=ship.owner,
        name=ship.name
    )
    _, ship_id = ship_repository.create_ship(ship.model_dump(by_alias=True))

    # Get the ship with the id
    ship_output: Ship = get_ship(ship_id)
    return ship_output


def get_ships() -> list[Ship]:
    ships = ship_repository.get_ships()

    if not ships:
        return []

    return [Ship(
        id=UUID(ship[0]),
        owner=UUID(ship[1]),
        name=str(ship[2])
    ) for ship in ships]


def get_ship(ship_id: UUID) -> Ship:
    result = ship_repository.get_ship(ship_id)

    if not result:
        return None

    return Ship(
        id=UUID(result[0]),
        owner=UUID(result[1]),
        name=str(result[2])
    )


def get_ship_by_name(ship_name: str) -> Ship:
    result = ship_repository.get_ship_by_name(ship_name)

    if not result:
        return None

    return Ship(
        id=UUID(result[0]),
        owner=UUID(result[1]),
        name=str(result[2])
    )


def get_ships_by_owner(owner: UUID) -> Ship:
    result = ship_repository.get_ships_by_owner(owner)

    if not result:
        return None

    return Ship(
        id=UUID(result[0]),
        owner=UUID(result[1]),
        name=str(result[2])
    )


def get_owner(ship_id: UUID) -> UUID:
    owner_id = ship_repository.get_owner(ship_id)[0]
    if not owner_id:
        return None

    return UUID(owner_id)
