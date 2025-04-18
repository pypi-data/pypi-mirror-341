from typing import List

from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    ProductDto,
    MarketLiquidityDto,
    MarketPriceDto,
    V1ProductGetParametersQuery,
    PageOfProductDtos,
    V1ProductMarketLiquidityGetParametersQuery,
    V1ProductMarketPriceGetParametersQuery,
    ListOfMarketPriceDtos,
)


def list_products(self, **kwargs) -> List[ProductDto]:
    """Lists all products and their configurations.

    Endpoint: GET v1/product

    Returns:
        PageOfProductDtos: List of product configurations.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/product",
        request_model=V1ProductGetParametersQuery,
        response_model=PageOfProductDtos,
        **kwargs,
    )
    return res.data


def get_market_liquidity(self, **kwargs) -> MarketLiquidityDto:
    """Gets market liquidity for a product.

    Endpoint: GET v1/product/market-liquidity

    Returns:
        MarketLiquidityDto: Market liquidity information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/product/market-liquidity",
        request_model=V1ProductMarketLiquidityGetParametersQuery,
        response_model=MarketLiquidityDto,
        **kwargs,
    )
    return res


def list_market_prices(self, **kwargs) -> List[MarketPriceDto]:
    """Gets market prices for multiple products.

    Endpoint: GET v1/product/market-price

    Returns:
        PageOfMarketPriceDtos: List of market prices.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/product/market-price",
        request_model=V1ProductMarketPriceGetParametersQuery,
        response_model=ListOfMarketPriceDtos,
        **kwargs,
    )
    return res.data
