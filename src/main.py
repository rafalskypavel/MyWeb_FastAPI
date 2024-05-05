from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from auth.router import router as router_auth
from operations.router import router as router_operation
from operations.router import router2 as router2

app = FastAPI(
    title="Интернет-магазин пневматического оборудования бренда Frosp"
)

app.include_router(router_auth)
app.include_router(router_operation)
app.include_router(router2)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")