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

@router.get("/teams")
async def get_team_names():
    names = data_processing.team_names()
    return {"teams": names}

@router.get("/seasons")
async def get_seasons():
    return data_processing.seasons()

@router.get("/team_seasons/{team}")
async def get_team_seasons(team: str):
    return data_processing.team_seasons(team)

router.get("/team_stats/{team}/{season}")
async def get_team_stats(team: str, season: str):
    return data_processing.team_stats_from_season(team, season)

app.include_router(router)