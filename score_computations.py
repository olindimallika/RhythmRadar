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
import csv
from typing import Any, Union

# from good_reads.a3_part2_recommendations import _WeightedVertex
from playlist import Playlist as PList
from playlist import Song as s
import math
import random


class Computations(PList):
    """"..."""

    def __init__(self) -> None:
        """Initialize this playlist."""
        super().__init__()

    def computing(self, user_songs: list[str]) -> dict[str: float]:
        """
        *** user_songs and dataset_songs are lists of song ids ***

        1. to access the song object, use Playlist._songs[SongID]
        2. then get its channels by using .channels
        3. use the get_other_endpoint method to get the song that is from the dataset

        >>> c = Computations()
        >>> user_songs = c.get_playlist_songs()
        >>> dataset_songs = c.get_dataset_songs()
        >>> c.get_songs_in_range(user_songs, dataset_songs)
        >>> c.computing(user_songs)
        """
        dict_so_far = {}
        for i in user_songs:
            lst_so_far = []
            total_songs = {song_id: self._songs[i].channels[song_id] for song_id in self._songs[i].channels
            if self._songs[i].channels != {}}
            print(total_songs)
            print({s:total_songs[s] for s in total_songs})

            # for channel in self._songs[i].channels:
            #     end_point = (total_songs[i].channels[channel]).get_other_endpoint(total_songs[i])
            #     distance = self.euclidean_distance(total_songs[i].valence, end_point.valence,
            #                                        total_songs[i].danceability, end_point.danceability)
            #
            #     next_distance = self.euclidean_distance(total_songs[i].energy, end_point.energy,
            #                                             total_songs[i].loudness, end_point.loudness)
            #     lst_so_far.append(distance + next_distance)
            # print(lst_so_far)

            # get i.valence and i.danceability and i.
            # somehow get the distance between v and dance and then distance between energy and loudness
            # take the min out of all the values and then order them from smallest to largest
            # and return in that order
            # for all the songs

        return dict_so_far

    def euclidean_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Returns the float value representing the distance between the user's song and the current song
        from our spotify dataset

        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        # #d = 2√(a2 + b2)
        # distance = 0.0
        return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

    def rec(self) -> Any:
        """
        # in pygame, if user clicks thumbs up button, keep song
        # if user clicks thumbs down button, go to their list of similar_songs and reccomend the next song
        """
        user_songs = self.get_playlist_songs()
        dataset_songs = self.get_dataset_songs()

        # call the method that sorts the songs from the datasets based on how similar they are.
        # gets the list of liked and disliked songs from the user
        # have an empty potential song list
        # go through all the songs that are similar and if they weren't liked or disliked add them to potentials songs
        #

    def sort_similar_songs(self) -> Any:
        user_songs = self.get_dataset_songs()

        similar_songs = self.computing(user_songs)
        songs_so_far = []
        reccomend_song = []
        for i in similar_songs.keys():
            value = similar_songs[i].values
            num = value[1]
            songs_so_far.append(num)
            sorted_songs = sorted(songs_so_far)
            minimum = sorted_songs[0]
            chosen_song = [song[0] for song in similar_songs if song[1] == minimum]
            reccomend_song.append(chosen_song[0])

# Create a dictionary of songs and their corresponding genres
songs = {
    "Song 1": "Pop",
    "Song 2": "Rock",
    "Song 3": "Hip Hop",
    "Song 4": "Country",
    "Song 5": "Electronic"
}

# Create a dictionary of users and their corresponding liked and disliked songs
users = {
    "User 1": {
        "Liked": ["Song 1", "Song 3", "Song 5"],
        "Disliked": ["Song 2", "Song 4"]
    },
    "User 2": {
        "Liked": ["Song 2", "Song 4"],
        "Disliked": ["Song 1", "Song 3", "Song 5"]
    }
}


# Function to recommend a song to a user based on their likes and dislikes
def recommend_song(user):
    # Get the user's liked and disliked songs
    liked_songs = users[user]["Liked"]
    disliked_songs = users[user]["Disliked"]

    # Create a list of potential songs to recommend
    potential_songs = []    # the reamining songs from score_computations, ordered from lowest to highest different
    for song in songs:
        if song not in liked_songs and song not in disliked_songs:
            potential_songs.append(song)

    # If there are no potential songs, recommend a random song
    if len(potential_songs) == 0:
        return random.choice(list(songs.keys()))

    # Calculate the genre frequency of the potential songs
    genre_frequency = {}
    for song in potential_songs:
        genre = songs[song]
        if genre in genre_frequency:
            genre_frequency[genre] += 1
        else:
            genre_frequency[genre] = 1

    # Sort the potential songs by their genre frequency
    sorted_songs = sorted(potential_songs, key=lambda song: genre_frequency[songs[song]], reverse=True)

    # Return the song with the highest genre frequency
    return sorted_songs[0]


# Test the function with User 1 and User 2
print(recommend_song("User 1"))
print(recommend_song("User 2"))
