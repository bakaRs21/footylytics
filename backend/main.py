from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
import scripts.teamData as team_data
import scripts.seasons as seasons_data
import scripts.playersData as players_data
import scripts.data_insertion as data_insertion
from scripts.schema import TableEnum

import io
import polars as pl
from Database import engine
from scripts.models import Base
from typing import Literal, get_args



app = FastAPI(title="API for Nuxt + FastAPI")
common = APIRouter(prefix="/common")
compare = APIRouter(prefix="/compare")
seasons = APIRouter(prefix="/seasons")
teams = APIRouter(prefix="/teams")
players = APIRouter(prefix="/players")

#run uvicorn main:app --reload --port 8000 or fastapi dev main.py --reload --port 8000

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("Database created / checked")
    yield
    # Shutdown

@app.get("/")
async def root():
    return {"message": "server is running"}



@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(..., description="CSV file to upload"), tables: TableEnum = None):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files allowed.")
    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="Invalid content type. Only CSV files allowed.")
    try:
        selected_table = tables.value
        uploaded_file = await file.read()
        text_buffer = io.BytesIO(uploaded_file)
        return data_insertion.insert_to_db(text_buffer, selected_table)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV file: {e}")
    
    

# from compare page

@compare.get("/Teams")
async def get_team_names(team: str | None = None, season: str | None = None):
    if team and season:
        return team_data.team_stats_from_season(team, season)
    elif season:
        return team_data.teams_from_season(season)
    elif team:
        return seasons_data.stats_for_season(team)
    
    return team_data.teams()

@compare.get("/Seasons")
async def get_seasons():
    return seasons_data.seasons()

@compare.get("/Players")
async def get_players():
    return players_data.players()

# common api endpoints
@common.get("/Seasons")
async def get_seasons(season: str | None = None, overall: bool = False):
    if season and overall:
        stats = seasons_data.stats_for_season(season)
        return stats
    return seasons_data.seasons()

@common.get("/Players")
async def get_players():
    return players_data.players()

@common.get("/Teams")
async def get_teams():
    return team_data.teams()


# from teams page
@teams.get("/{team}")
async def get_team(team: str):
    return seasons_data.seasons_for_team(team)

@teams.get("/{team}/season/{season}")
async def get_team_stats(team: str, season: str):
    return team_data.team_stats_from_season(team, season)


# from players page


app.include_router(common)
app.include_router(compare)
app.include_router(teams)
app.include_router(players)


# jestli se na to nekdy podivam, tak sem chtel pojmenovat i routery podle toho co delaj/kam patri
# napr. teams_router, players_router apod.
# naštudovat query parametry ve fastapi
# plexac mi neco vypliv o query parametrech, ale moc se mi to nezda, mam pocit ze to bylo trochu jinak
# https://fastapi.tiangolo.com/tutorial/query-params/ a tu je to zase celkem dost obecne takze to bude pro me jeste tezky "orisek"