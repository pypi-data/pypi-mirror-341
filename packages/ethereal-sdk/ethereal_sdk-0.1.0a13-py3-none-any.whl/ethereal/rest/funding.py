from typing import List
from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    FundingDto,
    V1FundingGetParametersQuery,
    PageOfFundingDtos,
    V1FundingProjectedGetParametersQuery,
    ProjectedFundingDto,
)


def list_funding(self, **kwargs) -> List[FundingDto]:
    """Lists funding rates for a product over time.

    Endpoint: GET v1/funding

    Returns:
        PageOfFundingDtos: List of funding information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/funding",
        request_model=V1FundingGetParametersQuery,
        response_model=PageOfFundingDtos,
        **kwargs,
    )
    return res.data


def get_projected_funding(self, **kwargs) -> ProjectedFundingDto:
    """Fetches the projected funding rate for a product.

    Endpoint: GET v1/funding/projected

    Returns:
        ProjectedFundingDto: Projected funding rate for the next hour.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/funding/projected",
        request_model=V1FundingProjectedGetParametersQuery,
        response_model=ProjectedFundingDto,
        **kwargs,
    )
    return res
