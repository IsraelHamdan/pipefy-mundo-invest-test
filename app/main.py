from fastapi import FastAPI
from app.api.routes.clients import router as clients_router
from app.api.routes.webhook import router as webhook_router
from contextlib import asynccontextmanager
from app.db.connection import engine, Base
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app): 
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    lifespan=lifespan
)

app.include_router(clients_router)
app.include_router(webhook_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}