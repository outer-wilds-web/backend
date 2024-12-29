from uuid import UUID
from fastapi import APIRouter, Request, status, Depends, HTTPException

from api.dependancies import auth_required

from api.models.Ship import ShipForCreate, Ship
from api.models.Position import Position
from api.services import ship_service, user_service, position_service

router = APIRouter(
    prefix="/ships",
    tags=["Ship"],
)


@router.get("")
def get_ships() -> list[Ship]:
    return ship_service.get_ships()


@router.get("/user/{user_id}")
def get_ship_by_owner(user_id: UUID) -> list[Ship]:
    ship = ship_service.get_ships_by_owner(user_id)
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ship


@router.get("/{ship_id}")
def get_ship(ship_id: UUID) -> Ship:
    ship = ship_service.get_ship(ship_id)
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ship


@router.post("", dependencies=[Depends(auth_required)])
def create_ship(ship: ShipForCreate, request: Request) -> Ship:
    current_user = request.state.user
    if current_user.id != ship.owner and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if not user_service.get_user_by_id(ship.owner):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ship owner not found")

    return ship_service.create_ship(ship)


@router.get("/position")
def get_all_ship_position() -> list[Position]:
    ship_ids = [ship.id for ship in ship_service.get_ships()]
    return position_service.get_all_last_position(ship_ids)


@router.get("/position/{ship_id}")
def get_ship_position(ship_id: UUID) -> Position:
    ship = ship_service.get_ship(ship_id)
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return position_service.get_last_position(ship_id)


@router.get("/positions")
def get_all_ship_positions() -> list[list[Position]]:
    ship_ids = [ship.id for ship in ship_service.get_ships()]
    return position_service.get_all_positions(ship_ids)


@router.get("/positions/{ship_id}")
def get_ship_positions(ship_id: UUID) -> list[Position]:
    ship = ship_service.get_ship(ship_id)
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")

    return position_service.get_positions(ship_id)
