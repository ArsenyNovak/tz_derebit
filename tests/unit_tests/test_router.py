import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException

from app.routers import get_latest_price, get_list_prices, get_prices_by_date

from app.models import PriceRecord
from app.scheme.utils import TickerQuery, TickerPagination, TickerDatePagination


@pytest.mark.asyncio
async def test_get_latest_price_success(
    session,
    price_record,
    ticker_query,
    mock_result,
    mock_scalars
):

    mock_scalars.first.return_value = price_record
    session.execute.return_value = mock_result

    result = await get_latest_price(session=session, query=ticker_query)

    assert result["ticker"] == price_record.ticker
    assert result["price"] == round(price_record.price, 2)
    assert result["timestamp"] == price_record.timestamp


@pytest.mark.asyncio
async def test_get_latest_price_not_found(
    session,
    ticker_query,
    mock_result,
    mock_scalars
):

    mock_scalars.first.return_value = None
    session.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc:
        await get_latest_price(session=session, query=ticker_query)

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_get_list_prices(
    session,
    ticker_pagination,
    price_record,
    mock_scalars
):

    count_result = MagicMock()
    count_result.scalar_one.return_value = 1

    data_result = MagicMock()
    mock_scalars.all.return_value = [price_record]
    data_result.scalars.return_value = mock_scalars

    session.execute.side_effect = [count_result, data_result]

    result = await get_list_prices(query=ticker_pagination, session=session)

    assert result.ticker == "eth_usd"
    assert result.total == 1
    assert len(result.records) == 1


@pytest.mark.asyncio
async def test_get_prices_by_date(
    session,
    ticker_date_pagination,
    price_record,
    mock_scalars
):

    count_result = MagicMock()
    count_result.scalar_one.return_value = 1

    data_result = MagicMock()
    mock_scalars.all.return_value = [price_record]
    data_result.scalars.return_value = mock_scalars

    session.execute.side_effect = [count_result, data_result]

    result = await get_prices_by_date(session=session, query=ticker_date_pagination)

    assert result.ticker == "eth_usd"
    assert result.total == 1


@pytest.mark.asyncio
async def test_get_prices_by_date_invalid_range(session, ticker_date_pagination):

    ticker_date_pagination.from_timestamp = 200
    ticker_date_pagination.to_timestamp = 100

    with pytest.raises(HTTPException) as exc:
        await get_prices_by_date(session=session, query=ticker_date_pagination)

    assert exc.value.status_code == 400