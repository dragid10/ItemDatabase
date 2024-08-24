import requests

from gui.api.barcode_helper_interface import BarcodeHelper


class BookHelper(BarcodeHelper):
    def __init__(self):
        self._base_url = "https://openlibrary.org/isbn/"
        self.sess = requests.Session()

    @property
    def base_url(self):
        return self._base_url

    def lookup_barcode(self, barcode: str):
        # if the barcode value doesn't start with '978', add it
        if not barcode.startswith("978"):
            barcode = f"978{barcode}"

        # Make a GET request to the Open Library API
        response = self.sess.get(f"{self._base_url}{barcode}.json")

        # Raise an exception if the response status code is not 200
        response.raise_for_status()

        # Return the JSON response
        json_response = response.json()

        return json_response
