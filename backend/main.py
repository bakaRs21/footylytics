from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import data_processing.teams.teamData as team_data
import data_processing.general.generalData as general_data

app = FastAPI(title="API for Nuxt + FastAPI example")
router = APIRouter(prefix="/api")

#run uvicorn main:app --reload --port 8000

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

@router.get("/teams")
async def get_team_names():
    names = team_data.team_names()
    return {"teams": names}

@router.get("/seasons")
async def get_seasons():
    return general_data.seasons()

@router.get("/team_seasons/{team}")
async def get_team_seasons(team: str):
    return team_data.team_seasons(team)

@router.get("/team_stats/{team}/seasons/{season}")
async def get_team_stats(team: str, season: str):
    return team_data.team_stats_from_season(team, season)

app.include_router(router)


# jestli se na to nekdy podivam, tak sem chtel pojmenovat i routery podle toho co delaj/kam patri
# napr. teams_router, players_router apod.
# naštudovat query parametry ve fastapi
# plexac mi neco vypliv o query parametrech, ale moc se mi to nezda, mam pocit ze to bylo trochu jinak
# https://fastapi.tiangolo.com/tutorial/query-params/ a tu je to zase celkem dost obecne takze to bude pro me jeste tezky "orisek"