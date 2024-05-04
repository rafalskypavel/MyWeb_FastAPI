from fastapi import FastAPI

from auth.router import router as router_auth
from operations.router import router as router_operation

app = FastAPI(
    title="Интернет-магазин пневматического оборудования бренда Frosp"
)

app.include_router(router_auth)
app.include_router(router_operation)