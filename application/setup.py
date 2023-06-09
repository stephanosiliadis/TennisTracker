"""
@author: Stefanos Iliadis
"""

from tkinter import *
import customtkinter as ctk

class RootSetup(object):
    """
    Creates the basic setup for the root object 
    and provides the run function
    """
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')

    def __init__(self, title: str, dimensions: tuple, resizable: bool, icon_path: str = None):
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self.root.iconbitmap(icon_path)
        self.root.resizable(resizable, resizable)
        self.base_frame = ctk.CTkFrame(master=self.root, 
                                       width=dimensions[0], 
                                       height=dimensions[1], 
                                       border_color="slateblue",
                                       border_width=3,
                                       corner_radius=12)
        self.base_frame.grid(row=0, column=0)
        print("Root Creation Successful...")

    def __clicked(self):
        print("You cliked a button!")

    def create_button(self):
        self.register_btn = ctk.CTkButton(master=self.base_frame, 
                                          text="Click Me!",
                                          command=self.__clicked)
        self.register_btn.place(relx=0.34, rely=0.5)

    def run_app(self):
        self.root.mainloop()

