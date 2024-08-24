import requests

from gui.api.barcode_helper_interface import BarcodeHelper


class ProductHelper(BarcodeHelper):
    def __init__(self):
        self._base_url = "https://api.upcitemdb.com/prod/trial/lookup?upc="
        self.sess = requests.Session()

    @property
    def base_url(self):
        return self._base_url

    def lookup_barcode(self, barcode: str ):
        response = self.sess.get(f"{self.base_url}{barcode}")

        response.raise_for_status()
        json_response = response.json().get("items")[0]

        return json_response
