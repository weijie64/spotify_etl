import requests
import os
from dotenv import load_dotenv
import base64
import pandas as pd

load_dotenv()

db_uri = os.getenv('DB_URI')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


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

token = get_spotify_token(client_id, client_secret)

print(token)
