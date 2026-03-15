from typing import List

from pydantic import BaseModel, ConfigDict


class PriceResponse(BaseModel):
    price: float
    timestamp: int

    model_config = ConfigDict(
        from_attributes=True
    )


class PriceListResponse(BaseModel):
    ticker: str
    records: List[PriceResponse]
    total: int


class PriceCreate(BaseModel):
    ticker: str
    price: float