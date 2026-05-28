from fastapi import FastAPI
from app.api.routes.clients import router as clients_router
from app.api.routes.webhook import router as webhook_router
app = FastAPI()

app.include_router(clients_router)
app.include_router(webhook_router)

@app.get("/")
def health():
    return {"status": "ok"}