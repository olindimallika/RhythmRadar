import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
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


def random_choices() -> dict[tuple[str, str]: tuple[float, float]]:
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


def csv_reader() -> dict[tuple[str, str]: tuple[float, float]]:
    """..."""
    list_of_songs = {}
    with open('practice_data.csv') as csv_file:
        rr = csv.reader(csv_file)

        next(rr)
        for row in rr:
            # for i in range(0, len(row)):
            #     if row[i] == row[3]:
            #         list(row[3])
            res = []
            lst = []
            value = len(row)
            if value > 19:
                for i in range(3, (value - (19 - 4))):

                    lst.extend(list(map(str.strip, row[i].split(','))))
                artist = lst[0]
                title = row[(value - 19) + 14]
                danceability = float(row[(value - (19 - 4))])
                valence = float(row[0])
                list_of_songs[(artist, title)] = (danceability, valence)
            else:
                artist = row[3]
                title = row[14]
                danceability = float(row[4])
                valence = float(row[0])
                list_of_songs[(artist, title)] = (danceability, valence)

        return list_of_songs


def get_similar_songs(dataset_songs: dict[tuple[str, str]: tuple[float, float]],
                user_songs: dict[tuple[str, str]: tuple[float, float]]) -> dict[tuple[str, str]: list[tuple[str, str]]]:
    """Return a list of the songs from the dataset that have a danceability and valence within a range of 0.2
        Preconditions:
            - all([0.0 <= dataset_songs[d][0] <= 1.0 for d in dataset_songs])
            - all([0.0 <= dataset_songs[d][1] <= 1.0 for d in dataset_songs])
            - all([0.0 <= user_songs[u][0] <= 1.0 for u in user_songs])
            - all([0.0 <= user_songs[u][1] <= 1.0 for u in user_songs])

        >>> https://open.spotify.com/playlist/10RDYOInFIIVTUC98kA8qW?si=8d4e3b1907ad4dc6
        >>> user_songs = random_choices()
        >>> dataset_songs = csv_reader()
        >>> get_similar_songs(dataset_songs, user_songs)
    """
    similar_songs = {}

    for input_song in user_songs:
        target_danceability = user_songs[input_song][0]
        target_valence = user_songs[input_song][1]

        songes = []
        for set_song in dataset_songs:
            danceability = dataset_songs[set_song][0]
            valence = dataset_songs[set_song][1]

            if (target_danceability - 0.2) <= danceability <= (target_danceability + 0.2) and \
                    (target_valence - 0.2) <= valence <= (target_valence + 0.2):
                songes.append(set_song)
        similar_songs[input_song] = songes
    return similar_songs
