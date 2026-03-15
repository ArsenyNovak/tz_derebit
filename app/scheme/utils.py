from typing import Literal, Annotated

from fastapi import Depends
from pydantic import BaseModel, Field

from app.config import settings


class TickerQuery(BaseModel):
    ticker: Literal[settings.TICKERS] = Field(..., description="Тикер валютной пары")

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
