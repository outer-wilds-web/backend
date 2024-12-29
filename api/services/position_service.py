from uuid import UUID

from api.models.Ship import Ship, Ship
from api.models.Position import Position
from api.repositories import position_repository


def get_last_position(id: UUID) -> Position:
    result = position_repository.get_last_position(id)

    if not result:
        return None

    position = {
        "id": result[0],
        "x": result[1],
        "y": result[2],
        "z": result[3],
        "time": result[4],
    }
    return position


def get_all_last_position(ids: list[UUID]) -> list[Position]:

    results = position_repository.get_all_last_positions(ids)

    # Transformer les résultats bruts en objets Position
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

    return positions


def get_positions(id: UUID) -> list[Position]:
    # Appelle le repository
    results = position_repository.get_positions(id)

    if not results:
        return []  # Retourne une liste vide si aucune position n'est trouvée

    # Transforme chaque ligne en objet Position
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
    return positions


def get_all_positions(ids: list[UUID]) -> list[list[Position]]:
    # Récupérer toutes les positions via le repository
    raw_results = position_repository.get_all_positions(ids)

    # Transformer les résultats bruts en objets Position et les regrouper par ID
    positions_by_id = {}
    for row in raw_results:
        position = Position(
            id=row[0],
            x=row[1],
            y=row[2],
            z=row[3],
            time=row[4],
        )
        if position.id not in positions_by_id:
            positions_by_id[position.id] = []
        positions_by_id[position.id].append(position)

    # Retourner une liste de listes (chaque sous-liste correspond aux positions d'un ID)
    return [positions for positions in positions_by_id.values()]
