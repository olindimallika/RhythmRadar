"""
CSC111 Winter 2023 Final Project
RhythmnRadar: Underground Song Recommendation System
[Insert Module Description]

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the CSC111 course department
at the University of Toronto St. George campus. All forms of distribution of this code,
whether as given or with any changes, are strictly prohibited. For more information on
copyright for CSC111 project materials, please consult our Course Syllabus.

This file is Copyright (c) 2023 of Mahek Cheema, Kelsang Tsomo, Olindi Mallika Appuhamilage, and Bea Alyssandra Castro
"""

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


def random_choices() -> dict[tuple[str]: tuple[float]]:
    """Return a list of 10 random song names from the user's input playlist."""
    # a list for the names of each random song
    song_names = []

    # the genres
    genres = []

    # a dictionary mapping a tuple of the song artist and song title to
    user_songs = {}

    # access the features of each song
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

        # add to the dictionary
        user_danceability = (sp.audio_features(track_uri)[0]['danceability'])
        user_valence = (sp.audio_features(track_uri)[0]['valence'])
        user_songs[('Artist: ' + artist, 'Song: ' + song_title)] = \
            (user_danceability, user_valence)

    return user_songs


def csv_reader() -> dict[tuple[str]: tuple[float]]:
    """Load song data from the spotify dataset with the required attributes"""
    # a dictionary mapping a tuple of the song artist to a tuple of the danceability and valence
    list_of_songs = {}
    with open('Subset_of_song_data.csv') as csv_file:
        rr = csv.reader(csv_file)

        # skip the row with the names of the features
        next(rr)
        for row in rr:
            artist = row[3]

            title = row[14]
            danceability = float(row[4])
            valence = float(row[0])

            list_of_songs[('Artist: ' + artist, 'Song: ' + title)] = (danceability, valence)

        return list_of_songs


def get_similar_songs(dataset_songs: dict[tuple[str]: tuple[float]], user_songs: dict[tuple[str]: tuple[float]]) -> \
        dict[tuple[str]: list[tuple[str]]]:
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
    # a dictionary mapping a tuple of the artist and title of a song from the user's playlist to a list of tuples
    # containing the artist and title of a song that is similar
    similar_songs = {}

    for input_song in user_songs:
        target_danceability = user_songs[input_song][0]
        target_valence = user_songs[input_song][1]

        similar_from_dataset = []

        for set_song in dataset_songs:
            danceability = dataset_songs[set_song][0]
            valence = dataset_songs[set_song][1]

            if (target_danceability - 0.1) <= danceability <= (target_danceability + 0.1) and \
                    (target_valence - 0.1) <= valence <= (target_valence + 0.1):
                similar_from_dataset.append(set_song)

        similar_songs[input_song] = similar_from_dataset

    return similar_songs
