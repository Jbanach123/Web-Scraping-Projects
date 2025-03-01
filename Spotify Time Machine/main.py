import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lxml
import os
import pprint

""" Spotify Authentication """
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["CLIENT_ID"],
                                               client_secret=os.environ["CLIENT_SECRET"],
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               requests_session=True,
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username=os.environ["USERNAME"]
                                               )
                     )
user_id = sp.current_user()["id"]

""" Scraping Billboard 100 """
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
year = date.split("-")[0]
URL = f"https://www.billboard.com/charts/hot-100/{date}"
print(URL)
response = requests.get(URL)
songs = response.text
soup = BeautifulSoup(songs, "lxml")
titles = soup.select("li ul li h3")
songs_list = [title.getText().strip() for title in titles]
# print(songs_list)

""" Searching Spotify for songs by title """
songs_uri = []
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # pprint.pp(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")
# print(songs_uri)
""" Creating a new private playlist in spotify and adding found songs"""
playlist = sp.user_playlist_create(user=user_id, name=f"Top 100 Billboard songs from {date} ", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)
print(playlist)
