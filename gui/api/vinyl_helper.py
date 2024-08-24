import requests

from gui.api.barcode_helper_interface import BarcodeHelper


class ProductHelper(BarcodeHelper):
    def __init__(self):
        self._base_url = f"https://musicbrainz.org/ws/2/release?query=barcode:%<BARCODE_FILL>%22&fmt=json&limit=1"
        self.sess = requests.Session()

    @property
    def base_url(self):
        return self._base_url

    def lookup_barcode(self, barcode: str):
        request_url = self.base_url.replace("<BARCODE_FILL>", barcode)
        response = self.sess.get(request_url)

        response.raise_for_status()
        json_response = response.json().get("items")[0]

        return json_response
