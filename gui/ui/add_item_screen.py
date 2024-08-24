from tkinter import *
from tkinter.ttk import *

from gui.api.book_helper import BookHelper
from gui.api.item_db_client import ItemDBClient
from gui.api.product_helper import ProductHelper


class AddItemScreen(Frame):
    def __init__(self, parent, parent_screen=None, db: ItemDBClient = None):
        super().__init__(parent)
        self.barcode_entry_manual = None
        self.purchase_date_entry = None
        self.warranty_link_label = None
        self.warranty_link_entry = None
        self.barcode_label = None
        self.barcode_entry_scan = None
        self.purchase_date_label = None
        self.type_entry = None
        self.type_label = None
        self.quantity_entry = None
        self.quantity_label = None
        self.description_entry = None
        self.description_label = None
        self.name_entry = None
        self.name_label = None
        self.notebook = None
        self.parent = parent
        self.parent_screen = parent_screen
        self.db = db

        self.setup_ui()

    def setup_ui(self):
        # Add 2 tabs to the screen
        self.notebook = Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Create frames for each tab
        manual_add_frame = Frame(self.notebook)
        barcode_add_frame = Frame(self.notebook)

        # Add frames to the notebook
        self.notebook.add(manual_add_frame, text="Manual Add")
        self.notebook.add(barcode_add_frame, text="Barcode Add")

        ### Manual Add Tab ###
        # Create labels and entry fields for manual add based on the Items class in main.py

        # Name
        self.name_label = Label(manual_add_frame, text="Name")
        self.name_label.pack()
        self.name_entry = Entry(manual_add_frame)
        self.name_entry.pack()

        # Barcode
        self.barcode_label = Label(manual_add_frame, text="Barcode")
        self.barcode_label.pack()
        self.barcode_entry_manual = Entry(manual_add_frame)
        self.barcode_entry_manual.pack()

        # Description
        self.description_label = Label(manual_add_frame, text="Description")
        self.description_label.pack()
        self.description_entry = Entry(manual_add_frame)
        self.description_entry.pack()

        # Quantity
        self.quantity_label = Label(manual_add_frame, text="Quantity")
        self.quantity_label.pack()
        self.quantity_entry = Entry(manual_add_frame)
        self.quantity_entry.pack()

        # Type
        self.type_label = Label(manual_add_frame, text="Type")
        self.type_label.pack()
        self.type_entry = Entry(manual_add_frame)
        self.type_entry.pack()

        # Purchase Date
        self.purchase_date_label = Label(manual_add_frame, text="Purchase Date (YYYY-MM-DD)")
        self.purchase_date_label.pack()
        self.purchase_date_entry = Entry(manual_add_frame)
        self.purchase_date_entry.pack()

        # Warranty Link
        self.warranty_link_label = Label(manual_add_frame, text="Warranty Link")
        self.warranty_link_label.pack()
        self.warranty_link_entry = Entry(manual_add_frame)
        self.warranty_link_entry.pack()

        # Add button to add item to the database
        add_button = Button(manual_add_frame, text="Add Item", command=self.add_item)
        add_button.pack()
        ### End Manual Add Tab ###

        ### Barcode Add Tab ###
        self.barcode_label = Label(barcode_add_frame, text="Scan Barcode:")
        self.barcode_label.pack()
        self.barcode_entry_scan = Entry(barcode_add_frame)
        self.barcode_entry_scan.pack()

        # Automatically hit the add_item_by_barcode method when the Enter key is pressed
        self.barcode_entry_scan.bind("<Return>", lambda event: self.add_item_by_barcode())

        add_by_barcode_button = Button(barcode_add_frame, text="Lookup", command=self.add_item_by_barcode)
        add_by_barcode_button.pack()

        ### End Barcode Add Tab ###

        # Back button (shared by both tabs)
        back_button = Button(self, text="Back", command=lambda: self.parent_screen.show_frame("HomeScreen"))
        back_button.pack()

    def add_item_by_barcode(self):
        barcode = self.barcode_entry_scan.get().strip()

        # Identify barcode type
        barcode_type = self._identify_barcode(barcode)

        match barcode_type:
            case "UPC":
                # Lookup the product using the barcode
                product_api = ProductHelper()
                response = product_api.lookup_barcode(barcode)

                product_type = "other"
                if "vinyl" in response.get("title").casefold():
                    product_type = "Vinyl Record"

                # Change tab to Manual, and Add and populate fields with the response
                self.notebook.select(0)
                self.name_entry.insert(0, response.get("title"))
                self.barcode_entry_manual.insert(0, barcode)
                self.description_entry.insert(0, response.get("description"))
                self.type_entry.insert(0, product_type)
                self.quantity_entry.insert(0, 1)
                self.purchase_date_entry.insert(0, "")
                self.warranty_link_entry.insert(0, "")

            case "ISBN":
                # You can implement a similar logic for ISBN lookup
                book_api = BookHelper()
                response = book_api.lookup_barcode(barcode)

                # Change tab to Manual, and Add and populate fields with the response
                self.notebook.select(0)
                self.name_entry.insert(0, response.get("full_title", response.get("title")))
                self.barcode_entry_manual.insert(0, response.get("isbn_13", [barcode])[0])
                self.description_entry.insert(0, f"openlibrary.org{response.get('key', '')}")
                self.type_entry.insert(0, "Book")
                self.quantity_entry.insert(0, 1)
                self.purchase_date_entry.insert(0, "")
                self.warranty_link_entry.insert(0, "")
            case "Unknown":
                print("Unknown barcode")

    def _identify_barcode(self, barcode: str) -> str:
        """Identify the type of barcode based on its length and content. The barcode types are based on the database item types.

        Args:
            barcode (str): The barcode to identify
        """

        # Check if the barcode is a UPC or ISBN or comic book barcode
        print("Identifying barcode type")
        if len(barcode) == 12 and barcode.isdigit():
            return "UPC"
        elif (len(barcode) == 10 or len(barcode) == 13) and \
                (barcode.startswith("ISBN") or barcode.isdigit()):
            # You can add ISBN check digit validation here if needed
            return "ISBN"
        else:
            return "Unknown"

    def add_item(self):
        # Get the item details from the entry fields and create the json object
        item = {
            "name": self.name_entry.get(),
            "barcode": self.barcode_entry_scan.get(),
            "description": self.description_entry.get(),
            "quantity": int(self.quantity_entry.get()),
            "type": self.type_entry.get(),
            "purchase_date": self.purchase_date_entry.get(),
            "warranty_link": self.warranty_link_entry.get()
        }

        try:
            status_code, body = self.db.add_item(item)
            if status_code == 200:
                print("Item added successfully")
                # Add a new label at the bottom to show the item was added successfully
                # Then delete the label after 5 seconds
                tmp_success = Label(self, text=f"'{item['name']}' added to database")
                tmp_success.pack()
                tmp_success.after(5000, lambda: tmp_success.destroy())
            else:
                print(f"Failed to add item: {body}")
        except Exception as e:
            print(f"Failed to add item: {e}")
        finally:
            self.clear_fields()

    def clear_fields(self):
        # Clear all entry fields
        self.name_entry.delete(0, END)
        self.barcode_entry_scan.delete(0, END)
        self.barcode_entry_manual.delete(0, END)
        self.description_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.type_entry.delete(0, END)
        self.purchase_date_entry.delete(0, END)
        self.warranty_link_entry.delete(0, END)
