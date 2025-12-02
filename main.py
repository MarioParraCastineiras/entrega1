from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from configuration.connections import DataBaseConnection
import os
from service.spotify_service import get_Token, get_Artists, get_NewReleases

SPOTIFY_CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URL=os.getenv("SPOTIFY_REDIRECT_URL")
SPOTIFY_CODE=os.getenv("SPOTIFY_CODE")
SPOTIFY_TOKEN_GLOBAL = None

app = FastAPI()

@app.get("/")
def root():
    return("Hello World!")

@app.get("/users")
async def get_user_list():
    mydb = DataBaseConnection(host="localhost", user="root", password="123123123", database="ENTREGA1")
    mydb_conn=mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute("SELECT * FROM users")
    data=mycursor.fetchall()
    mydb_conn.close()
    return data

@app.post("/users")
async def post_users(request: Request):
    mydb = DataBaseConnection(host="localhost", user="root", password="123123123", database="ENTREGA1")
    mydb_conn = mydb.get_connection() 
    request = await request.json()
    username = request['username']
    age = request['age']
    musicStyle = request['musicStyle']
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"INSERT INTO users (username, age, musicStyle) VALUES ('{username}', {age}, '{musicStyle}')")
    mydb_conn.commit()
    return JSONResponse(content={"message": "User added successfully"}, status_code=201)

@app.put("/users/{user_id}")
async def put_users(user_id: int, request: Request):
    #Connexion to dataBase
    mydb = DataBaseConnection(host="localhost", user="root", password="123123123", database="ENTREGA1")
    mydb_conn = mydb.get_connection()
    #datos a json
    request = await request.json()
    username = request['username']
    age = request['age']
    musicStyle = request['musicStyle']

    #cursor
    mycursor = mydb_conn.cursor()

    mycursor.execute(f"UPDATE users SET username = %s, age=%s, musicStyle=%s WHERE id=%s", (username, age, musicStyle, user_id))
    mydb_conn.commit()
    return JSONResponse(content={"message": "User updated successfully"}, status_code=201)
    
@app.delete("/users/{user_id}")
async def delete_users(user_id: int, request: Request):

    mydb = DataBaseConnection(host="localhost", user="root", password="123123123", database="ENTREGA1")
    mydb_conn = mydb.get_connection()
    
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"DELETE FROM users WHERE id=%s", (user_id,))
    mydb_conn.commit()

    return JSONResponse(content={"message": "User deleted successfully"}, status_code=201)

@app.post("/spotify/token")
async def spotifytoken(request: Request):
    global SPOTIFY_TOKEN_GLOBAL
    
    data = await request.json()
    username = data.get("username")

    if not username:
        raise HTTPException(status_code=400, detail="You must provide a username")

    mydb = DataBaseConnection(host="localhost", user="root", password="123123123", database="ENTREGA1")
    mydb_conn = mydb.get_connection()
    mycursor = mydb_conn.cursor()

    mycursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = mycursor.fetchone()
    mydb_conn.commit()

    if not user:
        raise HTTPException(status_code=404, detail="User not registered. Please register to get access")
    
    SPOTIFY_TOKEN_GLOBAL = get_Token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    if "error" in SPOTIFY_TOKEN_GLOBAL:
        raise HTTPException(status_code=404, detail="Token couldn't be generated")
    return JSONResponse(content=SPOTIFY_TOKEN_GLOBAL, status_code=200)
    print(SPOTIFY_TOKEN_GLOBAL)

@app.get("/spotify/artist/{id}")
async def artistinfo(id: str):
    global SPOTIFY_TOKEN_GLOBAL
    artist_data=get_Artists(SPOTIFY_TOKEN_GLOBAL, id)
    if "error" in artist_data:
        raise HTTPException(status_code=404, detail="Artist Not found")
    return JSONResponse(content=artist_data, status_code=200)
    print(artist_data)

@app.get("/spotify/releases")
async def newreleases():
    global SPOTIFY_TOKEN_GLOBAL
    releases_data = get_NewReleases(SPOTIFY_TOKEN_GLOBAL)

    if "error" in releases_data:
        raise HTTPException(status_code=404, detail="Unable to load latest data, try again later")
    return JSONResponse(content=releases_data, status_code=200)
    print(releases_data)
