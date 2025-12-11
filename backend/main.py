from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from Database import connect_db, disconnect_db, get_db
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from scripts.schema import TableEnum
from scripts.models import Base
from dotenv import load_dotenv
from fastapi import APIRouter
from Database import engine
import os
import psycopg2
import scripts.users as users_data
import scripts.teamData as team_data
import scripts.seasons as seasons_data
import scripts.playersData as players_data
import scripts.data_insertion as data_insertion


#run uvicorn main:app --reload --port 8000 or fastapi dev main.py --reload --port 8000


app = FastAPI(title="API for Nuxt + FastAPI")
common = APIRouter(prefix="/common")
compare = APIRouter(prefix="/compare")
seasons = APIRouter(prefix="/seasons")
teams = APIRouter(prefix="/teams")
players = APIRouter(prefix="/players")



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("Database created / checked")
    await connect_db()
    yield
    # Shutdown
    await disconnect_db()

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
async def get_users(conn=Depends(get_db)):
    return await users_data.get_all_users(conn)

@app.post("/create-user")
async def create_user(name: str, conn=Depends(get_db)):
    return await users_data.create_user(conn, name)

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(..., description="CSV file to upload"), tables: TableEnum = None, conn=Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files allowed.")
    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="Invalid content type. Only CSV files allowed.")
    try:
        selected_table = tables.value
        
        return data_insertion.insert_to_db(await file, selected_table, conn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV file: {e}")


@app.delete("/delete-user")
async def delete_user(user_id: int, conn=(Depends(get_db))):
    return await users_data.delete_user(conn, user_id)

# from compare page

@compare.get("/Teams")
async def get_team_names(team: str | None = None, season: str | None = None, conn=Depends(get_db)):
    if team and season:
        return await team_data.team_stats_from_season(team, season, conn)
    elif season:
        return await team_data.teams_from_season(season, conn)
    elif team:
        return await seasons_data.stats_for_season(team, conn)
    
    return await team_data.teams(conn)

@compare.get("/Seasons")
async def get_seasons(conn=Depends(get_db)):
    return await seasons_data.seasons(conn)

@compare.get("/Players")
async def get_players():
    return players_data.players()


# common api endpoints
@common.get("/Seasons")
async def get_seasons(conn=Depends(get_db), season: str | None = None, overall: bool = False):
    if season and overall:
        stats = await seasons_data.stats_for_season(conn, season) #call function that return overall stats for season (funcntion is under construction)
        return stats
    return await seasons_data.seasons(conn)
@common.get("/Players")
async def get_players(conn=Depends(get_db)):
    return await players_data.players(conn)
@common.get("/Teams")
async def get_teams(conn=Depends(get_db)):
    return await team_data.teams(conn)



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