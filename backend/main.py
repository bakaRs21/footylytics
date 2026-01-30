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
from metrics.PlayerMetrics import player_metrics, playerM_options
from metrics.TeamMetrics import metric_options, team_metrics


#run: uvicorn main:app --reload --port 8000 or fastapi dev main.py --reload --port 8000


app = FastAPI(title="API for Nuxt + FastAPI")
common = APIRouter(prefix="/common", tags=["Common Endpoints"])
compare = APIRouter(prefix="/compare", tags=["Compare Page"])
seasons = APIRouter(prefix="/seasons", tags=["Seasons Page"])
teams = APIRouter(prefix="/teams", tags=["Teams Page"])
players = APIRouter(prefix="/players", tags=["Players Page"])



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
    print("Shutting down backend...")


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
def get_seasons():
    return seasons_data.seasons()

@compare.get("/Players")
async def get_players(player_id: int | None = None, season_id: int | None = None):
    if player_id and season_id:
        return await players_data.player_stats_from_season(player_id, season_id)
    elif player_id:
        return players_data.player_seasons(player_id)
    return await players_data.players()


@common.get("/Teams")
async def get_teams():
    return await team_data.teams()



# from teams page
@teams.get("/{team_id}")
async def get_team_info(team_id: int):
    return team_data.team_info(team_id)

@teams.get("/{team_id}/seasons")
async def get_team_seasons(team_id: int):
    return await team_data.seasons_for_team(team_id)

@teams.get("/{team_id}/season/")
async def get_team_stats(team_id: int, season_id: int | None = None):
    return await team_data.team_stats_from_season(team_id, season_id)


# from players page
@players.get("/{player_id}")
def get_player_info(player_id: int):
    return players_data.player_info(player_id)

@players.get("/{player_id}/seasons")
def get_player(player_id: int):
    return players_data.player_seasons(player_id)

@players.get("/{player_id}/season/{season_id}")
async def get_player_stats(player_id: int, season_id: int):
    return await players_data.player_stats_from_season(player_id, season_id)

# seasons page
@seasons.get("/{season_id}/teams")
def get_teams_in_season(season_id: int):
    return team_data.teams_from_season(season_id)

app.include_router(seasons)
app.include_router(common)
app.include_router(compare)
app.include_router(teams)
app.include_router(players)
app.include_router(player_metrics.router)
app.include_router(playerM_options.router)
app.include_router(team_metrics.router)
app.include_router(metric_options.router)