from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from services.dispatcher import dispatcher_loop
from api import controls, direct, home, info, map, orders

@asynccontextmanager
async def lifespan(app: FastAPI):
    dispatcher_task = asyncio.create_task(dispatcher_loop())
    yield
    dispatcher_task.cancel()

app = FastAPI(title="Home page", lifespan=lifespan)

app.include_router(controls.router, prefix="/controls", tags=["Controls"])
app.include_router(direct.router, prefix="/direct", tags=["Direct"])
app.include_router(home.router, prefix="/home", tags=["Home"])
app.include_router(info.router, prefix="/info", tags=["Info"])
app.include_router(map.router, prefix="/map", tags=["Map"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])