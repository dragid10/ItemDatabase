from tkinter import *
from tkinter.ttk import *

from gui.ui.add_item_screen import AddItemScreen


class HomeScreen(Frame):
    def __init__(self, parent, parent_screen=None):
        super().__init__(parent)
        self.parent = parent
        self.parent_screen = parent_screen
        self.setup_ui()

    def setup_ui(self):
        # Button options
        button_options = [
            ("Add Item", lambda: self.parent_screen.show_frame(AddItemScreen)),  # Replace with actual add item logic
            ("Edit Item", lambda: print("Edit Item clicked")),  # Replace with actual edit item logic
            ("Add Friend", lambda: print("Add Friend clicked")),  # Replace with actual add friend logic
            ("Checkout Item", lambda: print("Checking Out Item")),  # Replace with actual loan item logic
            ("Checkin Item", lambda: print("Checking In Item")),  # Replace with actual loan item logic
            ("View Loans", lambda: print("View Loans clicked"))  # Replace with actual view loans logic
        ]

        # Create buttons for each option
        for text, command in button_options:
            button = Button(self, text=text, command=command)
            button.pack(pady=10)  # Add vertical spacing between buttons
