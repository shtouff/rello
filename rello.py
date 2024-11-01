import os
import socket

from fastapi import FastAPI
from redis import Redis

app = FastAPI()
redis = Redis(
    host=os.environ.get("RELLO_REDIS_HOST", "127.0.0.1"),
    port=int(os.environ.get("RELLO_REDIS_PORT", "6379")),
    db=int(os.environ.get("RELLO_REDIS_DB", 0)),
)


@app.get("/api/hello")
def get_hello(name: str = "world"):
    canonical = name.lower()

    views = redis.incr(f"views:{canonical}")
    return {
        "msg": f"Hello {name.lower().title()}",
        "views": views,
        "host": socket.gethostname(),
    }
