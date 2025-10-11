from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="API for Nuxt + FastAPI example")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI"}

app.include_router(router)
