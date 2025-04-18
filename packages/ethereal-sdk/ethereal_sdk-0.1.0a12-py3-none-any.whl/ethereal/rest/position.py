from typing import List

from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    PositionDto,
    V1PositionGetParametersQuery,
    PageOfPositionDtos,
)


def list_positions(
    self,
    **kwargs,
) -> List[PositionDto]:
    """Lists positions for a subaccount.

    Endpoint: GET v1/position

    Returns:
        PageOfPositionDtos: List of position information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/position",
        request_model=V1PositionGetParametersQuery,
        response_model=PageOfPositionDtos,
        **kwargs,
    )
    return res.data


def get_position(
    self,
    id: str,
    **kwargs,
) -> PositionDto:
    """Gets a specific position by ID.

    Endpoint: GET v1/position/{positionId}

    Args:
        id (str): UUID of the position.

    Returns:
        PositionDto: Position information.
    """
    endpoint = f"{API_PREFIX}/position/{id}"
    res = self.get(endpoint, **kwargs)
    return PositionDto(**res)
