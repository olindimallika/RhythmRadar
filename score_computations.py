"""
CSC111 Winter 2023 Final Project
RhythmRadar: Underground Song Recommendation System
[Insert Module Description]

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the CSC111 course department
at the University of Toronto St. George campus. All forms of distribution of this code,
whether as given or with any changes, are strictly prohibited. For more information on
copyright for CSC111 project materials, please consult our Course Syllabus.

This file is Copyright (c) 2023 of Mahek Cheema, Kelsang Tsomo, Olindi Mallika Appuhamilage, and Bea Alyssandra Castro
"""
import math
import playlist as plist
import pyperclip

import random
from typing import Any, Union
import csv


# from good_reads.a3_part2_recommendations import _WeightedVertex


class Computations(plist.Playlist):
    """"..."""

    def __init__(self) -> None:
        """Initialize this playlist."""
        super().__init__()

    def remove_out_of_range(self, user_songs: list[str]) -> dict[str: list[tuple[str, plist.Channel]]]:
        """Remove the songs that do not have any channels.

        A song without channels means there were either no songs from the dataset that were within the user's songs'
        danceability, valence, energy, and loudness or the similar song found from the dataset is the same song from
        the user's playlist.
        """
        total_songs = {}

        for u in user_songs:
            channels = []
            for c in self._songs[u].channels:
                channel = self._songs[u].channels[c]
                channels.append((c, channel))
            total_songs[u] = channels
        return total_songs

    def similar_song_helper(self, user_id: str, total_songs: dict[str: list[tuple[str, plist.Channel]]]) \
            -> list[tuple[str, float]]:
        """Append the minimum distances to lst_so_far and then append the end_point ids to end_point_ids."""
        distance_lst = []

        for channel_tuple in total_songs[user_id]:
            channel_id = channel_tuple[0]
            channel = channel_tuple[1]
            user_song = self._songs[user_id]

            end_point = channel.get_other_endpoint(user_song)
            distance = self.euclidean_distance(user_song.valence, end_point.valence,
                                               user_song.danceability, end_point.danceability)

            next_distance = self.euclidean_distance(user_song.energy, end_point.energy,
                                                    user_song.loudness, end_point.loudness)
            total_distance = distance + next_distance
            distance_lst.append((channel_id, total_distance))
        return distance_lst

    def compute_similar_song(self, total_songs: dict[str: list[tuple[str, plist.Channel]]]) -> \
            dict[str: list[tuple[str, float]]]:
        """Return the dictionary mapping the song id of a song from the user's playlist to a tuple containing
        the song id of a similar song from the dataset to the

        >>> # https://open.spotify.com/playlist/10RDYOInFIIVTUC98kA8qW?si=8d4e3b1907ad4dc6
        >>> c = Computations()
        >>> us = c.get_playlist_songs()
        >>> dataset_songs = c.get_dataset_songs()
        >>> c.get_songs_in_range(us, dataset_songs)
        >>> ts = c.remove_out_of_range(us)
        >>> hi = c.compute_similar_song(ts)
        >>> import pprint
        >>> pprint.pprint(hi)
        """
        dict_so_far = {}
        for s in total_songs:
            user_song_lst = self.similar_song_helper(s, total_songs)
            dict_so_far[s] = user_song_lst
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
        return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

    def rec(self) -> Any:
        """

        """
        user_songs = self.get_playlist_songs()
        dataset_songs = self.get_dataset_songs()

        # call the method that sorts the songs from the datasets based on how simizlar they are.
        # gets the list of liked and disliked songs from the user
        # have an empty potential song list
        # go through all the songs that are similar and if they weren't liked or disliked add them to potentials songs
        #

    def sort_similar_songs(self) -> Any:
        """..."""
        recommend_song = []
        songs_so_far = []
        user_songs = self.get_playlist_songs()
        dataset_songs = self.get_dataset_songs()
        self.get_songs_in_range(user_songs, dataset_songs)
        total_songs = self.remove_out_of_range(user_songs)
        similar_songs = self.compute_similar_song(total_songs)

        lst_so_far = []
        for i in similar_songs.keys():

            for j in similar_songs[i]:
                user_genre = self._songs[i].genres
                data_genre = self._songs[j[0]].genres

                check1 = [i for i in data_genre if i in user_genre]
                if len(check1) > 0:
                    lst = [k for k in similar_songs[i] if self._songs[k[0]].genres in check1]

                    num_so_far = []
                    for num in lst:
                        num_so_far.append(num[1])

                    num_so_far = sorted(num_so_far)
                    final = [value for value in j[0] if j[1] == num_so_far[0]]
                    recommend_song.append(final[0])

                else:
                    num = j[1]
                    songs_so_far.append(num)
        sorted_songs = sorted(songs_so_far)
        # chosen_song = [song[0] for song in similar_songs.values() if song[1] == sorted_songs[]]
        recommend_song.append(sorted_songs[0])
        return recommend_song

        # lst = [k for k in similar_songs[i] if self._songs[k[0]].genres in check1]
        # num_so_far = []
        # for num in lst:
        #     num_so_far.append(num[1])
        #
        # num_so_far = sorted(num_so_far)
        # final = [value for value in j[0] if j[1] == num_so_far[0]]
        # recommend_song.append(final[0])

        # for i in total_songs.keys():
        #     self._songs[i].genres
        #     similar_songs = self.compute_similar_song(total_songs)
        #     value = [song[1] for song in similar_songs[i]]
        #     recommend_song.append(value[0])
        # return recommend_song
        # songs_so_far = []
        # reccomend_song = []
        # minimum = 0.0
        # for i in similar_songs.keys():
        #     for j in similar_songs.values():
        #         minimum = j[1]
        #         # songs_so_far.append(num)
        #     # sorted_songs = sorted(songs_so_far)
        #     # minimum = num
        #     chosen_song = [song[0] for song in similar_songs.values() if song[1] == minimum]
        #     reccomend_song.append(chosen_song[0])
        # return reccomend_song


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
    """..."""
    # Get the user's liked and disliked songs
    liked_songs = users[user]["Liked"]
    disliked_songs = users[user]["Disliked"]

    # Create a list of potential songs to recommend
    potential_songs = []  # the reamining songs from score_computations, ordered from lowest to highest different
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

# if __name__ == '__main__':
#     import python_ta
#
#     python_ta.check_all(config={
#         'extra-imports': ['math', 'playlist'],  # the names (strs) of imported modules
#         'disable': ['too-many-branches'],
#         'allowed-io': [],  # the names (strs) of functions that call
#         'max-line-length': 120
#     })
