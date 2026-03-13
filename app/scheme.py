from typing import List, Literal, Annotated

from fastapi import Depends
from pydantic import BaseModel, Field


class TickerQuery(BaseModel):
    ticker: Literal["btc_usd", "eth_usd"] = Field(..., description="Тикер валютной пары")

TickerDep = Annotated[TickerQuery, Depends(TickerQuery)]


class PaginationParams(BaseModel):
    limit: int = Field(5, ge=0, le=100, description='Количество элементов на странице')
    offset: int = Field(0, ge=0, description='Смещение для пагинации')

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]


class TickerPagination(TickerQuery):
    limit: int = Field(5, ge=0, le=100, description='Количество элементов на странице')
    offset: int = Field(0, ge=0, description='Смещение для пагинации')

TickerPaginationDep = Annotated[TickerPagination, Depends(TickerPagination)]


class TickerDatePagination(TickerPagination):
    from_timestamp: int = Field(..., description="Unix timestamp начала периода")
    to_timestamp: int = Field(..., description="Unix timestamp конца периода")

TickerDatePaginationDep = Annotated[TickerDatePagination, Depends(TickerDatePagination)]


class PriceResponse(BaseModel):
    price: float
    timestamp: int

    class Config:
        from_attributes = True


class PriceListResponse(BaseModel):
    ticker: str
    records: List[PriceResponse]
    total: int


class PriceCreate(BaseModel):
    ticker: str
    price: float
