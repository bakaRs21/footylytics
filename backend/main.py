import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from scripts.schema_updated import TableEnum
from Database import Base, engine
from fastapi import APIRouter
from scripts import users as users_data
from scripts import teamData as team_data
from scripts import seasons as seasons_data
from scripts import playersData as players_data
from scripts.load_from_csv import run_loader_once, run_loader_periodically
from metrics.PlayerMetrics import metrics as player_metrics


#run uvicorn main:app --reload --port 8000 or fastapi dev main.py --reload --port 8000


app = FastAPI(title="API for Nuxt + FastAPI")
common = APIRouter(prefix="/common")
compare = APIRouter(prefix="/compare", tags=["Compare Page"])
seasons = APIRouter(prefix="/seasons")
teams = APIRouter(prefix="/teams")
players = APIRouter(prefix="/players")



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("Database created / checked")
    await asyncio.to_thread(run_loader_once)
    print("Initial data load complete")
    asyncio.create_task(run_loader_periodically(interval_seconds=24*60*60))  # 24 hours
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)

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

@app.get("/users")
def get_users():
    return users_data.get_all_users()

@app.post("/create-user")
def create_user(name: str):
    return users_data.create_user(name)

@app.delete("/delete-user")
async def delete_user(user_id: int):
    return users_data.delete_user(user_id)

# from compare page

@compare.get("/Teams")
def get_team_names(team: str | None = None, season: str | None = None):
    if team and season:
        return team_data.team_stats_from_season(team, season)
    elif season:
        return team_data.teams_from_season(season)
    elif team:
        return seasons_data.seasons_for_team(team)
    return team_data.teams()

@compare.get("/Seasons")
async def get_seasons():
    return await seasons_data.seasons()

@compare.get("/Players")
async def get_players(player: str | None = None):
    if player:
        return await players_data.player_seasons(player)
    return await players_data.players()


@common.get("/Teams")
async def get_teams():
    return await team_data.teams()



# from teams page
@teams.get("/{team}")
async def get_team(team: str):
    return await seasons_data.seasons_for_team(team)

@teams.get("/{team}/season/{season}")
async def get_team_stats(team: str, season: str):
    return await team_data.team_stats_from_season(team, season)


# from players page


app.include_router(common)
app.include_router(compare)
app.include_router(teams)
app.include_router(players)
app.include_router(player_metrics.router)