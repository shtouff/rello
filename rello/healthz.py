from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from .deps import PooledRedis

router = APIRouter(prefix="/healthz")


@router.get("/ready")
async def get_ready(redis: Annotated[PooledRedis, Depends()]):
    # am I ready to accept traffic ? say yes iff I can talk to redis
    if await redis.ping():
        return {"message": "ready"}
    raise HTTPException(status_code=503, detail="Redis unreachable")


@router.get("/live")
async def get_live(redis: Annotated[PooledRedis, Depends()]):
    if await redis.ping():
        return {"message": "alive"}
    raise HTTPException(status_code=503, detail="Redis unreachable")
