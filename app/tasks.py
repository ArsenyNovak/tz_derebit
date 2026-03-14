import httpx
from celery import Celery, shared_task


from app.config import settings


import logging

from app.database import sync_session_maker
from app.models import PriceRecord

celery_app = Celery('crypto_client')
celery_app.conf.update(
    broker_url=settings.broker_url,
    result_backend=settings.broker_url,
    beat_schedule={
        'fetch-prices-every-minute': {
            'task': 'app.tasks.fetch_deribit_prices',
            'schedule': 60.0,
        },
    }
)

logger = logging.getLogger(__name__)


class DeribitHTTPXClient:
    def __init__(self):
        self.base_url = 'https://test.deribit.com'
        self.client = httpx.Client(
            timeout=httpx.Timeout(10.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
            headers={"User-Agent": "CryptoClient/1.0"}
        )

    def get_index_price(self, ticker: str):
        """Синхронный httpx запрос"""
        url = f"{self.base_url}/api/v2/public/get_index_price"
        response = self.client.get(url, params={"index_name": ticker})
        response.raise_for_status()  # Аналог requests

        data = response.json()
        return {
            "ticker": ticker,
            "price": float(data["result"]["index_price"]),
            "timestamp": data["usIn"]
        }


# Глобальный клиент (создается один раз)
client = DeribitHTTPXClient()


@shared_task(bind=True, max_retries=3)
def fetch_deribit_prices(self):
    """Celery задача с синхронным httpx"""
    try:
        results = []
        for ticker in settings.TICKERS:
            try:
                price_data = client.get_index_price(ticker)
                results.append(price_data)
                logger.info(f"✅ {ticker}: ${price_data['price']:.2f}")
            except httpx.TimeoutException:
                logger.warning(f"⏰ Timeout {ticker}, retry...")
                raise self.retry(countdown=60)
            except httpx.HTTPStatusError as e:
                logger.error(f"❌ HTTP {e.response.status_code} {ticker}")
            except Exception as e:
                logger.error(f"❌ {ticker}: {e}")

        # Синхронное сохранение (psycopg2)
        with sync_session_maker() as session:
            for result in results:
                session.add(PriceRecord(**result))
            session.commit()

        logger.info(f"💾 Сохранено {len(results)} записей")
        return {"status": "success", "count": len(results)}

    except Exception as exc:
        logger.error(f"💥 Критическая ошибка: {exc}")
        raise self.retry(countdown=300)