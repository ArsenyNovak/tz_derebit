from fastapi import APIRouter, HTTPException
from sqlalchemy import select, func

from app.database import SessionDep
from app.models import PriceRecord
from app.scheme import PriceListResponse, PriceResponse, TickerPaginationDep, \
    TickerDatePaginationDep, TickerDep

router = APIRouter(prefix='/prices', tags=['Работа с ценой'])


@router.get("/list")
async def get_list_prices(query: TickerPaginationDep, session: SessionDep):
    """Список цен по тикеру"""
    ticker = query.ticker
    total = await session.execute(
        select(func.count(PriceRecord.id)).where(PriceRecord.ticker == ticker)
    )
    total_count = total.scalar_one()

    stmt = (
        select(PriceRecord)
        .where(PriceRecord.ticker == ticker)
        .order_by(PriceRecord.timestamp.desc())
        .offset(query.offset)
        .limit(query.limit)
    )

    result = await session.execute(stmt)
    db_records = result.scalars().all()
    records = [PriceResponse.model_validate(record) for record in db_records]

    return PriceListResponse(
        ticker=ticker,
        records=records,
        total=total_count
    )


@router.get("/latest")
async def get_latest_price(session: SessionDep, query: TickerDep):
    """Последняя цена"""
    ticker = query.ticker
    stmt = (
        select(PriceRecord)
        .where(PriceRecord.ticker == ticker)
        .order_by(PriceRecord.timestamp.desc())
    )
    result = await session.execute(stmt)
    latest = result.scalars().first()

    if not latest:
        raise HTTPException(404, "Нет данных")

    return {
        "ticker": latest.ticker,
        "price": round(latest.price, 2),
        "timestamp": latest.timestamp,
    }


@router.get("/list_by_date")
async def get_prices_by_date(session: SessionDep, query: TickerDatePaginationDep) -> PriceListResponse:
    """Получить цены по тикеру за период дат"""
    ticker = query.ticker
    from_timestamp = query.from_timestamp
    to_timestamp = query.to_timestamp
    if from_timestamp >= to_timestamp:
        raise HTTPException(400, "from_timestamp должен быть меньше to_timestamp")

    # Подсчет общего количества за период
    count_stmt = (
        select(func.count(PriceRecord.id))
        .where(
            PriceRecord.ticker == ticker,
            PriceRecord.timestamp >= from_timestamp,
            PriceRecord.timestamp <= to_timestamp
        )
    )
    total_result = await session.execute(count_stmt)
    total = total_result.scalar_one()

    # Выборка за период с пагинацией
    stmt = (
        select(PriceRecord)
        .where(
            PriceRecord.ticker == ticker,
            PriceRecord.timestamp >= from_timestamp,
            PriceRecord.timestamp <= to_timestamp
        )
        .order_by(PriceRecord.timestamp.desc())
        .offset(query.offset)
        .limit(query.limit)
    )

    result = await session.execute(stmt)
    db_records = result.scalars().all()

    records = [PriceResponse.model_validate(record) for record in db_records]

    return PriceListResponse(
        ticker=ticker,
        records=records,
        total=total
    )
