import socket
from typing import Annotated

from fastapi import APIRouter, Depends

from .deps import PooledRedis

router = APIRouter(prefix="/api")


@router.get("/hello")
async def get_hello(redis: Annotated[PooledRedis, Depends()], name: str = "world"):
    lower_name = name.lower()

    return {
        "msg": f"Hello {lower_name.title()}",
        "views": await redis.incr(f"views:{lower_name}"),
        "host": socket.gethostname(),
    }
