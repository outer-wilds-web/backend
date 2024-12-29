from uuid import UUID
from fastapi import APIRouter, Request, status, Depends, HTTPException

from api.models.Planet import Planet
from api.services import planet_service

router = APIRouter(
    prefix="/planets",
    tags=["Planet"]
)


@router.get("")
def get_planets() -> list[Planet]:
    return planet_service.get_planets()


@router.get("/{planet_id}")
def get_planet(planet_id: UUID) -> Planet:
    planet = planet_service.get_planet(planet_id)
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet
