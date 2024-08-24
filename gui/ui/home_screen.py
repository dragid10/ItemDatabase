from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from gui.api.item_db_client import ItemDBClient


class HomeScreen(Frame):
    def __init__(self, parent, parent_screen=None, db: ItemDBClient = None):
        super().__init__(parent)
        self.parent = parent
        self.parent_screen = parent_screen
        self.db = db

        # UI Components to hold
        self.barcode_entry_scan = None

        self.setup_ui()

    def setup_ui(self):
        # Button options
        button_options = [
            ("Add Item", lambda: self.parent_screen.show_frame("AddItemScreen")),
            # Replace with actual add item logic
            ("Edit Item", lambda: print("Edit Item clicked")),  # Replace with actual edit item logic
            ("Add Friend", lambda: print("Add Friend clicked")),  # Replace with actual add friend logic
            ("View Loans", lambda: print("View Loans clicked"))  # Replace with actual view loans logic
        ]

        # Create buttons for each option
        for text, command in button_options:
            button = Button(self, text=text, command=command)
            button.pack(pady=10)  # Add vertical spacing between buttons

        # Add a separator between the buttons and the exit button
        separator = Separator(self, orient="horizontal")
        separator.pack(fill="x", pady=10)

        # Add a barcode bar so that users can scan barcodes and view product information from db
        barcode_label = Label(self, text="Scan Barcode:")
        barcode_label.pack()
        self.barcode_entry_scan = Entry(self)
        self.barcode_entry_scan.pack()

        # Automatically hit the add_item_by_barcode method when the Enter key is pressed
        self.barcode_entry_scan.bind("<Return>", lambda event: self.lookup_in_database())

        # Create a button to exit the program
        exit_button = Button(self, text="Exit", command=self.parent.quit)
        exit_button.pack(pady=10)

    def lookup_in_database(self):
        barcode: str = self.barcode_entry_scan.get().strip()

        # Lookup the item in the database
        status_code, result = self.db.get_item_by_barcode(item_barcode=barcode)
        if status_code != 200:
            # Create an alert to display the message that the item was not found in the database
            messagebox.showerror("Error", f"Item not found in database.")

        # Display the item information in a new window
        self.display_item_information(result)

    def display_item_information(self, result: dict):
        # Create a new window to display the item information
        item_info_window = Toplevel(self)
        item_info_window.title("Item Information")

        # Create labels to display the item information
        for key, value in result.items():
            label = Label(item_info_window, text=f"{key}: {value}")
            label.pack()
