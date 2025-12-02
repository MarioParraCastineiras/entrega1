import requests
import base64

def get_Token(client_id: str, client_secret: str):
    url = f"https://accounts.spotify.com/api/token"
    basic_auth = f"{client_id}:{client_secret}"
    basic_auth_bytes = basic_auth.encode("ascii")
    basic_auth_base64 = base64.b64encode(basic_auth_bytes).decode("ascii")
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

def get_Artists(token: str, id: str):
    url=f"https://api.spotify.com/v1/artists/{id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response=requests.get(url, headers=headers)
    print(response)
    if response.status_code != 200:
        return {"error":"Artist not found"}
    artist_data = response.json()
    return artist_data

def get_NewReleases(token:str):
    url=f"https://api.spotify.com/v1/browse/new-releases"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response=requests.get(url, headers=headers)
    print(response)

    if response.status_code != 200:
        return {"error":"Something went wrong, please try again"}
    if response.status_code == 401:
        return{"error": "Valid user authentication required"}
    
    newReleases_data = response.json()
    return newReleases_data



"""

def get_personal_token(client_id: str, client_secret: str, code: str, redirect_url: str):
    url = f"https://accounts.spotify.com/api/token"

    basic_auth = f"{client_id}:{client_secret}"
    basic_auth_bytes = basic_auth.encode("ascii")
    basic_auth_base64 = base64.b64encode(basic_auth_bytes).decode("ascii")

    headers = {
        "Authorization": f"Basic {basic_auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_url
    }

    response = requests.post(url, data=data, headers=headers)
    print (response)
    if response.status_code != 200:
        return {"error":"Token could not be generated"}
    token_data = response.json()

    access_token = token_data.get("access_token")

    return access_token

def get_followed_artists(personal_token: str):
    url=f"https://api.spotify.com/v1/me" #/following?type=artist

    headers = {
        "Authorization": f"Bearer {personal_token}",
    }
    response = requests.get(url, headers=headers)
    print (response)
    if response.status_code != 200:
        return {"error": "Request couldn't be performed. Please Check token caducity"}
    
    artist_data=response.json()
    return artist_data
"""