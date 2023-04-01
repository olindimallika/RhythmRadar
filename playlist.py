"""
CSC111 Winter 2023 Final Project
RhythmnRadar: Underground Song Recommendation System
This module contains a collection of Python classes and functions for our song recommendation system.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the CSC111 course department
at the University of Toronto St. George campus. All forms of distribution of this code,
whether as given or with any changes, are strictly prohibited. For more information on
copyright for CSC111 project materials, please consult our Course Syllabus.

This file is Copyright (c) 2023 of Mahek Cheema, Kelsang Tsomo, Olindi Mallika Appuhamilage, and Bea Alyssandra Castro
"""
from __future__ import annotations

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
from typing import Any
from typing import Optional
import csv

# from python_ta.contracts import check_contracts

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

###############################################################################
# Song and Network  Classes
###############################################################################
SongID: str


# @check_contracts
class Song:
    """A class that represents a song from the user's playlist or from the spotify database.

    Instance Attributes:
    - song_id:
        The unique identifier of this song.
    - name:
        The name of the song.
    - artist:
        The name of the person who created the song.
    - valence:
        Numerical scale from 0.0 to 1.0 defining the musical positivity that a recording conveys. Tracks with a high
        valence sound happier, cheerier, and more uplifting, whereas tracks with a low valence sound
        more depressing. (e.g. sad, depressed, angry).
    - danceability:
        Based on a combination of musical elements, including tempo, rhythm stability, beat strength,
        and overall regularity, danceability quantifies how appropriate the song is for dancing. The least danceable
        number is 0.0, and the most danceable value is 1.0.
    - energy:
        A perceptual gauge of intensity and action, energy ranges from 0.0 to 1.0. In general, energetic music
        feels quick, energetic, and noisy. For instance, a Bach prelude rates poorly on the energy metre compared
        to death metal. This characteristic is influenced by perceptual elements like dynamic range, perceived
        loudness, timbre, onset rate, and general entropy.
    - loudness:
        A track's overall volume in dB (dB). In order to compare the relative loudness of tracks, loudness
        values are averaged over the full clip. Typical values lie between -60 and 0 db.
    - popularity:
        A track's popularity is measured on a scale of 0 to 100, with 100 representing the most recognition.
        The popularity is determined by an algorithm and primarily depends on how recently and how many times
        the music has been played overall.
    - similar_songs:
        Songs similar to this song, represented by a list. If no similar songs have been computed yet, this will
        be represented by an empty list.
    - genre:
        The category (genre) of the song, which is characterized by similarities in composition. A song can have
        multiple genres, and is represented as a list of strings. If not yet classified, the genre is none.
    """
    song_id: SongID
    name: str
    artist: str
    valence: float
    danceability: float
    energy: float
    loudness: float
    popularity: int
    similar_songs: list[Song]
    genres: list[str]

    def __init__(self, song_id: SongID, name: str, artist: str, valence: float, danceability: float, energy: float,
                 loudness: float, popularity: int, genres: list[str]) -> None:
        """Initialize a new song given song_id, name, artist, valence, acousticness, danceability, energy,
        instrumentalness, loudness, popularity, speechiness, tempo and genre."""
        self.song_id = song_id
        self.name = name
        self.artist = artist
        self.valence = valence
        self.danceability = danceability
        self.energy = energy
        self.loudness = loudness
        self.popularity = popularity
        self.similar_songs = []
        self.genres = genres

    def __repr__(self):
        """Return a string representation of this song

        This is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.
        >>> song = Song('ABC123', 'CSC111', 'Uoft', 1.0, 0.0, 1.0, 0.0, 100)
        """
        return f"Song(song_id='{self.song_id}', name='{self.name}', artist='{self.artist}', valence={self.valence}, " \
               f"danceability={self.danceability}, energy={self.energy}, " \
               f"loudness={self.loudness}, popularity={self.popularity}, " \
               f"similar_songs={self.similar_songs}, " \
               f"genre={self.genres})"

    def get_user_features(self, song: Any, song_names: list[str], user_songs: dict[tuple[str]: tuple[float]],
                          genres: list[Any]) -> dict[tuple[str]: tuple[float]]:
        """Extract the features from a song in the user's playlist."""
        self.name = song["track"]["name"]
        song_names.append(self.name)
        track_uri = song["track"]["uri"]

        artist_uri = song["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        self.popularity = artist_info["popularity"]
        self.artist = song["track"]["artists"][0]["name"]
        self.genres = artist_info["genres"]
        genres.append((self.artist, self.popularity, self.genres))

        # add to the dictionary
        self.danceability = (sp.audio_features(track_uri)[0]['danceability'])
        self.valence = (sp.audio_features(track_uri)[0]['valence'])
        self.loudness = (sp.audio_features(track_uri)[0]['loudness'])
        self.energy = (sp.audio_features(track_uri)[0]['energy'])
        user_songs[(self.artist, self.name)] = \
            (self.danceability, self.valence, self.loudness, self.energy)


# @check_contracts
class Playlist:
    """A class that represents ten songs from the users playlist connected to each other.

    Private Instance Attributes:
    - _songs: A mapping from SongID to Song in this playlist

    Representation Invariants:
    - all(id == self._song[id].song_id for id in self._songs)
    """
    _songs: dict[SongID, Song]

    def __init__(self) -> None:
        """Initialize an empty Playlist"""
        self._songs = {}

    def csv_reader(self) -> dict[tuple[str, str]: tuple[float, float]]:
        """..."""
        list_of_songs = {}
        with open('new.csv') as csv_file:
            reader = csv.reader(csv_file)

            next(reader)
            for row in reader:
                lst = []
                value = len(row)
                if value > 19:
                    for i in range(3, (value - (19 - 4))):
                        lst.extend(list(map(str.strip, row[i].split(','))))
                    artist = lst[0]
                    title = row[(value - 19) + 14]
                    danceability = float(row[(value - (19 - 4))])
                    valence = float(row[0])
                    loudness = float((value - 19) + 12)
                    energy = float((value - 19) + 6)
                    list_of_songs[(artist, title)] = (danceability, valence, loudness, energy)

                    popularity = int((value - 19) + 15)
                    song = Song('', title, artist, valence, danceability, energy, loudness, popularity)

                    self._songs[SongID] = song

                else:
                    artist = row[3]
                    title = row[14]
                    danceability = float(row[4])
                    valence = float(row[0])
                    loudness = float(row[12])
                    energy = float(row[6])
                    list_of_songs[(artist, title)] = (danceability, valence, loudness, energy)


                    popularity = int(row[15])
                    song = Song('', title, artist, valence, danceability, energy, loudness, popularity)

                    self._songs[SongID] = song

            return list_of_songs

    def random_choices(self) -> dict[SongID, Song]:
        """Return a list of 10 random song names from the user's input playlist."""

        # take a sample of 10 random songs
        random_songs = random.sample(sp.playlist_tracks(playlist_URI)["items"], 10)

        # a list for the names of each random song
        song_names = []

        # a dictionary mapping a tuple of the song artist and song title to
        user_songs = {}

        # access the features of each song
        for s in random_songs:

            # access the features of each song
            song_title = s['track']['name']
            song_names.append(song_title)
            track_uri = s['track']['uri']
            song_id = s['track']['id']

            artist_uri = s['track']['artists'][0]['uri']
            artist_info = sp.artist(artist_uri)
            popularity_score = artist_info['popularity']
            artist = s['track']['artists'][0]['name']
            artist_genres = artist_info['genres']

            # add to the dictionary
            user_danceability = (sp.audio_features(track_uri)[0]['danceability'])
            user_valence = (sp.audio_features(track_uri)[0]['valence'])
            user_energy = (sp.audio_features(track_uri)[0]['energy'])
            user_loudness = (sp.audio_features(track_uri)[0]['loudness'])

            song = Song(song_id, song_title, artist, user_valence, user_danceability, user_energy, user_loudness,
                        popularity_score, [], artist_genres)

            self._songs[SongID] = song

        return self._songs


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
