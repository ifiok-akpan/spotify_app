from ast import Import
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

os.environ['SPOTIPY_CLIENT_ID'] = 'your_client_id'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'your_client_secret'


# Load environment variables from .env file (if using python-dotenv)
# from dotenv import load_dotenv
# load_dotenv()

# Retrieve the credentials from the environment variables
client_id = os.getenv('your_client_id')
client_secret = os.getenv('your_client_secret')

# Initialize the Spotify client with the retrieved credentials
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Function to get all albums of an artist and output in JSON format
def get_michael_jackson_albums_json():
    # Search for Michael Jackson by name
    results = sp.search(q='Michael Jackson', type='artist', limit=1)
    artist_id = results['artists']['items'][0]['id']

    # Fetch all albums by Michael Jackson
    albums = sp.artist_albums(artist_id=artist_id, album_type='album', limit=50)
    album_list = []

    while albums:
        for album in albums['items']:
            album_data = {
                'name': album['name'],
                'release_date': album['release_date'],
                'total_tracks': album['total_tracks'],
                'album_type': album['album_type'],
                'external_url': album['external_urls']['spotify']
            }
            album_list.append(album_data)

        if albums['next']:
            albums = sp.next(albums)
        else:
            albums = None

    # Remove duplicates by converting to a set of tuples, then back to a list of dictionaries
    unique_albums = list({v['name']: v for v in album_list}.values())

    # Output the album list in JSON format
    return json.dumps(unique_albums, indent=4)

# Get the Michael Jackson albums in JSON format
michael_jackson_albums_json = get_michael_jackson_albums_json()

# Print the JSON output
print(michael_jackson_albums_json)

# Optionally, write the JSON output to a file
with open('michael_jackson_albums.json', 'w') as f:
    f.write(michael_jackson_albums_json)
