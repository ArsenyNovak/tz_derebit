import pytest
from unittest.mock import AsyncMock, MagicMock

from app.models import PriceRecord
from app.scheme.utils import (
    TickerQuery,
    TickerPagination,
    TickerDatePagination
)


@pytest.fixture
def session():
    """Мок сессии БД"""
    session = MagicMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def price_record():
    """Тестовая запись цены"""
    return PriceRecord(
        ticker="eth_usd",
        price=71647.26,
        timestamp=1773579377016400
    )


@pytest.fixture
def ticker_query():
    return TickerQuery(ticker="eth_usd")


@pytest.fixture
def ticker_pagination():
    return TickerPagination(
        ticker="eth_usd",
        limit=10,
        offset=0
    )


@pytest.fixture
def ticker_date_pagination():
    return TickerDatePagination(
        ticker="eth_usd",
        from_timestamp=1773579377014400,
        to_timestamp=1773579377018400,
        limit=10,
        offset=0
    )


@pytest.fixture
def mock_scalars():
    scalars = MagicMock()
    return scalars


@pytest.fixture
def mock_result(mock_scalars):
    result = MagicMock()
    result.scalars.return_value = mock_scalars
    return result




