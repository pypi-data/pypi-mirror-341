from typing import Literal

from pydantic import BaseModel


class OrderRequest(BaseModel):
    itemId: int
    tokenId: str
    currencyId: str
    side: Literal["BUY", "SELL"]
    quantity: float
    amount: float
    curPrice: float
    flag: str
    version: str
    securityRiskToken: str
