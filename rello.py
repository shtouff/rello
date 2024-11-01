import os
import socket

from fastapi import FastAPI, Request, BackgroundTasks
from prometheus_client import Counter, multiprocess, CollectorRegistry, make_asgi_app
from redis import Redis

app = FastAPI()
redis = Redis(
    host=os.environ.get("RELLO_REDIS_HOST", "127.0.0.1"),
    port=int(os.environ.get("RELLO_REDIS_PORT", "6379")),
    db=int(os.environ.get("RELLO_REDIS_DB", 0)),
)
metrics = {"requests": Counter("requests", "Number of requests", labelnames=["path"])}


# Using multiprocess collector for registry
def make_metrics_app():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return make_asgi_app(registry=registry)


metrics_app = make_metrics_app()
app.mount("/metrics", metrics_app)


@app.middleware("http")
async def execute_after_each_api_request(
    request: Request,
    call_next,
):
    response = await call_next(request)

    # we want to increment counter iff the api was hit. Do not count /metrics or /docs.
    if request.url.path.startswith("/api/"):

        async def increment_requests_counter(url_path: str):
            metrics["requests"].labels(path=url_path).inc()

        bg_tasks = BackgroundTasks()
        bg_tasks.add_task(increment_requests_counter, request.url.path)
        response.background = bg_tasks

    return response


@app.get("/api/hello")
async def get_hello(name: str = "world"):
    lower_name = name.lower()

    return {
        "msg": f"Hello {lower_name.title()}",
        "views": redis.incr(f"views:{lower_name}"),
        "host": socket.gethostname(),
    }
