from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import data_processing

app = FastAPI(title="API for Nuxt + FastAPI example")
router = APIRouter(prefix="/api")


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

@app.get("/")
async def root():
    return {"message": "server is running"}

@app.get("/nums")
async def get_nums():
    result = data_processing.process_dataset()
    return {"numbers": "10"}

@router.get("/team_names")
async def get_team_names():
    names = data_processing.team_names()
    return {"team_names": names}

app.include_router(router)