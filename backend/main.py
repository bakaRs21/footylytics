import asyncio
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from scripts.schema_updated import TableEnum
from Database import Base, engine, get_session
from fastapi import APIRouter
from scripts import users as users_data
from scripts import teamsData as team_data
from scripts import seasonsData as seasons_data
from scripts import playersData as players_data
from scripts import refereesData as referee_data
from scripts.load_from_csv import run_loader_once, run_loader_periodically
from metrics.PlayerMetrics import player_metrics, playerM_options
from metrics.TeamMetrics import metric_options, team_metrics
from metrics.SeasonMetrics import season_metrics


#run: uvicorn main:app --reload --port 8000 or fastapi dev main.py --reload --port 8000

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("Database created / checked")

    db_gen = get_session()
    db = next(db_gen)
    try:
        await asyncio.to_thread(run_loader_once, db)
        print("Initial data load complete")
        asyncio.create_task(run_loader_periodically(interval_seconds=24*60*60))  # 24 hours
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass
    yield
    # Shutdown
    print("Shutting down backend...")


app = FastAPI(title="API for Nuxt + FastAPI", lifespan=lifespan)

common = APIRouter(prefix="/common", tags=["Common Endpoints"])
compare = APIRouter(prefix="/compare", tags=["Compare Page"])
seasons = APIRouter(prefix="/seasons", tags=["Seasons Page"])
teams = APIRouter(prefix="/teams", tags=["Teams Page"])
players = APIRouter(prefix="/players", tags=["Players Page"])
referees = APIRouter(prefix="/referees", tags=["Referees"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://footylytics.org",
        "https://www.footylytics.org",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "server is running"}

@app.get("/users")
def get_users(db: Session = Depends(get_session)):
    return users_data.get_all_users(db)

@app.post("/create-user")
def create_user(name: str, db: Session = Depends(get_session)):
    return users_data.create_user(name, db)

@app.delete("/delete-user")
async def delete_user(user_id: int, db: Session = Depends(get_session)):
    return users_data.delete_user(user_id, db)

# from compare page

@compare.get("/Teams")
async def get_team_names(team_id: str | None = None, season_id: str | None = None, db: Session = Depends(get_session)):
    if team_id and season_id:
        return "Team stats for specific season coming soon!"
    elif season_id:
        return team_data.teams_from_season(season_id, db)
    elif team_id:
        return await team_data.seasons_for_team(team_id, db)
    return team_data.teams(db)

@compare.get("/Seasons")
def get_seasons(season_id: int | None = None, db: Session = Depends(get_session)):
    if season_id:
        return "Aggregated data for whole season coming soon!"
    return seasons_data.seasons(db)

@compare.get("/Players")
async def get_players(player_id: int | None = None, season_id: int | None = None, limit: int | None = None, db: Session = Depends(get_session)):
    if player_id and season_id:
        return "Player stats for specific season coming soon!"
    elif season_id:
        return players_data.players_from_season(season_id, db)
    elif player_id:
        return players_data.player_seasons(player_id, db)
    return await players_data.players(limit, db)


@common.get("/Teams")
async def get_teams(db: Session = Depends(get_session)):
    return await team_data.teams(db)



# from teams page
@teams.get("/with-seasons")
async def get_all_teams(db: Session = Depends(get_session)):
    return await team_data.teams_with_seasons(db)
@teams.get("/{team_id}")
async def get_team_info(team_id: int, db: Session = Depends(get_session)):
    return team_data.team_info(team_id, db)

@teams.get("/{team_id}/seasons")
async def get_team_seasons(team_id: int, db: Session = Depends(get_session)):
    return await team_data.seasons_for_team(team_id, db)

@teams.get("/{team_id}/season/")
async def get_team_stats(team_id: int, season_id: int | None = None, db: Session = Depends(get_session)):
    return await team_data.team_stats_from_season(team_id, season_id, db)

@teams.get("/{team_id}/matches/{season_id}")
async def get_team_matches(team_id: int, season_id: int, db: Session = Depends(get_session)):
    return await team_data.team_matches(team_id, season_id, db)

# from players page
@players.get("/with-seasons-teams")
async def get_players_with_seasons_teams(db: Session = Depends(get_session)):
    return players_data.player_with_seasons_teams(db)

@players.get("/{player_id}")
def get_player_info(player_id: int, db: Session = Depends(get_session)):
    return players_data.player_info(player_id, db)

@players.get("/{player_id}/seasons")
def get_player(player_id: int, db: Session = Depends(get_session)):
    return players_data.player_seasons(player_id, db)

@players.get("/{player_id}/season/")
async def get_player_stats(player_id: int, season_id: int | None = None, db: Session = Depends(get_session)):
    return await players_data.player_stats_from_season(player_id, season_id, db)

# seasons page
@seasons.get("/{season_id}/teams")
def get_teams_in_season(season_id: int, db: Session = Depends(get_session)):
    return team_data.teams_from_season(season_id, db)

@seasons.get("/{season_id}/matches")
def get_matches_in_season(season_id: int, db: Session = Depends(get_session)):
    return seasons_data.get_matches_in_season(season_id, db)

@referees.get("")
def get_referees(db: Session = Depends(get_session)):
    return referee_data.get_referees(db)

app.include_router(seasons)
app.include_router(common)
app.include_router(compare)
app.include_router(teams)
app.include_router(players)
app.include_router(referees)
app.include_router(season_metrics.router)
app.include_router(player_metrics.router)
app.include_router(playerM_options.router)
app.include_router(team_metrics.router)
app.include_router(metric_options.router)