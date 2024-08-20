import tkinter as tk
from tkinter import ttk

# Import your screen classes
from gui.ui.home_screen import HomeScreen
from gui.ui.add_item_screen import AddItemScreen


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()

        # Window configuration
        self.title("Item Database")
        self.geometry("500x500")
        self.resizable(True, True)

        # Container for different screens
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Dictionary to store screens
        self.frames = {}

        # Dynamically add screens to the frames dictionary
        screen_classes = [HomeScreen, AddItemScreen]  # Add other screen classes here
        for F in screen_classes:
            frame = F(parent=container, parent_screen=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the HomeScreen initially
        self.show_frame(HomeScreen)

    def show_frame(self, container):
        """Raises the specified frame to the top."""
        frame = self.frames[container]
        frame.tkraise()
