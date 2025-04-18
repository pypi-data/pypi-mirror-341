import time
from decimal import Decimal
from typing import List

from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    TokenDto,
    WithdrawDto,
    TransferDto,
    InitiateWithdrawDto,
    InitiateWithdrawDtoData,
    V1TokenGetParametersQuery,
    V1TokenTransferGetParametersQuery,
    V1TokenWithdrawGetParametersQuery,
    PageOfTokensDtos,
    PageOfTransfersDtos,
    PageOfWithdrawDtos,
)
from ethereal.rest.util import generate_nonce


def list_tokens(
    self,
    **kwargs,
) -> List[TokenDto]:
    """Lists all tokens.

    Endpoint: GET v1/token

    Returns:
        PageOfTokensDtos: A list containing all token information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/token",
        request_model=V1TokenGetParametersQuery,
        response_model=PageOfTokensDtos,
        **kwargs,
    )
    return res.data


def get_token(
    self,
    id: str,
    **kwargs,
) -> TokenDto:
    """Gets a specific token by ID.

    Endpoint: GET v1/token/{id}

    Args:
        id (str): The token identifier.

    Returns:
        TokenDto: The requested token information.
    """
    endpoint = f"{API_PREFIX}/token/{id}"
    res = self.get(endpoint, **kwargs)
    return TokenDto(**res)


def list_token_withdraws(
    self,
    **kwargs,
) -> List[WithdrawDto]:
    """Lists token withdrawals for a subaccount.

    Endpoint: GET v1/token/withdraw

    Returns:
        PageOfWithdrawDtos: A list of withdrawal information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/token/withdraw",
        request_model=V1TokenWithdrawGetParametersQuery,
        response_model=PageOfWithdrawDtos,
        **kwargs,
    )
    return res.data


def list_token_transfers(
    self,
    **kwargs,
) -> List[TransferDto]:
    """Lists token transfers for a subaccount.

    Endpoint: GET v1/token/transfer

    Returns:
        PageOfTransfersDtos: A list of transfer information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/token/transfer",
        request_model=V1TokenTransferGetParametersQuery,
        response_model=PageOfTransfersDtos,
        **kwargs,
    )
    return res.data


def withdraw_token(
    self,
    subaccount: str,
    token_id: str,
    token: str,
    amount: int,
    account: str,
    **kwargs,
):
    """Initiates a token withdrawal.

    Endpoint: POST v1/token/{tokenId}/withdraw

    Args:
        subaccount (str): UUID of the registered subaccount.
        token_id (str): UUID of the token.
        token (str): Token address.
        amount (int): Amount to withdraw.
        account (str): Destination address.

    Returns:
        WithdrawDto: The withdrawal information.
    """
    endpoint = f"{API_PREFIX}/token/{token_id}/withdraw"

    domain = self.rpc_config.domain.model_dump(mode="json", by_alias=True)
    primary_type = "InitiateWithdraw"
    types = self.chain.get_signature_types(self.rpc_config, primary_type)

    nonce = generate_nonce()
    signed_at = str(int(time.time()))

    withdraw_data = {
        "account": account,
        "subaccount": subaccount,
        "token": token,
        "amount": amount,
        "nonce": nonce,
        "signedAt": signed_at,
    }
    message = {
        "account": account,
        "subaccount": subaccount,
        "token": token,
        "amount": str(Decimal(amount * 1e9)),
        "nonce": nonce,
        "signedAt": signed_at,
    }

    data = InitiateWithdrawDtoData.model_validate(withdraw_data)
    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    initiate_withdraw = InitiateWithdrawDto(data=data, signature=signature)
    response = self.post(
        endpoint,
        data=initiate_withdraw.model_dump(mode="json", by_alias=True),
        **kwargs,
    )
    return WithdrawDto(**response)
