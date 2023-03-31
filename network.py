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
from typing import Optional, Any

# from python_ta.contracts import check_contracts


###############################################################################
# Song and Playlist Classes
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
    - genre:
        The category (genre) of the song, which is characterized by similarities in composition. A song can have
        multiple genres, and is represented as a list of strings. If not yet classified, the genre is none.
    """
    song_id: str
    name: str
    artist: str
    valence: float
    danceability: float
    energy: float
    loudness: float
    popularity: int
    genre: Optional[list]
    similar_songs: list[Song]

    def __init__(self, song_id: str, name: str, artist: str, valence: float, acousticness: float, danceability: float,
                 energy: float, loudness: float, popularity: int, genre: Optional[list] = None) -> None:
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
        self.genre = genre

    def __repr__(self):
        """Return a string representation of this song


        This is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.
        >>> song = Song('ABC123', 'CSC111', 'Uoft', 1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        """
        return f" Song(song_id='{self.song_id}', name='{self.name}', artist='{self.artist}', valence={self.valence}, " \
               f" danceability={self.danceability}, energy={self.energy}," \
               f" loudness={self.loudness}, popularity={self.popularity}, " \
               f" genre={self.genre})"
