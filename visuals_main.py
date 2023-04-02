"""
CSC111 Winter 2023 Final Project
RhythmnRadar: Underground Song Recommendation System
This module contains a the pygame visualization code our song recommendation system.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the CSC111 course department
at the University of Toronto St. George campus. All forms of distribution of this code,
whether as given or with any changes, are strictly prohibited. For more information on
copyright for CSC111 project materials, please consult our Course Syllabus.

This file is Copyright (c) 2023 of Mahek Cheema, Kelsang Tsomo, Olindi Mallika Appuhamilage, and Bea Alyssandra Castro
"""
import tkinter as tk
import pyperclip


class LinkHolder:
    """
    A class to hold a single string representing a Spotify link.

    """

    def __init__(self):
        self.link = ""


def on_submit(linkinput: LinkHolder):
    """
    A function to handle the submission of a Spotify link from the user. The attribute linkinput is an
    instance of the LinkHolder class to store the link.
    """
    linkinput.link = input_box.get()
    print("Link stored:", linkinput.link) # testing purposes
    # code to handle the link goes here
    input_box.delete(0, tk.END)


def on_paste():
    """
    A function to handle the pasting of a Spotify link from the user's clipboard.
    """
    input_box.insert(tk.END, pyperclip.paste())


root = tk.Tk()
root.title("RhythmnRadar")
root.configure(bg="black")

# Set up the title and subtitle
title_label = tk.Label(root, text="RhythmnRadar", font=("Avenir", 30), bg="black", fg="white")
title_label.pack(pady=10)

subtitle_label = tk.Label(root, text="Underground Song Recommender", font=("Avenir", 20), bg="black", fg="white")
subtitle_label.pack()

# Set up the instructions label and input box
instructions_label = tk.Label(root, text="Please input your Spotify link here:", font=("Avenir", 16), bg="black",
                              fg="white")
instructions_label.pack(pady=20)


link_holder = LinkHolder()
input_box = tk.Entry(root, width=50, font=("Avenir", 14), bg="black", fg="white", highlightthickness=2,
                     highlightbackground="green")
input_box.pack(pady=10)

# Set up the Go button
go_button = tk.Button(root, text="Go", font=("Avenir", 16), command=lambda: on_submit(link_holder))
go_button.pack(pady=10)

# Set up the Paste button
paste_button = tk.Button(root, text="Paste", font=("Avenir", 16), command=on_paste)
paste_button.pack(pady=10)

root.mainloop()
