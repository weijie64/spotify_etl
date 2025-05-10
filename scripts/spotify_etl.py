import requests
import os
from dotenv import load_dotenv
import base64
import pandas as pd
from utils_sql import upsert_dataframe

load_dotenv()

db_uri = os.getenv('DB_URI')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
artist_list = ['Drake','Kendrick Lamar','J Cole','Taylor Swift','SZA']

if not client_id or not client_secret:
    raise ValueError("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET")

def get_spotify_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers={'Authorization': f'Basic {b64_auth_str}',},
        data={'grant_type': 'client_credentials'}
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get token: {response.status_code}, {response.text}")

    token = response.json()['access_token']
    return token


def get_artist_data(token, artists):
    url = f"https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    results = []    

    for name in artists:
        params = {'q': name, 'type': 'artist', 'limit': 1}
        response = requests.get(url, headers=headers,params=params)
        response.raise_for_status()
        data = response.json()
        artist = data['artists']['items'][0]
        results.append(
            {
                'id': artist['id'],
                'name': artist['name'],
                'genres': artist['genres'],
                'followers': artist['followers']['total'],
                'popularity': artist['popularity'],
                'spotify_url': artist['external_urls']['spotify']
            }
        )
    return pd.DataFrame(results)

def run_etl():
    token = get_spotify_token(client_id, client_secret)
    df = get_artist_data(token, artist_list)
    if not df.empty:
        df['updated_at'] = pd.Timestamp.now()
        upsert_dataframe(df,db_uri,'spotify_artists','id')        
        print("ETL complete")
    else:
        print("No data returned")