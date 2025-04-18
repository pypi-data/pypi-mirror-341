from typing import List

from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    LinkSignerDto,
    LinkSignerDtoData,
    SignerDto,
    AccountSignerQuotaDto,
    V1LinkedSignerGetParametersQuery,
    PageOfSignersDto,
    V1LinkedSignerQuotaGetParametersQuery,
)
from ethereal.rest.util import generate_nonce


# TODO: Add revoke signer


def list_signers(
    self,
    **kwargs,
) -> List[SignerDto]:
    """Lists signers for a subaccount.

    Endpoint: GET v1/linked-signer

    Returns:
        PageOfSignersDto: List of signer information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/linked-signer",
        request_model=V1LinkedSignerGetParametersQuery,
        response_model=PageOfSignersDto,
        **kwargs,
    )
    return res.data


def get_signer(
    self,
    id: str,
    **kwargs,
) -> SignerDto:
    """Gets a specific signer by ID.

    Endpoint: GET v1/linked-signer/{id}

    Args:
        id (str): UUID of the signer.

    Returns:
        SignerDto: Signer information.
    """
    endpoint = f"{API_PREFIX}/linked-signer/{id}"
    res = self.get(endpoint, **kwargs)
    return SignerDto(**res)


def get_signer_quota(
    self,
    **kwargs,
) -> AccountSignerQuotaDto:
    """Gets the signer quota for a subaccount.

    Endpoint: GET v1/linked-signer/quota

    Returns:
        AccountSignerQuotaDto: Signer quota configuration.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/linked-signer/quota",
        request_model=V1LinkedSignerQuotaGetParametersQuery,
        response_model=AccountSignerQuotaDto,
        **kwargs,
    )
    return res


def link_signer(
    self,
    sender: str,
    signer: str,
    signerSignature: str,
    subaccount: str,
    subaccountId: str,
    **kwargs,
) -> SignerDto:
    """Links a signer to a subaccount.

    Endpoint: POST v1/linked-signer/link

    Args:
        sender (str): Address of the sender.
        signer (str): Address of the signer.
        signerSignature (str): Signature from the signer.
        subaccount (str): Address of the subaccount.
        subaccountId (str): UUID of the subaccount.

    Returns:
        SignerDto: Created signer information.
    """
    endpoint = f"{API_PREFIX}/linked-signer/link"

    domain = self.rpc_config.domain.model_dump(mode="json", by_alias=True)
    primary_type = "LinkSigner"
    types = self.chain.get_signature_types(self.rpc_config, primary_type)

    data = {
        "sender": sender,
        "signer": signer,
        "subaccountId": subaccountId,
        "subaccount": subaccount,
        "nonce": generate_nonce(),
    }
    model_data = LinkSignerDtoData.model_validate(data)
    message = model_data.model_dump(mode="json", by_alias=True)
    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    link_signer = LinkSignerDto(
        data=model_data, signature=signature, signerSignature=signerSignature
    )
    res = self.post(
        endpoint, data=link_signer.model_dump(mode="json", by_alias=True), **kwargs
    )
    return SignerDto(**res)
