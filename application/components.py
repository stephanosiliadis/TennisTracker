from tkinter import *


def hr(master, width, bg, relx, rely) -> Frame:
    """
    Returns something similar to an <hr /> element of HTML
    """
    return Frame(
        master=master,
        width=width,
        height=3,
        highlightthickness=100,
        highlightbackground=bg,
        bg=bg,
    ).place(relx=relx, rely=rely)


def navbar(master, dimensions, color) -> Frame:
    """
    Creates something similar to the <nav></nav> element of HTML
    """
    return Frame(
        master=master,
        width=dimensions[0],
        height=dimensions[1],
        highlightthickness=3,
        highlightbackground=color,
        bg=color,
    ).place(relx=0, rely=0)