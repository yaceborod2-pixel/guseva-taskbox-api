from fastapi import FastAPI
from app.routers.health import healthRouter

app=FastAPI(title="Taskbox-api")

app.include_router(healthRouter)