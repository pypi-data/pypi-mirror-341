from typing import List
from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    SubaccountDto,
    SubaccountBalanceDto,
    V1SubaccountGetParametersQuery,
    PageOfSubaccountDtos,
    V1SubaccountBalanceGetParametersQuery,
    PageOfSubaccountBalanceDtos,
)


def list_subaccounts(self, **kwargs) -> List[SubaccountDto]:
    """Lists subaccounts for a sender.

    Endpoint: GET v1/subaccount

    Returns:
        PageOfSubaccountDtos: List of subaccount information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/subaccount/",
        request_model=V1SubaccountGetParametersQuery,
        response_model=PageOfSubaccountDtos,
        **kwargs,
    )
    return res.data


def get_subaccount(self, id: str, **kwargs) -> SubaccountDto:
    """Gets a specific subaccount by ID.

    Endpoint: GET v1/subaccount/{subaccountId}

    Args:
        id (str): UUID of the subaccount.

    Returns:
        SubaccountDto: Subaccount information.
    """
    endpoint = f"{API_PREFIX}/subaccount/{id}"
    res = self.get(endpoint, **kwargs)
    return SubaccountDto(**res)


def get_subaccount_balances(self, **kwargs) -> List[SubaccountBalanceDto]:
    """Gets balances for a subaccount.

    Endpoint: GET v1/subaccount/balance

    Returns:
        PageOfSubaccountBalanceDtos: List of balance information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/subaccount/balance",
        request_model=V1SubaccountBalanceGetParametersQuery,
        response_model=PageOfSubaccountBalanceDtos,
        **kwargs,
    )
    return res.data
