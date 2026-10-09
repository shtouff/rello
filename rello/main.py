from aioprometheus import MetricsMiddleware
from aioprometheus.asgi.starlette import metrics
from fastapi import FastAPI

from . import api, healthz

app = FastAPI()

app.include_router(api.router)
app.include_router(healthz.router)

app.add_middleware(MetricsMiddleware)
app.add_route("/metrics", metrics)
