import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    MODE: str
    DB_NAME : str
    DB_PASSWORD : str
    DB_HOST : str
    DB_PORT : int = 5432
    DB_USER : str

    BROKER_PORT: int = 6379
    BROKER_HOST: str

    TICKERS: tuple = ('btc_usd', 'eth_usd')


    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../" ".env")
    )

    @property
    def database_url_async(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def database_url_sync(self) -> str:
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def broker_url(self) -> str:
        return f'redis://{self.BROKER_HOST}:{self.BROKER_PORT}/0'



settings = Settings()