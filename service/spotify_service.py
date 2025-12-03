import requests
import base64

# OBTENCION DEL TOKEN PARA PODER ACCEDER A LA API PUBLICA DE SPOTIFY
def get_Token(client_id: str, client_secret: str):
    url = f"https://accounts.spotify.com/api/token"
    basic_auth = f"{client_id}:{client_secret}"
    basic_auth_bytes = basic_auth.encode("ascii")
    basic_auth_base64 = base64.b64encode(basic_auth_bytes).decode("ascii") #DADO QUE ESTO LO SUELE HACER POSTMAN DEBEMOS TRANSFORMAR LOS CLIENT ID Y SECRET ID
    headers = {

        "Authorization": f"Basic {basic_auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
                "grant_type": "client_credentials"
    }
    response=requests.post(url, data=data, headers=headers)
    print (response)
    if response.status_code != 200:
        return {"error":"Token could not be generated"}
    token_data = response.json()
    access_token = token_data.get("access_token")
    return access_token

# OBTENCION DEL LOS DATOS DEL ARTISTA SELECCIONADO, SE COMPRUEBA SI EL TOKEN ES VALIDO
def get_Artists(token: str, id: str):
    url=f"https://api.spotify.com/v1/artists/{id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response=requests.get(url, headers=headers)
    print(response)

    if response.status_code == 401:
        return{"token_error": "Valid user authentication required. Please try again with a new token"} #EN CASO DE DEVOLVER 401 = UNAUTHORIZED POR LO QUE EL TOKEN ES PROBABLE QUE ESTE CADUCADO

    if response.status_code != 200:
        return {"error":"Artist not found"}
    artist_data = response.json()
    return artist_data

# OBTENCION DE LOS ULTIMOS LANZAMIENTOS, SE COMPRUEBA SI EL TOKEN ES VALIDO
def get_NewReleases(token:str):
    url=f"https://api.spotify.com/v1/browse/new-releases"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response=requests.get(url, headers=headers)
    print(response)

    if response.status_code == 401:
        return{"token_error": "Valid user authentication required. Please try again with a new token"} #EN CASO DE DEVOLVER 401 = UNAUTHORIZED POR LO QUE EL TOKEN ES PROBABLE QUE ESTE CADUCAD
    if response.status_code != 200:
        return {"error":"Something went wrong, please try again"}
   
    
    newReleases_data = response.json()
    return newReleases_data