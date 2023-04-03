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

import sys

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
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
    - genres:
        The category (genres) of the song, which is characterized by similarities in composition. A song can have
        multiple genres, and is represented as a list of strings. If not yet classified, the genre is none.
    - recommended_songs:
        Songs similar to this song, represented by a list. If no similar songs have been computed yet, this will
        be represented by an empty list.
    - channels:
        A dictionary mapping the SongID to the channel that links a song from the user's playlist to
        its recommended songs.
    """
    song_id: SongID
    name: str
    artist: str
    valence: float
    danceability: float
    energy: float
    loudness: float
    popularity: int
    genres: list[str]
    recommended_songs: list[Song]
    channels: dict[SongID, Channel]

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
        self.genres = genres
        self.recommended_songs = []
        self.channels = {}

    def __repr__(self):
        """Return a string representation of this song

        This is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.
        >>> song = Song('ABC123', 'CSC111', 'Uoft', 1.0, 0.0, 1.0, 0.0, 100)
        """
        return f"Song(song_id='{self.song_id}', name='{self.name}', artist='{self.artist}', valence={self.valence}, " \
               f"danceability={self.danceability}, energy={self.energy}, " \
               f"loudness={self.loudness}, popularity={self.popularity}, " \
               f"genre={self.genres}"


# @check_contracts
class Channel:
    """A link (or "edge") connecting two songs in an interconnection network.

    Instance Attributes:
    - endpoints: The two songs linked by this channel.

    Representation Invariants:
        - len(self.endpoints) == 2
    """
    endpoints: set[Song]

    def __init__(self, song1: Song, song2: Song) -> None:
        """Initialize an empty channel with the two given songs.

        Also add this channel to song1 and song2.

        Preconditions:
            - song1 != song2
            - song1 and song2 are not already connected by a channel
        """
        self.endpoints = {song1, song2}
        song1.channels[song2.song_id] = self
        song2.channels[song1.song_id] = self

    def get_other_endpoint(self, curr_song: Song) -> Song:
        """Return the endpoint of this channel that is not equal to the given node.

        Preconditions:
            - song in self.endpoints
        """
        return (self.endpoints - {curr_song}).pop()

    def __repr__(self) -> str:
        """Return a string representing this channel.

        __repr__ is a special method that's called when the object is evaluated in the Python console.

        >>> channel = Channel(Song(0), Song(1))
        >>> repr(channel) in {'Channel(Song(0), Song(1))', 'Channel(Song(1), Song(0))'}
        True
        """
        endpoints = list(self.endpoints)
        return f'Channel({endpoints[0]}, {endpoints[1]})'


# @check_contracts
class Playlist:
    """A class that represents ten random songs from the users playlist that are each connected to their similar songs.

    Private Instance Attributes:
    - _songs: A mapping from SongID to Song in this playlist

    Representation Invariants:
    - all(id == self._song[id].song_id for id in self._songs)
    """
    _songs: dict[SongID, Song]

    def __init__(self) -> None:
        """Initialize an empty Playlist"""
        self._songs = {}

    def add_song(self, song_id: SongID, name: str, artist: str, valence: float, danceability: float, energy: float,
                 loudness: float, popularity: int, genres: list[str]) -> Song:
        """Add a new song with the given address to this network and return it.

        The new song is not adjacent to any other songs. (This violates our assumption that
        interconnection networks are connected; but, we'll assume that whenever a new song
        is added, edges will also be added for that song.)

        Preconditions:
            - address not in self._songs
        """
        new_song = Song(song_id, name, artist, valence, danceability, loudness, energy, popularity, genres)
        self._songs[song_id] = new_song
        return new_song

    def add_channel(self, id1: SongID, id2: SongID) -> None:
        """Add a new channel between the nodes with the two given addresses.

        If a given address doesn't correspond to a node in this network, first create a new
        node for that address.

        Preconditions:
        - id1 != id2
        - id1 in self._songs and id2 in self._songs
        """
        Channel(self._songs[id1], self._songs[id2])

    def playlist_to_dict(self) -> dict[SongID, set[SongID]]:
        """Return a dictionary mapping the song id of each song from the user's playlist to a set of song ids
            from the dataset that are similar.~

        >>> https://open.spotify.com/playlist/10RDYOInFIIVTUC98kA8qW?si=8d4e3b1907ad4dc6
        >>> p = Playlist()
        >>> p.get_songs_in_range()
        >>> p.playlist_to_dict()
        {'0hiOO6QBWALL7e5IzlIC5Z': {'7FihoA0WgTT21DkWR7wbYR', '5Yb82JrDj09gQHQtjWgYYo'}, '76GlO5H5RT6g7y0gev86Nk': {'4L9l5x0WuzNtyEBeqzvgPE', '2LQb3iYBzoxbxct2IexjBc', '1jgUFLCsFEtcDy47RzCwWe', '4m8QO7mDC4kqWTKSLqsZS8', '2nMOodYNHBAQ3Kc1QNimZU'}, '296nXCOv97WJNRWzIBQnoj': {'5cEbtwig1FXW8RF6FSxRU1', '3J4A8aojSB2mBTuzczisHA', '6B4KWBeFdHrpVezjTqggWr', '4QnC1bIaMSfDQvF4XDhV5M', '1SlM5HXf9DjC6PVy2x4nWQ', '2KuvxztaTuhjIdQrXMrmoN', '26t0xoYPRxyHvIN62P85au', '7vo78dgK2nJ5TdtYEYV4yo', '1vBeIXlzbAieGoDqInav5j', '7COq4g77Lk81xC5vZwfnIs', '7w77k7yCaDOMe25fYxnzit', '3hbZsQXQNbPMBmgI7O0CTv', '0bQfYvx2zDkHYLoSd8Si7t', '7GwYENSg87oERcW0Wacd6m', '0TYhf0MgEj4YJaKwo5c4Km', '2Cv7cXyq024BX30zo8sm2v'}, '6OiRh4kttAs1YWglvTcYkB': {'5Y7a8iWIawp1QTbevGeH1V', '4grrgOFDvIVvw807GmqT1X', '1rEkUEBFYEtqDLYaTuElsx', '7EEaV81pUNKvqsTrEHGoQH', '4ePKbzLwkIBslceokt2iXZ', '5NAiPIEzxAexFE3ucV18Q8', '4m1lB7qJ78VPYsQy7RoBcU', '7E6knQgEAcU0nIjQJuwrIv', '0tsUIJakq2RksuC1YixAHX', '4cJMTTVlG4zefUr4mNITuQ', '2hVKFfp7Rmr2XPK31jFCrX', '3fKXS93P7YOS4xEUnWzkUz', '4byXh93siQtzKLdjKuJaAF', '72geHhNU5UA2hU1QgUzXdE', '3R8PKPTPgHApBhCt3NUJ0q', '3hYBu3LRhapDItoL2R5aK2', '3gRwYAsiX4e50J43BkmZxI', '7ElHqs46U65NOaSwha2eMv', '5xkTOC5NHPfUmrBCIrSTJX', '1BRzYmGZ3UTPSc3qsZASQL', '6eMeqiSoQYtM8u3vvfth21', '5U4zBRfVdqaL1kOULNtZ1T'}, '4sNwdacKyi2S26WrRtNama': {'1vHeu2j2MpfMqqvcXKLtic', '1trFxVLL8WKhYap543e74l', '5pdfnefsLnfBFo7gxHvqBK', '0wsZ8UUvvYWm9xMPDUWJp1', '0ZxFFIJg3TzEoVcuj08rA2', '7uL1ZsdxI8l4sgEsgCmTlG', '3YVj9LLq5GMvBvoKubnUp0', '701DK0It9f7iurRnzKvF0y', '3TgelNfEK1DnYrsHOBxaVJ', '0AAAns3nqYVd9zKCipsSR2'}, '4c0tJe2ENJwrZbn9Bap2qs': {'7nzmXUrZwSOJPNmV0mOmEn', '4v8GJxLdvUiN7R31cKcmNL', '73u7dTjaBTMyvs3KWOThGR', '7yMYqHqzye8vtyiHqdVlZw', '6kiIVIbmwEw6JvIZc7UG0E', '4nyF5lmSziBAt7ESAUjpbx', '3w6f34fBUXOvuko0Ihq7he', '2bUXfclD8DwJwwUENtSCWu', '4th5Ot5mSRXWgV9gyf2rpn', '23wrmyJ1S2sjeh2dFN5P9k', '0PUkanqCGTb6qseXPKOw1F', '5Tb6K5YFvUNXREaGbDLn1m', '4drTFbY9KJIvllrqVcJvLi', '2deFH5zveEBEUuURpqTN3C', '2g6WTGWNYGnRCBaWEzFE00', '6hRrzZJ90DNQdEF1Wu2Mrf', '6ctlpLPyLH3R1V16fxoOWE', '61nXG1EGqF8a9OgRlCLSB4', '6nl9BAvm7wMV2mEEChRzA9', '6Iw6fQVKZi0fWtEQBrTFcP', '66H06L8hktjhduwRDWntDT', '63LJjsJuqZgQyYibMXn9ku', '48WTGGIeSFD5ZMF51Rm4Y9', '1XjdBT4P0TfLf5hYxGqjs9', '2yg9UN4eo5eMVJ7OB4RWj3', '3Mf5CJ4c9wzdCI5Dib3V3B', '0hoRmVUp5cZ1empu0nSHU8', '4zcVQvCRJRafP6JtLGyy7R', '7oTE1KmtU2ml9zBhv9Reao'}, '7DcJ6fEBb7BaKuYKTwiDxK': {'3ODTE9DkjQHCGEqL1lOIOC', '1QRJb5VY3sIkCKcTuIKCrk', '4NkIYlfobkqS2hALHTIUV9', '0vy1K9FhCK8woHW7MKEcBG', '45ROR8UMn60YEVQnDy0uVF', '043T1ZzD0qHoesyfZhseGn', '308prODCCD0O660tIktbUi', '4c60yLpE5lXvICT0pyEaZ5', '6HUO25AttZZCoKAY0vUVtc', '5GMQdzgtI7vtpmtps2YiYx', '4cJMTTVlG4zefUr4mNITuQ', '4Svpc4QRvDW0J34AE30S9c', '4NeHCGpTPVCudqVpJiT7O9', '01ZqsXtHhRtO2Z2JrvkG1w', '5Po5YmT4RhawSeqNXx5m0o', '0c5qAIcNy3jNIxmZXllp4V', '2APxijdVoN8AIrS1AuCMAT', '63LJjsJuqZgQyYibMXn9ku', '1MOaO6K6N4U55utUuudcwm', '1MIpU2U1kUInGTpaCYuVKs', '6y4pOReFqH2wzo4CV91cZC', '1nedyHXLtbomGOaa7BOwYl', '6eMeqiSoQYtM8u3vvfth21'}, '5BK0uqwY9DNfZ630STAEaq': {'01ZqsXtHhRtO2Z2JrvkG1w', '1QRJb5VY3sIkCKcTuIKCrk', '2bUXfclD8DwJwwUENtSCWu', '7LdMXgWzLthvxJOngkynaB', '7Hy7Fgp3es9APBsQIzEF3V', '63LJjsJuqZgQyYibMXn9ku', '48WTGGIeSFD5ZMF51Rm4Y9', '1MIpU2U1kUInGTpaCYuVKs', '5GMQdzgtI7vtpmtps2YiYx', '46Nz7uguhTyUWOXhRBbzxa', '2GSLoT7abyYGchSSDCpWEI', '4NeHCGpTPVCudqVpJiT7O9'}, '4HffeEF97c6UxNePgbuECW': {'7ibRB2S2WOfPKSvYkhcYtj', '1kwnxJNVl7cwcU98RvMBaR', '55GLc4nywcX4aIlOcx1u06', '7w0lCrXGoUj5b8DgW5wZlx', '0Vr6vFlxGoAMs6RPA5vJZY'}, '3SXXFIZel1VQQ4ENiqozxi': {'0l3jBCAEdeLR9OgQqES9CI', '0Kq6RzOqkHxnfiA9OGqReU', '0TUK4LKkHVHdsLwscQckX6', '1Y3TlYJNhIa7k4YAvFkJAB', '1zQjzfgYp0ZDSsU1dxi5g8', '5SLDICTLPlgaebtGUZtr7J', '6JgXQTdqLL1xS5qfqOGVNb', '5qNNanYonpCwahfJGuFVRQ', '5LPlvbxA6bJQHvUW12Mr22', '49oBFP6ZHPtd6t33LFTD3E', '15vyZX2dCWO1alNLe8YjZs', '2JfV8E7wsD7eVY5wr69teC', '7paFC3FEu1WtPVP4Do6VZN', '5V5BHmvpylV0nSc2Yu2Mu4', '26gSBcw01jGFdkbWY5Plei', '1uhPCuhxeC9wEYl7smMByK', '1x7KRBVwvqgA0vYU6UeXHP'}, '0AAAns3nqYVd9zKCipsSR2': {'4sNwdacKyi2S26WrRtNama'}, '2O1qYJTA2BI5ypFFqEZhh4': set(), '01ZqsXtHhRtO2Z2JrvkG1w': {'5BK0uqwY9DNfZ630STAEaq', '7DcJ6fEBb7BaKuYKTwiDxK'}, '1xfFPJdRjgDAaMcDgbXwyh': set(), '5opxZwZYGrLuWTOLW8HvMK': set(), '1iJdIZU5Ffgixa92wrcZZC': set(), '03w1u0L5fS0F7izSUkdqS2': set(), '78EDmwVdZzp6vTl3hVWzpW': set(), '260V7huyJrXnyYe0dFv2Fa': set(), '2bUXfclD8DwJwwUENtSCWu': {'5BK0uqwY9DNfZ630STAEaq', '4c0tJe2ENJwrZbn9Bap2qs'}, '1SJkTuUNKe4rYQgX8wmqku': set(), '5NAiPIEzxAexFE3ucV18Q8': {'6OiRh4kttAs1YWglvTcYkB'}, 9: set(), '4UYLGTJRGCt4KzP9r9Y9bH': set(), '5qNNanYonpCwahfJGuFVRQ': {'3SXXFIZel1VQQ4ENiqozxi'}, '66H06L8hktjhduwRDWntDT': {'4c0tJe2ENJwrZbn9Bap2qs'}, '7LdMXgWzLthvxJOngkynaB': {'5BK0uqwY9DNfZ630STAEaq'}, '64DmB3o38q6oMZUz35vLcp': set(), 10: set(), '07egAPsYgrxjkEnZxs1ePJ': set(), '3YVj9LLq5GMvBvoKubnUp0': {'4sNwdacKyi2S26WrRtNama'}, '4CUChWZSJxtBpACA0j55Bk': set(), '6nl9BAvm7wMV2mEEChRzA9': {'4c0tJe2ENJwrZbn9Bap2qs'}, '2fGxYYMQbVqgIdaqfz2OwA': set(), '1rEkUEBFYEtqDLYaTuElsx': {'6OiRh4kttAs1YWglvTcYkB'}, '1QLyDdhB9gmxbGv0K1kFyT': set(), '0FD8KMG4pHp0O9clTpChjp': set(), '6CRRlfXDdhsL6vih3J5xco': set(), '1MIpU2U1kUInGTpaCYuVKs': {'5BK0uqwY9DNfZ630STAEaq', '7DcJ6fEBb7BaKuYKTwiDxK'}, '4M0WfSYF2z5FCRgQDOck9O': set(), '4c60yLpE5lXvICT0pyEaZ5': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '2XWEKRbJ8lSvmDI3qfIsXc': set(), '4XrvRf68c9H4orZZ9KoldQ': set(), '2Cv7cXyq024BX30zo8sm2v': {'296nXCOv97WJNRWzIBQnoj'}, '55GLc4nywcX4aIlOcx1u06': {'4HffeEF97c6UxNePgbuECW'}, '4grrgOFDvIVvw807GmqT1X': {'6OiRh4kttAs1YWglvTcYkB'}, '4v8GJxLdvUiN7R31cKcmNL': {'4c0tJe2ENJwrZbn9Bap2qs'}, '701DK0It9f7iurRnzKvF0y': {'4sNwdacKyi2S26WrRtNama'}, '1rXojdsUqqxGj2WCmJGWHP': set(), '2RGe02P8xxSF9syj0ltPjX': set(), '4svkPL62HbvyFgf0nHFXAF': set(), '1BRzYmGZ3UTPSc3qsZASQL': {'6OiRh4kttAs1YWglvTcYkB'}, '77dwRzKegOkVtlHajKnDCb': set(), '13TfD0g69nL4M7OtfI59oW': set(), '06EMBzxDm2hueehobAlMtm': set(), '7Hy7Fgp3es9APBsQIzEF3V': {'5BK0uqwY9DNfZ630STAEaq'}, '0bQfYvx2zDkHYLoSd8Si7t': {'296nXCOv97WJNRWzIBQnoj'}, '4J7SCXbz18duODAQYjtzI2': set(), '2pDPOMX0kWA7kcPBcDCQBu': set(), '1060gzllf4b0UETAXisR5l': set(), '5EIIvtMRH9qyf5wIyEfT8l': set(), '63LJjsJuqZgQyYibMXn9ku': {'5BK0uqwY9DNfZ630STAEaq', '4c0tJe2ENJwrZbn9Bap2qs', '7DcJ6fEBb7BaKuYKTwiDxK'}, 11: set(), '2PXTRyViXMQnezQOs6vDHa': set(), '0obIo2GEab6qqms6t3JaMY': set(), '09kaIU1AZoo2MRk46s6AEi': set(), '4FC7GMnGwYeAjuvC83Srbs': set(), '2qwn6whaZf7gax7SaqUZSC': set(), '4m8QO7mDC4kqWTKSLqsZS8': {'76GlO5H5RT6g7y0gev86Nk'}, '1xUQwXDDKW79z7GRUt2vMW': set(), '46Nz7uguhTyUWOXhRBbzxa': {'5BK0uqwY9DNfZ630STAEaq'}, '4YBDSEzVNQbvCvVIWNtruF': set(), '7enVhl0fuHvQ4ErXvAXYIH': set(), '0dcsuO7AQ06VS9uWfA6m1C': set(), '2sDfnEOD1MlaOW2yTYSHZQ': set(), '2eVKwKivluiYn67kLtZ3d7': set(), '1SXIQAhAPRo0tENxO3HQTi': set(), '3b8REPBdYQfaZvblfMuwc5': set(), '0PYmO55JPwEWgtyJbkN6mq': set(), '4NkIYlfobkqS2hALHTIUV9': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '7BjygzvUpf8P7X6uWzIhsF': set(), '3bjLA6ukBcGtvhe5tybxp7': set(), '1uwLMwgqPprCs5Q0OPRKI7': set(), 13: set(), '5nMBzG9xVnJZTpZKgnWCec': set(), '6JgXQTdqLL1xS5qfqOGVNb': {'3SXXFIZel1VQQ4ENiqozxi'}, '6DCxsitO66sRaPLAZJMFkT': set(), '0ByKkm4qqcDPtC2cPWo1wE': set(), '4xb8JHIN56xixSl6vkSPjm': set(), '71DxoKxpHcW8iaYNczwGi3': set(), '0erWz20ZejKi8WRNoeNQjJ': set(), '1trFxVLL8WKhYap543e74l': {'4sNwdacKyi2S26WrRtNama'}, '1hI9ZhG2wlCbQKJnw3krPU': set(), '4eUsMWZO1Dpc0lQp4JsKXa': set(), '6I90hMc9paVMjNPxMOXoot': set(), '7APmLuBrYJfp7pnXCYXR4v': set(), '0YBNpbrmpZdFRT0NFqii5C': set(), '7ArrTJ1LwcGAlEO65LUQ7i': set(), '6Tvzf3VEi16JMhAgOwdt2y': set(), '4th5Ot5mSRXWgV9gyf2rpn': {'4c0tJe2ENJwrZbn9Bap2qs'}, '4NeHCGpTPVCudqVpJiT7O9': {'5BK0uqwY9DNfZ630STAEaq', '7DcJ6fEBb7BaKuYKTwiDxK'}, '7uL1ZsdxI8l4sgEsgCmTlG': {'4sNwdacKyi2S26WrRtNama'}, '5atcLAbdW7d6BOui2DDI9z': set(), '1SlM5HXf9DjC6PVy2x4nWQ': {'296nXCOv97WJNRWzIBQnoj'}, '3fMKnwiByu9yfeD5ISn9Et': set(), '4UADR6fNQfx4fxkiRQvSy2': set(), '6Gg25EZRbQd4IHiJz2KSY0': set(), '38zwkK6TtTjIW9tpYBfZ3D': set(), '5tY0sWgi6v0UEibwYjfWlL': set(), '7IKh3MlTFsgFOaqKc0z7If': set(), '5h66wqaGklsSa8eSxTwcJT': set(), '6rDaCGqcQB1urhpCrrD599': set(), '2cJC39Aqmyo6YBS7WuevRh': set(), '5uvucCRBTkxv7VxIDLOqe7': set(), '3LRbalLzZcuvSR6jVnqclh': set(), '3TgelNfEK1DnYrsHOBxaVJ': {'4sNwdacKyi2S26WrRtNama'}, '7IL3UOlcJ6nmcCMwpnlfcA': set(), '0syXbGoFZbTMXm8hGCEvW0': set(), '0TUK4LKkHVHdsLwscQckX6': {'3SXXFIZel1VQQ4ENiqozxi'}, '2Yp9qysxGcSZocXOiv3hYs': set(), '5N6USyYyAuSyysUQ1xncYc': set(), '1aa3A3F6b5FZFtXAhtrybK': set(), '5Y7a8iWIawp1QTbevGeH1V': {'6OiRh4kttAs1YWglvTcYkB'}, '3BPoSr2pO34Aan6alFfVto': set(), '14KP6cmTImZmrcAC5m0Azd': set(), '4m1lB7qJ78VPYsQy7RoBcU': {'6OiRh4kttAs1YWglvTcYkB'}, '6L1rxT6NUotot2AAiLXGLj': set(), '1vBeIXlzbAieGoDqInav5j': {'296nXCOv97WJNRWzIBQnoj'}, '6m3LlhdZ0HWn4D7Nnm06MQ': set(), '0TYhf0MgEj4YJaKwo5c4Km': {'296nXCOv97WJNRWzIBQnoj'}, '7E6knQgEAcU0nIjQJuwrIv': {'6OiRh4kttAs1YWglvTcYkB'}, '3pOMQhSSzx6IZ96kMef6i1': set(), '1y9jnUTgn4u8RzybqK8WFT': set(), '0TxSk5fpK01cBLV9ePqcE6': set(), '5rBQIzDduJsmDbZ97gqWEW': set(), '1q5wF1wZQD41ura41yVqXb': set(), '6TqoydI7ZJdRkwBgPYy7eb': set(), '2JaIIUKcFXkgMRL3v3mZEK': set(), '1wtrm5eTeRfEXyJNF4Low1': set(), '6y4pOReFqH2wzo4CV91cZC': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '6lJ5aSxKHCwNBoWkZT3JeJ': set(), '4ePKbzLwkIBslceokt2iXZ': {'6OiRh4kttAs1YWglvTcYkB'}, '2LQb3iYBzoxbxct2IexjBc': {'76GlO5H5RT6g7y0gev86Nk'}, '36m0b1aad6A4CXq41VYxDe': set(), '0hoRmVUp5cZ1empu0nSHU8': {'4c0tJe2ENJwrZbn9Bap2qs'}, '54IbnYEdA3ymfxv07WgN3b': set(), '0IrtQ83z9jylZaLEJK2eoy': set(), '7a1D98IVXyVBKsq40imjyg': set(), '5fCDWDX2Kv9jc1s7nZfzOi': set(), '2g6WTGWNYGnRCBaWEzFE00': {'4c0tJe2ENJwrZbn9Bap2qs'}, '2yg9UN4eo5eMVJ7OB4RWj3': {'4c0tJe2ENJwrZbn9Bap2qs'}, '05fmLn8tNYb3ijIH2jCLPb': set(), '6okflAl3X7elXPx7MgJMi6': set(), '5cEbtwig1FXW8RF6FSxRU1': {'296nXCOv97WJNRWzIBQnoj'}, '7ElHqs46U65NOaSwha2eMv': {'6OiRh4kttAs1YWglvTcYkB'}, '48WTGGIeSFD5ZMF51Rm4Y9': {'5BK0uqwY9DNfZ630STAEaq', '4c0tJe2ENJwrZbn9Bap2qs'}, '5GsDw8rD0LJ9XF4dEzUPDK': set(), '6U9OkV9oa8kN8LyBGf3wvJ': set(), '2RuOeqFMhuYLVGbgGPQx2l': set(), '4KevTcBXEIYxXVyPE78XXm': set(), '4zvqMZ6g4wKZaPpOQvoBpP': set(), '25diaIekB8iIN5oAukdFNe': set(), '7GbAp0HKPQW7WnFJAzMoRk': set(), '73u7dTjaBTMyvs3KWOThGR': {'4c0tJe2ENJwrZbn9Bap2qs'}, '3woRy7uxzl1lO2XO99oHsN': set(), '2APxijdVoN8AIrS1AuCMAT': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '5GMQdzgtI7vtpmtps2YiYx': {'5BK0uqwY9DNfZ630STAEaq', '7DcJ6fEBb7BaKuYKTwiDxK'}, '5U4zBRfVdqaL1kOULNtZ1T': {'6OiRh4kttAs1YWglvTcYkB'}, '3xngVLz4NYEshyX3aRRXgf': set(), '7vfaRUaFBDwENwa3tzJY64': set(), '5H9wMglUZwqivHCDzElAbB': set(), '11L064movtyopGdLiX4sVg': set(), '0c99BUd87HQfzgUUQqRyds': set(), '5bdPZNRLtytNqjUmSr4S0P': set(), '1e6aAbWR0MXCNcr4yQovNr': set(), '6gcNSi6b9gvDBjYO059lrF': set(), '5Yb82JrDj09gQHQtjWgYYo': {'0hiOO6QBWALL7e5IzlIC5Z'}, '2ph6BRhGcUzc2W9wIulG5k': set(), '0Z1CgKoZXoQYRiqyXhq9LV': set(), '5wxurz8J6YlyQRNnGN8zXS': set(), '4mnfRzyz2dafyBaXBLZle2': set(), '7vvfMbZeNxCrYOqxqcw3fe': set(), '3ZIc9JjtVQadMkew71IhLf': set(), '4z4OzUPgnHa4PYg9L6qqEs': set(), '6FyRXC8tJUh863JCkyWqtk': set(), '3uYDO9dPLTVrgfwg7EYXSf': set(), '7tpLBCGQi9oFrfVuaY9gjk': set(), '4fgIoBKHzO7YO5eATyYbMl': set(), '2cOE7d35PyfAh9M7DglPk0': set(), '6Ju28M6P8Y8sLjBgWjyUUD': set(), '2qpX5WY7A7uLLLQfFpvRDK': set(), '7EEaV81pUNKvqsTrEHGoQH': {'6OiRh4kttAs1YWglvTcYkB'}, '6nkJ6jerrO6S4V0kdc4KRp': set(), '0kBqgeRsRdvvFqMpiCYRNg': set(), '4LteP7qMBiV8Tol9Oug4Kc': set(), '4lhhYqzREcts4uOOqWHjRJ': set(), '5pdfnefsLnfBFo7gxHvqBK': {'4sNwdacKyi2S26WrRtNama'}, '1vHeu2j2MpfMqqvcXKLtic': {'4sNwdacKyi2S26WrRtNama'}, '1ZqeykOaDmjkldzs7XGR4b': set(), '0vy1K9FhCK8woHW7MKEcBG': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '5Aq0BYuiWi5GGSezli1Cor': set(), '1z1mMZtZW0gvR9FSPc7JpJ': set(), '78q95oBxFrzHHAWsXRogXa': set(), '4aTKyYeIzC0ask2ZJicjIJ': set(), '5Tb6K5YFvUNXREaGbDLn1m': {'4c0tJe2ENJwrZbn9Bap2qs'}, '0pohtuADv9aAqQ7KVDxa56': set(), '2nkoWsTZa8LKPNGdjI5uxj': set(), '4VVvKg5swvHf34JI7uwL2L': set(), '7FihoA0WgTT21DkWR7wbYR': {'0hiOO6QBWALL7e5IzlIC5Z'}, '7h8j5w0ywpI7AC2IQvdWqT': set(), '15vyZX2dCWO1alNLe8YjZs': {'3SXXFIZel1VQQ4ENiqozxi'}, '5SLDICTLPlgaebtGUZtr7J': {'3SXXFIZel1VQQ4ENiqozxi'}, '7JEUg9KqmpdIE5Nbb9ss66': set(), '6eMeqiSoQYtM8u3vvfth21': {'7DcJ6fEBb7BaKuYKTwiDxK', '6OiRh4kttAs1YWglvTcYkB'}, '1QRJb5VY3sIkCKcTuIKCrk': {'5BK0uqwY9DNfZ630STAEaq', '7DcJ6fEBb7BaKuYKTwiDxK'}, '3mVetrcTFdjigng5ankZRf': set(), '21AUdfi6fLFDp9JuNcHsfS': set(), '1MOaO6K6N4U55utUuudcwm': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '0Vr6vFlxGoAMs6RPA5vJZY': {'4HffeEF97c6UxNePgbuECW'}, '4FeWr4OsidcJClBjUEBHWI': set(), '33tNYw9oMtSkGe27NpgS64': set(), '37s8uwIjw72XfMseKJXNOO': set(), '3g3RCV5ImXwzHpKwM2iunc': set(), '3hYBu3LRhapDItoL2R5aK2': {'6OiRh4kttAs1YWglvTcYkB'}, '6kiIVIbmwEw6JvIZc7UG0E': {'4c0tJe2ENJwrZbn9Bap2qs'}, '54qmGkfYnt4bmpAW7354eS': set(), '0fNLObXT9pvc3VED0oAevd': set(), '2HICdPKr1U60RWy1Zm5J07': set(), '3J4A8aojSB2mBTuzczisHA': {'296nXCOv97WJNRWzIBQnoj'}, '13O36COxxWjcvc9r5Zsd1P': set(), '3aUviSdBVbsdmH406j5GZC': set(), '26t0xoYPRxyHvIN62P85au': {'296nXCOv97WJNRWzIBQnoj'}, '5ngcqrs4Xq915GUqNtNNr5': set(), '4R9KztunyNTH13KtAqePLp': set(), '1SZWIusKczJ8vloqRTAgsz': set(), '3GRAmRiwbmyTYhzzBtUTuU': set(), '4zIiarkbaDt2cm6sukb1Xt': set(), '23wrmyJ1S2sjeh2dFN5P9k': {'4c0tJe2ENJwrZbn9Bap2qs'}, '7hBRNyuEkGR4qj5nTDGTry': set(), '0NJp8GyCOWnQh71xKSPfuV': set(), '2Fw4gGClr8zVFZVwIRjyWK': set(), '6HUO25AttZZCoKAY0vUVtc': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '3amKj48hT2lYv4uzoLtBov': set(), '5xkTOC5NHPfUmrBCIrSTJX': {'6OiRh4kttAs1YWglvTcYkB'}, '5WyL4ZuwJ06qVd8X5bf2b5': set(), '7rLokcIMP9p8fl0iROdVfC': set(), '63yQS5uf762DJHLssPlrNw': set(), '5DJhKbXvR8wcX2cZKmoMg0': set(), 12: set(), '2vEIsR8I5HaEC0t64BDx1P': set(), '6ctlpLPyLH3R1V16fxoOWE': {'4c0tJe2ENJwrZbn9Bap2qs'}, '2RHVebvnbPxqx2MMlSjgrx': set(), '7KK4d7xfH6WjUuK1kPL8E2': set(), '5Po5YmT4RhawSeqNXx5m0o': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '3Yt1ovsh3v3VEzRuhI1TL5': set(), '6f096qqr3TLKBEoWxy8HPg': set(), '6rcn967QN5JtkPOBDwYIuT': set(), '1FpAKPGuR8SoIUw5t0I5vn': set(), '6E7jAJN2e3znSHyPCdQqx8': set(), '6x1jUK7H6qZVS265OCnlVw': set(), '45ROR8UMn60YEVQnDy0uVF': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '0C5X8RJXZNuGO2CfQJumb5': set(), '1M8rJIlT5HcGmvzZyssBlG': set(), '3qVNNJ7f9RQeNR4iPIeS0c': set(), '0tsUIJakq2RksuC1YixAHX': {'6OiRh4kttAs1YWglvTcYkB'}, '7COq4g77Lk81xC5vZwfnIs': {'296nXCOv97WJNRWzIBQnoj'}, '2mvn2MHPnPJeqgDrZKDnQZ': set(), '2sqE9z7rJlzV5ZgieeUatU': set(), '0wsZ8UUvvYWm9xMPDUWJp1': {'4sNwdacKyi2S26WrRtNama'}, '6L1sKb2kv74gPGUpjkybTO': set(), '49oBFP6ZHPtd6t33LFTD3E': {'3SXXFIZel1VQQ4ENiqozxi'}, '6hRrzZJ90DNQdEF1Wu2Mrf': {'4c0tJe2ENJwrZbn9Bap2qs'}, '4aGvs7y4hQIbGss7zmEXKf': set(), '2qHGPanT2ux9hwZDbmPr8t': set(), '4gOgQTv9RYYFZ1uQNnlk3q': set(), '4BOikd4oZjOYMde9AXfrTo': set(), '7nzmXUrZwSOJPNmV0mOmEn': {'4c0tJe2ENJwrZbn9Bap2qs'}, '6xRWoYwfwIKnT8bQGzKbxR': set(), '08T4lSobn8UP6PQc9qtTzT': set(), '1x7KRBVwvqgA0vYU6UeXHP': {'3SXXFIZel1VQQ4ENiqozxi'}, '7hV7333ajQNI1J6R5C9A8c': set(), '3WeYjOyamokKdl3cvQysZq': set(), '2aV5ZEAvHwvL332EsJ1gWc': set(), '4Svpc4QRvDW0J34AE30S9c': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '1UVg2llYjfc1sil4idS8NB': set(), '7w0lCrXGoUj5b8DgW5wZlx': {'4HffeEF97c6UxNePgbuECW'}, '6vZnpaBquxZQzTZqJrap1B': set(), '1jgUFLCsFEtcDy47RzCwWe': {'76GlO5H5RT6g7y0gev86Nk'}, '2ahXijXJBI2ZZoNG1zPCnl': set(), '7KVA9XflawdJaRBd1XYkJu': set(), '69IosokH54HzpJZoFIIy74': set(), '5Es5pG548uc04wSlpBKlUN': set(), '7pEGM6phhCcPXx0muMqFWW': set(), '56JyMaElW79S7TDWh1Zw1m': set(), '3r2TFFPynN97CgmzXKal5X': set(), '523XDGMjH8Gbzc8V6ek5cl': set(), '1z5YtEopKg5pyjCM3BEsr5': set(), '7JrSIPcfkWhDzxWII8Jz7V': set(), '6uopU5gxLNYdykfjAozHkW': set(), '5V5BHmvpylV0nSc2Yu2Mu4': {'3SXXFIZel1VQQ4ENiqozxi'}, '1AkO4OZeeB8pPCl2MWGhOS': set(), '2NDH7pMWv3UQHOCN4tnXbI': set(), '1RMuWWLRYeJvvPgnwaW3Tt': set(), '0ZxFFIJg3TzEoVcuj08rA2': {'4sNwdacKyi2S26WrRtNama'}, '6l26j7uCiDstBiYTuiaInV': set(), '0ClPIeT6MSgfSgQ9ZrJbAq': set(), '2deFH5zveEBEUuURpqTN3C': {'4c0tJe2ENJwrZbn9Bap2qs'}, '5uHl2eYaITSX6xEX8bmaXy': set(), '7hzlzoOwCZ4D3Ow5YZK4kj': set(), '6tsmYOwZtMfL3DdoG1itMa': set(), '3gRwYAsiX4e50J43BkmZxI': {'6OiRh4kttAs1YWglvTcYkB'}, '4UgLRXh1z9NorzrdawpIgj': set(), '7fdwZ9ShF56daUOBH02U7S': set(), '442FV16HuyEMgy7auT88hB': set(), '4gbB4ORVF9jqFWgPF8277Z': set(), '6nx6oC4HgnZOxC4dgsPiIU': set(), '2AAL4PF8WtOgHKHajUBbwh': set(), '4k9byIhs9ppbYWE22waJMB': set(), '06Pvy98db25O7wlfFFFIRM': set(), '7oTE1KmtU2ml9zBhv9Reao': {'4c0tJe2ENJwrZbn9Bap2qs'}, '6WY88gYhRrnqS4wGtO45TH': set(), '0Cks68XMF8C89s1zTfFtR2': set(), '0DU6Y7DNKhVLG1lQl0keLV': set(), '775dmuIRQojrplsns8VKen': set(), '6z8sQFj47s9ZG0Ls1k9Gct': set(), '7yMYqHqzye8vtyiHqdVlZw': {'4c0tJe2ENJwrZbn9Bap2qs'}, '4EDnXPt4LiqknZ2ClpIzXU': set(), '6ImEBuxsbuTowuHmg3Z2FO': set(), '78vv48Ic6syaE6kWqDGY47': set(), '5DSi7heBC8eTIFROBvttnp': set(), '1yOlQ6v0E3Jgo9iY0dtMyQ': set(), '2CxLla7i6lur02aOVMHPMK': set(), '4B9v2AXBpnA5tBhGTaQG0G': set(), '4iddJAOsc6U0hJ3krSJAKn': set(), '6B4KWBeFdHrpVezjTqggWr': {'296nXCOv97WJNRWzIBQnoj'}, '7LZ8mtSwAwgAopE8cCjeGw': set(), '2sFF0K2eHIClZYUqIbAwdb': set(), '36Uc6BhILjfe4VTgweoHZj': set(), '72geHhNU5UA2hU1QgUzXdE': {'6OiRh4kttAs1YWglvTcYkB'}, '3R8PKPTPgHApBhCt3NUJ0q': {'6OiRh4kttAs1YWglvTcYkB'}, '4L9l5x0WuzNtyEBeqzvgPE': {'76GlO5H5RT6g7y0gev86Nk'}, '41FLEFSeRCv19OBn0vLiaH': set(), '65cYA2DbCETUTylYI75HgP': set(), '0apsgQi5yIbTMhm1wuvnQf': set(), '1XfDYxQ8o7yZN7lbKECwHE': set(), '61GiMDN1kUiEQK6zHGMdnx': set(), '4EfcBQEzf6D3h2VrLD4tsX': set(), '4byXh93siQtzKLdjKuJaAF': {'6OiRh4kttAs1YWglvTcYkB'}, '0Jgbauc8Nv2OOjR5ERW28B': set(), '4cB00WOFuQFLoDpnydcx8c': set(), '3ni5wRSp4mB4OvHwk0SNi5': set(), '7ibRB2S2WOfPKSvYkhcYtj': {'4HffeEF97c6UxNePgbuECW'}, '05ppzZppc3WvHkYFxeKE9x': set(), '3Mf5CJ4c9wzdCI5Dib3V3B': {'4c0tJe2ENJwrZbn9Bap2qs'}, '3FigWC4Kgj0YB1tc6WMwJL': set(), '7vo78dgK2nJ5TdtYEYV4yo': {'296nXCOv97WJNRWzIBQnoj'}, '1Y3TlYJNhIa7k4YAvFkJAB': {'3SXXFIZel1VQQ4ENiqozxi'}, '26gSBcw01jGFdkbWY5Plei': {'3SXXFIZel1VQQ4ENiqozxi'}, '58qO4dGa5SgNdtvqvpewyz': set(), '6ALoVRxwV5KxaSWyejnmvi': set(), '3mQ6SLdxxaL52Yte7KF2Ks': set(), '42dtq3bqOCzD0L2kITk4Dp': set(), '0Kq6RzOqkHxnfiA9OGqReU': {'3SXXFIZel1VQQ4ENiqozxi'}, '1KDsnpM14Y6CXbJHDaRV2B': set(), '0ZHTPz5fqG9mAqqdMPCaQ6': set(), '0nEWVyeYLtIi3JUHpASGiU': set(), '7paFC3FEu1WtPVP4Do6VZN': {'3SXXFIZel1VQQ4ENiqozxi'}, '1dccdhKRYUcjPVdMGjRQ1H': set(), '7o3Mcis1uKcYDuuJD1W0Rm': set(), '1Td7TGT1XtK2ojUjz1mGUV': set(), '3GXDBeiF8ATGHJNWLinWAA': set(), '7CwPDvjGUUyPSJK8HudIlO': set(), '4QnC1bIaMSfDQvF4XDhV5M': {'296nXCOv97WJNRWzIBQnoj'}, 14: set(), '1ytCra0qH6gcHnCVQwREvu': set(), '6pOpsuCxYF1cuRkHBPDigj': set(), '6yluLIF5UowR56bZgIwd69': set(), '5LPlvbxA6bJQHvUW12Mr22': {'3SXXFIZel1VQQ4ENiqozxi'}, '3DXdjHnePKnh6oXw2ZgGSl': set(), '1F8yKtk5CQBptos4kM7aO7': set(), '0c5qAIcNy3jNIxmZXllp4V': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '3hbZsQXQNbPMBmgI7O0CTv': {'296nXCOv97WJNRWzIBQnoj'}, '5bQ9rtAfOUbPmuxjPK8zDp': set(), '4zcVQvCRJRafP6JtLGyy7R': {'4c0tJe2ENJwrZbn9Bap2qs'}, '0K6D1HbWxE8TRL8pWjNk1g': set(), '0NzH3fU6dpigJZCu1lP4lz': set(), '1gFjHoRPSRD1K9S9HhQjRd': set(), '3ODTE9DkjQHCGEqL1lOIOC': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '3tZGFwuam4LKjMRuoEC0T1': set(), '5wS1sJr2rzh9AKYFpkqqnA': set(), '6zgPxJ3HlrD8Vqv7OVLG0Y': set(), '1nedyHXLtbomGOaa7BOwYl': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '7y19aIuU0rRw4290rke252': set(), '25B5fGr9K0VdZJiRFsnMO4': set(), '1VCD7bvSOjhJYBcOzQguik': set(), '24QjawKdGJmsAIVe3EhzGH': set(), '7ueAzFpkUwrLePgFwEevFN': set(), '7xqpOUezLTYW1zMNFqnBZs': set(), '1XjdBT4P0TfLf5hYxGqjs9': {'4c0tJe2ENJwrZbn9Bap2qs'}, '3pJnfyKoVePwVmljB6Wun1': set(), '2z4cwnHBebyWzfOYRFRGXv': set(), '4cJMTTVlG4zefUr4mNITuQ': {'7DcJ6fEBb7BaKuYKTwiDxK', '6OiRh4kttAs1YWglvTcYkB'}, '1onmFJfN0YdkQ5Rrb3tLXN': set(), '2hVKFfp7Rmr2XPK31jFCrX': {'6OiRh4kttAs1YWglvTcYkB'}, '2KuvxztaTuhjIdQrXMrmoN': {'296nXCOv97WJNRWzIBQnoj'}, '41hwbZ1yF705MxJ7H9bwEu': set(), '27Y1N4Q4U3EfDU5Ubw8ws2': set(), '3StBhEiBdQICzrGiaajy2M': set(), '4sjdZEEQvR1sXrRNSuBfbA': set(), '1iIhGHzzrzqQfuNkFI2qAn': set(), '3w6f34fBUXOvuko0Ihq7he': {'4c0tJe2ENJwrZbn9Bap2qs'}, '1ZyQEn0iceHj0Lbt6I6Op3': set(), '5eEQCfq7MXQr6aHLNRUZLs': set(), '7na7Bk98usp84FaOJFPv3d': set(), '1kwnxJNVl7cwcU98RvMBaR': {'4HffeEF97c6UxNePgbuECW'}, '3ZqgCbcM2AGXivffHcun0X': set(), '2p72O2JobPc9sVz520Hil5': set(), '3uKkRicm0OvtCbynx02V8A': set(), '45xDNu9YVKIegqePEa1dSh': set(), '0y7Ao3CVJsyKFmqdjutiIF': set(), '63e35wfL6GMUp0boIvNBhw': set(), '2le8xbpMJ1aA0SpJZRMbRw': set(), '06scTb0zbkxYNgpAB3J9fN': set(), '7GwYENSg87oERcW0Wacd6m': {'296nXCOv97WJNRWzIBQnoj'}, '61nXG1EGqF8a9OgRlCLSB4': {'4c0tJe2ENJwrZbn9Bap2qs'}, '1zmv0tPVWdbCuvBw90MYwO': set(), '2Q1s11otlyEtj80OgsqDFz': set(), '3fKXS93P7YOS4xEUnWzkUz': {'6OiRh4kttAs1YWglvTcYkB'}, '4X9r5jOEmvl5Qr3ozFwTww': set(), '1sS5aMT5JWYSHwrTbxGGsn': set(), '043T1ZzD0qHoesyfZhseGn': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '1b2C65g0kgbybIAeKCxRYl': set(), '0S9ZVNTNRzLMgb96tmmG1u': set(), '1zQjzfgYp0ZDSsU1dxi5g8': {'3SXXFIZel1VQQ4ENiqozxi'}, '4drTFbY9KJIvllrqVcJvLi': {'4c0tJe2ENJwrZbn9Bap2qs'}, '4XVoOlgRCYC8yssdOBmLPF': set(), '0kKOC50fPTnqmrYvtJInsT': set(), '1nuPjx9gZH0aHZt8Q5Njx6': set(), '4nyF5lmSziBAt7ESAUjpbx': {'4c0tJe2ENJwrZbn9Bap2qs'}, '4loM16743hROPC6uIJG6wM': set(), '1uhPCuhxeC9wEYl7smMByK': {'3SXXFIZel1VQQ4ENiqozxi'}, '6hjh2phISvfR1Ib6S0FK7b': set(), '3ewS8DYitFRgZBv9X4f7qZ': set(), '3r9FFjLrAIQjoR8pSHVPC9': set(), '5jSBnH9NyaNP5zdSB3pwgu': set(), '6B2RbPOuwAKtxNAnIKY63A': set(), '0l3jBCAEdeLR9OgQqES9CI': {'3SXXFIZel1VQQ4ENiqozxi'}, '24uZaMwLQ0G8ZQfTt7f64B': set(), '3ELLCuwPrhznALIu2UAwVB': set(), '2JfV8E7wsD7eVY5wr69teC': {'3SXXFIZel1VQQ4ENiqozxi'}, '7vTspUAmMKFkUpKL9HLZNL': set(), '2nMOodYNHBAQ3Kc1QNimZU': {'76GlO5H5RT6g7y0gev86Nk'}, '1AYNmdKudx7JArl2uDy1nv': set(), '3cr3oAP4bQFNjZBV7ElKaB': set(), '6DeGFcrDiYDuyV7e7KnqPd': set(), '0dJhXJKZTpiaxTUc7uItIN': set(), '5Jm4w8jmPEBTLjI9vH4fXo': set(), '4ZAQiu61otvHVveuTsPAUr': set(), '6IsiCdn42x5fGWTUqkyDwj': set(), '3qHgGyJY4GpXNOK4WL4NSo': set(), 15: set(), '2GSLoT7abyYGchSSDCpWEI': {'5BK0uqwY9DNfZ630STAEaq'}, '6V1Jx3o0S2MtBI9yIDXsJS': set(), '5XBbvUfLSFAT5Rh8eudY8G': set(), '1FgPyHX7HruKDL4Tx4MeZB': set(), '25Mld9UGdMqXYDU2x8l3ld': set(), '7w77k7yCaDOMe25fYxnzit': {'296nXCOv97WJNRWzIBQnoj'}, '0PUkanqCGTb6qseXPKOw1F': {'4c0tJe2ENJwrZbn9Bap2qs'}, '6Iw6fQVKZi0fWtEQBrTFcP': {'4c0tJe2ENJwrZbn9Bap2qs'}, '308prODCCD0O660tIktbUi': {'7DcJ6fEBb7BaKuYKTwiDxK'}, '13MOQ6oQqkrZEDkZOHukCw': set(), '2f8y4CuG57UJEmkG3ujd0D': set(), '6RuFOroO9VO0aMGEzirLHk': set(), '0OStKKAuXlxA0fMH54Qs6E': set(), '4BZXVFYCb76Q0Klojq4piV': set(), '5SiZJoLXp3WOl3J4C8IK0d': set()}
        """
        similarities_so_far = {}

        for song_id, song in self._songs.items():
            similarities_so_far[song_id] = set(song.channels)

        return similarities_so_far

    def get_song_ids(self) -> set[SongID]:
        """Return a set containing all the song ids in the playlist or dataset.~"""
        return set(self._songs.keys())  # Note: calling dict.keys is technically unnecessary, but added for clarity

    def get_dataset_songs(self) -> list[SongID]:
        """Load all the song data from the CSV file.

        This method will return a dictionary with a tuple of strings mapped to a tuple of floats for each song.
        The tuple of strings will contain the song id, the artist name, and the title of the song respectively.
        The tuple of floats will contain the danceability, valence, energy, and loudness respectively.~
        """
        list_of_songs = []
        with open('new_small.csv') as csv_file:
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
                    popularity = int((value - 19) + 15)
                    SongID = row[((value - 19) + 8)]

                    # lst = []
                    # artist_id = []
                    # value = len(row)
                    # if value > 24:
                    #     for i in range(4, (value - (24 - 4))):
                    #         lst.extend(list(map(str.strip, row[i].split(','))))
                    #     for j in range(value - (24 - 4), (value - (24 - 6))):
                    #         artist_id.extend(list(map(str.strip, row[j].split(','))))
                    #
                    #     artist = lst[0]
                    #     title = row[1]
                    #     danceability = float(row[((value - 24) + 9)])
                    #     valence = float(row[((value - 24) + 18)])
                    #     loudness = float(row[((value - 24) + 12)])
                    #     energy = float(row[(value - 24) + 10])
                    #     SongId = row[0]
                    list_of_songs.append(SongID)

                    # finding the artists genres
                    if len(sys.argv) > 1:
                        name = ' '.join(sys.argv[1:])
                    else:
                        name = artist

                    artist_genre = []
                    results = sp.search(q='artist:' + name, type='artist')
                    items = results['artists']['items']
                    if len(items) > 0:
                        artist2 = items[0]
                        artist_genre = artist2['genres']
                    self.add_song(SongID, title, artist, valence, danceability, energy, loudness, popularity,
                                  artist_genre)

                else:
                    artist = row[3]
                    title = row[14]
                    danceability = float(row[4])
                    valence = float(row[0])
                    loudness = float(row[12])
                    energy = float(row[6])
                    popularity = int(row[15])
                    SongID = row[8]

                    list_of_songs.append(SongID)

                    artist_genre = []
                    results = sp.search(q='artist:' + artist, type='artist')
                    items = results['artists']['items']
                    if len(items) > 0:
                        artist2 = items[0]
                        artist_genre = artist2['genres']
                    self.add_song(SongID, title, artist, valence, danceability, energy, loudness, popularity,
                                  artist_genre)
        return list_of_songs

    def get_playlist_songs(self) -> list[SongID]:
        """Return a list of 30 random song ids from the user's input playlist~.

        # add a precondition ?
        """
        # a dictionary mapping a tuple of the song artist and song title to
        user_songs = []

        # take a sample of 30 random songs
        random_songs = random.sample(sp.playlist_tracks(playlist_URI)["items"], 10)

        # access the features of each song
        for s in random_songs:
            # access the features of each song
            song_title = s['track']['name']
            track_uri = s['track']['uri']
            SongID = s['track']['id']

            artist_uri = s['track']['artists'][0]['uri']
            artist_info = sp.artist(artist_uri)
            popularity_score = artist_info['popularity']
            artist = s['track']['artists'][0]['name']
            artist_genres = artist_info["genres"]

            # add to the dictionary
            user_danceability = (sp.audio_features(track_uri)[0]['danceability'])
            user_valence = (sp.audio_features(track_uri)[0]['valence'])
            user_energy = (sp.audio_features(track_uri)[0]['energy'])
            user_loudness = (sp.audio_features(track_uri)[0]['loudness'])

            self.add_song(SongID, song_title, artist, user_valence, user_danceability, user_energy, user_loudness,
                          popularity_score, artist_genres)

            user_songs.append(SongID)
        return user_songs

    def get_songs_in_range(self, user_songs: list[str], dataset_songs: list[str]) -> None:
        """Add a channel between each song from the user's playlist and its similar songs.

        'Similar songs' are found by sorting through each song from the dataset and keeping the songs that:
            - have a danceability within a range of -0.2 and 0.2
            - have a valence within a range of -0.2 and 0.2
            - have an energy within a range of -0.5 and +0.5
            - have a loudness within a range of -2 and +2 ~

        Preconditions:
            - all([0.0 <= self._songs[d].danceability <= 1.0 for d in user_songs])
            - all([0.0 <= self.songs[v].valence <= 1.0 for v in user_songs])
            - all([0.0 <= self._songs[e].energy <= 1.0 for e in user_songs])
            - all([-60.0 <= self.songs[l].loudness <= 0.0 for l in user_songs])
            - all([0.0 <= self._songs[d].danceability <= 1.0 for d in dataset_songs])
            - all([0.0 <= self.songs[v].valence <= 1.0 for v in dataset_songs])
            - all([0.0 <= self._songs[e].energy <= 1.0 for e in dataset_songs])
            - all([-60.0 <= self.songs[l].loudness <= 0.0 for l in dataset_songs])

        >>> https://open.spotify.com/playlist/10RDYOInFIIVTUC98kA8qW?si=8d4e3b1907ad4dc6
        >>> p = Playlist()
        >>> user_songs = p.get_playlist_songs()
        >>> dataset_songs = p.get_dataset_songs()
        >>> p.get_songs_in_range(user_songs, dataset_songs)
        >>> p.playlist_to_dict()
        """
        for input_song in user_songs:
            target_danceability = self._songs[input_song].danceability
            target_valence = self._songs[input_song].valence
            target_energy = self._songs[input_song].energy
            target_loudness = self._songs[input_song].loudness

            for set_song in dataset_songs:
                danceability = self._songs[set_song].danceability
                valence = self._songs[set_song].valence
                energy = self._songs[set_song].energy
                loudness = self._songs[set_song].loudness

                if (target_danceability - 0.5) <= danceability <= (target_danceability + 0.5) and \
                        (target_valence - 0.5) <= valence <= (target_valence + 0.5) and \
                        (target_energy - 0.8) <= energy <= (target_energy + 0.8) and \
                        (target_loudness - 5) <= loudness <= (target_loudness + 5):

                    while input_song == set_song:
                        song_index = user_songs.index(input_song)
                        input_song = random.choice(sp.playlist_tracks(playlist_URI)["items"])

                        while input_song in user_songs:
                            input_song = random.choice(sp.playlist_tracks(playlist_URI)["items"])

                        song_title = input_song['track']['name']
                        track_uri = input_song['track']['uri']
                        SongID = input_song['track']['id']

                        artist_uri = input_song['track']['artists'][0]['uri']
                        artist_info = sp.artist(artist_uri)
                        popularity_score = artist_info['popularity']
                        artist = input_song['track']['artists'][0]['name']
                        artist_genres = artist_info["genres"]

                        user_danceability = (sp.audio_features(track_uri)[0]['danceability'])
                        user_valence = (sp.audio_features(track_uri)[0]['valence'])
                        user_energy = (sp.audio_features(track_uri)[0]['energy'])
                        user_loudness = (sp.audio_features(track_uri)[0]['loudness'])

                        new_song = self.add_song(SongID, song_title, artist, user_valence, user_danceability,
                                                 user_energy, user_loudness, popularity_score, artist_genres)

                        user_songs[song_index] = new_song.song_id
                    self.add_channel(input_song, set_song)

    @property
    def songs(self):
        return self._songs


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, x):
        return self.queue.insert(0, x)

    def dequeue(self):
        return self.queue.pop()

    def isEmpty(self):
        return len(self.queue) == 0

    def front(self):
        return self.queue[-1]

    def rear(self):
        return self.queue[0]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
