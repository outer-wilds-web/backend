from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from functools import partial

from api.dependancies import auth_required, allowed_roles
from api.exceptions import AlreadyExistsException
from api.models.Ship import ShipForCreate, ShipOutput
from api.services import ship_service

router = APIRouter(
    prefix="/ships",
    # dependencies=[Depends(auth_required)],
    tags=["Ship"],
)


@router.get("")
def get_ships() -> list[ShipOutput]:
    return ship_service.get_ships()


@router.get("/user/{user_id}")
def get_ship_by_owner(user_id: UUID) -> ShipOutput:
    ship = ship_service.find_ship_by_owner(user_id)
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ship


@router.get("/{ship_id}")
def get_ship(ship_id: UUID) -> ShipOutput:
    ship = ship_service.find_ship_by_id(ship_id)
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ship


@router.post("")
def create_ship(ship: ShipForCreate) -> ShipOutput:
    return ship_service.create_ship(ship)
