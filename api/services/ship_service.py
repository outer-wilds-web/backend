from uuid import UUID

from api.exceptions import AlreadyExistsException
from api.models.Ship import Ship, ShipForCreate, ShipOutput
from api.repositories import ship_repository

def create_ship(ship: ShipForCreate) -> ShipOutput:
    if find_ship_by_owner(ship.owner):
        raise AlreadyExistsException("Ship already exists")
    
    ship: Ship = Ship(
        owner=ship.owner
    )
    ship_repository.create_ship(ship.model_dump(by_alias=True))
    
    # Get the ship with the id
    ship_output: ShipOutput = find_ship_by_owner(ship.owner)
    print(ship_output)
    return ship_output


def get_ships() -> list[ShipOutput]:
    ships = ship_repository.get_ships()
    
    if not ships:
        return []
    
    ships = [{
        'id': UUID(ship[0]),
        'owner': UUID(ship[1])
    } for ship in ships]
    
    return [ShipOutput(
        id=ship['id'],
        owner=ship['owner']
    ) for ship in ships]
    

def find_ship_by_owner(owner: UUID) -> ShipOutput:
    result = ship_repository.find_ship_by_owner(owner)
    
    if not result:
        return None
    
    result = {
        'id': UUID(result[0]),
        'owner': UUID(result[1])
    }
    
    ship_output: ShipOutput = ShipOutput(
        id=result['id'],
        owner=result['owner']
    )
    return ship_output


def find_ship_by_id(ship_id: UUID) -> ShipOutput:
    result = ship_repository.find_ship_by_id(ship_id)
    
    if not result:
        return None
    
    result = {
        'id': UUID(result[0]),
        'owner': UUID(result[1])
    }
    
    ship_output: ShipOutput = ShipOutput(
        id=result['id'],
        owner=result['owner']
    )
    return ship_output