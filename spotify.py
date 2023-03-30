import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from matplotlib import pyplot as plt
import random
from typing import Any
import csv

# from spotify developer account
SPOTIPY_CLIENT_ID = "158a267327884c17b24134277cbd0032"
SPOTIPY_CLIENT_SECRET = "141d1c21b70940d89ddf3f9b21493e76"

# connecting to spotify api
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# making user enter playlist link
playlist_code = input("Enter the Playlist Link: \n")
playlist_dict = sp.playlist(playlist_code)

# collecting track URIs
playlist_URI = playlist_code.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

# take a sample of 10 random songs
random_songs = random.sample(sp.playlist_tracks(playlist_URI)["items"], 10)


def random_choices() -> dict[(str, str): tuple[float, float]]:
    """Return a list of 10 random song names."""
    # a list for the name of each random song
    song_names = []
    genres = []
    user_songs = {}

    for song in random_songs:
        song_title = song["track"]["name"]
        song_names.append(song_title)
        track_uri = song["track"]["uri"]

        artist_uri = song["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        popularity_score = artist_info["popularity"]
        artist = song["track"]["artists"][0]["name"]
        artist_genres = artist_info["genres"]
        genres.append((artist, popularity_score, artist_genres))

        user_danceability = (sp.audio_features(track_uri)[0]['danceability'])
        user_valence = (sp.audio_features(track_uri)[0]['valence'])
        user_songs[(artist, song_title)] = (user_danceability, user_valence)

    return user_songs


def spotify_runner() -> None:
    """Plot the 10 random songs from the input user's playlist."""
    tup = random_choices(random_songs)
    random_track_names = tup[0]
    x = tup[1]
    y = tup[2]

    plt.scatter(x, y, s=40, c='pink', edgecolor='black', linewidth=1)

    # axis labels
    plt.xlabel('Danceability')
    plt.ylabel('Valence')

    # scatter plot title
    plt.title('Random Songs')

    # shows scatter plot to user and the random songs
    plt.show()
    print(random_track_names)


def csv_reader() -> dict[str: tuple[float, float]]:
    """..."""
    list_of_songs = {}
    with open('Subset_of_song_data.csv') as csv_file:
        rr = csv.reader(csv_file)

        next(rr)
        for row in rr:
            artist = row[3]

            title = row[14]
            danceability = (row[4])
            valence = (row[0])

            list_of_songs[title] = (danceability, valence)

        return list_of_songs


def get_similar_songs(dataset_songs: dict[(str, str): tuple[float, float]], user_songs: dict[(str, str): tuple[float, float]]) -> list:
    """...
        Preconditions:
            - all([0.0 <= s[2] <= 1.0 for s in dataset_songs])
            - all([0.0 <= s[3] <= 1.0 for s in dataset_songs])
            - all([0.0 <= u[1] <= 1.0 for u in users_songs])
            - all([0.0 <= u[2] <= 1.0 for u in user_songs])

        >>> https://open.spotify.com/playlist/10RDYOInFIIVTUC98kA8qW?si=8d4e3b1907ad4dc6
        >>> user_songs = random_choices()
        >>> dataset_songs = {'p': (0.5, 0.61)}
        >>> get_similar_songs(dataset_songs, user_songs)
    """
    similar_songs = []

    for u in user_songs:
        target_danceability = user_songs[u][0]
        target_valence = user_songs[u][1]

        for song in dataset_songs:
            song_name = song
            danceability = dataset_songs[song][0]
            valence = dataset_songs[song][1]

            if (target_danceability - 0.2) <= danceability <= (target_danceability + 0.2) and \
                    (target_valence - 0.2) <= valence <= (target_valence + 0.2):
                similar_songs.append(song_name)
    return similar_songs
