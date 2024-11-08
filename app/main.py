import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from prometheus_client import Histogram, make_asgi_app
from prometheus_async.aio import time

# Метрика для снятия продолжительности запроса
REQ_TIME = Histogram("req_time_seconds", "Time spent in requests")


@time(REQ_TIME)
async def homepage(request):
    await asyncio.sleep(1)
    return JSONResponse({"message": "Hello from Starlette!"})


# Основное приложение Starlette
app = Starlette(
    routes=[
        Route('/', homepage),
    ]
)

# Добавляем /metrics как ASGI-приложение
app.mount("/metrics", make_asgi_app())
