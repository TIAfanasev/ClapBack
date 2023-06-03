from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lifespan import lifespan
from router import apiRouter

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(apiRouter)
