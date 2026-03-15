## Design decisions
---
| Решение | Обоснование                                                                                                    |
|:--------|:---------------------------------------------------------------------------------------------------------------|
| httpx   | Выбрана вместо aiohttp так как может работать в синхронном режиме. Celery синхронная библиотека.               |
| celery  | Было обязательным условием. Возможно рассмотрение пакета Taskiq для работы всего кода в асинхронном режиме     |
| docker  | Разделение на 5 контейнеров, вместо 2-ух. Для удобство масштабирования и соблюдения микросервисной архитектуры |


## Local setup
---
1. Run command:  
`git clone https://github.com/ArsenyNovak/tz_derebit`
2. Work directory create file ".env":
    ````
   # .env.example
   
   # PostgreSQL
    DB_NAME=db
    DB_USER=derebit
    DB_PASSWORD=2408derebit2309
    DB_HOST=postgres_derebit
    DB_PORT=5432
   
   # redis
    BROKER_PORT=6379
    BROKER_HOST=redis
   
   MODE=DEV
    ````
3. Run command:  
`docker compose -f docker-compose.app.yml up -d`  
`docker exec derebit_fastapi uv run alembic upgrade head`  
`docker compose -f docker-compose.celery.yml up -d`  
