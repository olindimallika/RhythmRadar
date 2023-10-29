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
import math
import playlist as plist


class Computations(plist.Playlist):
    """"..."""

    def __init__(self) -> None:
        """Initialize this playlist."""
        super().__init__()

    def remove_out_of_range(self, user_songs: list[str]) -> dict[str: plist.Channel]:
        """Remove the songs that do not have any channels.

        A song without channels means there were either no songs from the dataset that were within the user's songs'
        danceability, valence, energy, and loudness or the similar song found from the dataset is the same song from
        the user's playlist.
        """
        total_songs = {}

        for i in user_songs:
            total_songs = {song_id: self._songs[i].channels[song_id] for song_id in self._songs[i].channels
                           if self._songs[i].channels != {}}
        return total_songs

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

    def similar_song_helper(self, user_id: str, distances: list[float], set_ids: list[str],
                            total_songs: dict[str: plist.Channel]) -> tuple[list[float], list[str]]:
        """Append the minimum distances to lst_so_far and then append the end_point ids to end_point_ids."""
        for song in total_songs[user_id].endpoints:
            if song.song_id != user_id:
                end_point = total_songs[user_id].get_other_endpoint(song)
                set_ids.append(end_point.song_id)
                distance = self.euclidean_distance(end_point.valence, end_point.valence,
                                                   end_point.danceability, end_point.danceability)

                next_distance = self.euclidean_distance(end_point.energy, end_point.energy,
                                                        end_point.loudness, end_point.loudness)
                distances.append(distance + next_distance)
        return distances, set_ids

    def compute_similar_song(self, total_songs: dict[str: plist.Channel]) -> dict[str: tuple[str, float]]:
        """Return the dictionary mapping the song id of a song from the user's playlist to a tuple containing
        the song id of a similar song from the dataset to the

        >>> # https://open.spotify.com/playlist/10RDYOInFIIVTUC98kA8qW?si=8d4e3b1907ad4dc6
        >>> c = Computations()
        >>> us = c.get_playlist_songs()
        >>> dataset_songs = c.get_dataset_songs()
        >>> c.get_songs_in_range(us, dataset_songs)
        >>> c.compute_similar_song(us)
        """
        dict_so_far = {}

        for s in total_songs:
            lst_so_far = []
            end_point_ids = []

            self.similar_song_helper(s, lst_so_far, end_point_ids, total_songs)

            if lst_so_far:
                for e in end_point_ids:
                    min_distance = min(lst_so_far)
                    dict_so_far[s] = (e, min_distance)
        return dict_so_far


if __name__ == '__main__':
    print('l')
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['math', 'playlist'],  # the names (strs) of imported modules
    #     'disable': ['too-many-branches'],
    #     'allowed-io': [],  # the names (strs) of functions that call
    #     'max-line-length': 120
    # })
