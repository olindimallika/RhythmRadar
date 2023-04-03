"""
CSC111 Winter 2023 Final Project
RhythmnRadar: Underground Song Recommendation System
This module contains the pygame visualization code for our song recommendation system.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the CSC111 course department
at the University of Toronto St. George campus. All forms of distribution of this code,
whether as given or with any changes, are strictly prohibited. For more information on
copyright for CSC111 project materials, please consult our Course Syllabus.

This file is Copyright (c) 2023 of Mahek Cheema, Kelsang Tsomo, Olindi Mallika Appuhamilage, and Bea Alyssandra Castro
"""
import tkinter as tk
import score_computations as score


class MainMenu:
    """A class for displaying a main menu to ask for the user's input."""

    def __init__(self):
        """Initialize a MainMenu object while prompting the user for a spotify playlist."""
        # create a window, called root with a clack bg
        self.root = tk.Tk()
        self.root.configure(bg='black')

        # customize the size of the window
        self.root.geometry('700x680')

        # create a title for the window
        self.root.title('RhythmRadar')

        # add text to the window; in order: parent object,
        self.title_label = tk.Label(self.root, text='Rhythm Radar', font=('Segoe UI Semibold', 30), bg='black',
                                    fg='white')
        # change distance of text to the edge of window
        self.title_label.pack(pady=30)

        self.subtitle_label = tk.Label(self.root, text='Underground Song Recommender', font=('Segoe UI Semibold', 13),
                                       bg='black', fg='white')
        self.subtitle_label.pack()

        # Set up the instructions label
        self.instructions_label = tk.Label(self.root, text='Please input your Spotify link here:',
                                           font=('Segoe UI Semibold', 17), bg='spring green', fg='white')
        self.instructions_label.pack(pady=20)

        # store the link of the user's playlist
        self.playlist_link = tk.StringVar()

        # set up the textbox for the user to enter a link
        self.link_entry = tk.Entry(self.root, textvariable=self.playlist_link, font=('Segoe UI Semibold', 10))
        self.link_entry.pack()

        # Set up the Go button
        self.go_button = tk.Button(self.root, text="Go", width=12, font=('Segoe UI Semibold', 16),
                                   command=self.open_recommended)
        self.go_button.pack(pady=30)

        self.root.mainloop()

    def get_recommended(self):
        """Compute the recommended songs, which are the songs similar to the user's playlist songs."""
        self.recommended_song = tk.Label(self.root, font=('Segoe UI Semibold', 10), bg='white', fg='black')
        self.recommended_song.pack()
        playlist_code = self.playlist_link.get()

        return playlist_code

    def open_recommended(self):
        """Open a new window to show the user their recommended songs."""
        p = score.Computations()
        p.sort_similar_songs()
        score.recommend_song()
        RecommendationWindow()


class RecommendationWindow:
    """A class for displaying recommended songs in a new window."""

    def __init__(self):
        """Initialize a RecommendationWindow object with the given list of recommended songs."""
        # create a window, called root with a clack bg
        self.root = tk.Tk()
        self.root.configure(bg='royal blue')

        # customize the size of the window
        self.root.geometry('700x680')

        # create a title for the window
        self.root.title('RhythmRadar')

        # add text to the window; in order: parent object,
        self.title_label = tk.Label(self.root, text='Recommended Playlist', font=('Segoe UI Semibold', 30),
                                    bg='royal blue', fg='white')
        # change distance of text to the edge of window
        self.title_label.pack(pady=30)

        self.subtitle_label = tk.Label(self.root, text='Rhythm Radar', font=('Segoe UI Semibold', 13),
                                       bg='royal blue', fg='white')
        self.subtitle_label.pack()

        self.song_frame = tk.Frame(self.root)
        self.song_frame.columnconfigure(0, weight=1)
        self.song_frame.columnconfigure(1, weight=1)
        self.song_frame.columnconfigure(2, weight=1)
        self.song_frame.columnconfigure(3, weight=1)
        self.song_frame.columnconfigure(4, weight=1)
        self.song_frame.columnconfigure(5, weight=1)
        self.song_frame.columnconfigure(6, weight=1)
        self.song_frame.columnconfigure(7, weight=1)
        self.song_frame.columnconfigure(8, weight=1)
        self.song_frame.columnconfigure(9, weight=1)
        self.song_frame.columnconfigure(10, weight=1)

        self.song1 = tk.Label(self.song_frame, text='1.', font=('Segoe UI Semibold', 12))
        self.song1.grid(row=0, column=0, sticky=tk.W)

        self.song2 = tk.Label(self.song_frame, text='2.', font=('Segoe UI Semibold', 12))
        self.song2.grid(row=1, column=0, sticky=tk.W)

        self.song3 = tk.Label(self.song_frame, text='3.', font=('Segoe UI Semibold', 12))
        self.song3.grid(row=2, column=0, sticky=tk.W)

        self.song4 = tk.Label(self.song_frame, text='4.', font=('Segoe UI Semibold', 12))
        self.song4.grid(row=3, column=0, sticky=tk.W)

        self.song5 = tk.Label(self.song_frame, text='5.', font=('Segoe UI Semibold', 12))
        self.song5.grid(row=4, column=0, sticky=tk.W)

        self.song6 = tk.Label(self.song_frame, text='6.', font=('Segoe UI Semibold', 12))
        self.song6.grid(row=5, column=0, sticky=tk.W)

        self.song7 = tk.Label(self.song_frame, text='7.', font=('Segoe UI Semibold', 12))
        self.song7.grid(row=6, column=0, sticky=tk.W)

        self.song8 = tk.Label(self.song_frame, text='8.', font=('Segoe UI Semibold', 12))
        self.song8.grid(row=7, column=0, sticky=tk.W)

        self.song9 = tk.Label(self.song_frame, text='9.', font=('Segoe UI Semibold', 12))
        self.song9.grid(row=8, column=0, sticky=tk.W)

        self.song10 = tk.Label(self.song_frame, text='10.', font=('Segoe UI Semibold', 12))
        self.song10.grid(row=9, column=0, sticky=tk.W)

        self.song_frame.pack(pady=20)

        self.root.mainloop()



MainMenu()
