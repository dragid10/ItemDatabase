import http

import arrow
import requests


class ItemDBClient:
    def __init__(self):
        self._base_url = "http://localhost:8000"
        self.sess = requests.Session()

    def add_item(self, item: dict) -> tuple[int, dict]:
        # Convert any empty fields to None
        for key, value in item.items():
            if not value:
                item[key] = None

        # If purchase date field isn't null or empty, use arrow to convert to python date object
        if item["purchase_date"]:
            item["purchase_date"] = arrow.get(item["purchase_date"]).datetime.date()

        try:
            response = self.sess.post(f"{self._base_url}/items", json=item)
            response.raise_for_status()
        except Exception as e:
            return http.HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Connection Error: {e}"}

        status_code, json_response = response.status_code, response.json()
        return status_code, json_response

    def get_item_by_barcode(self, item_barcode: str) -> tuple[int, dict]:
        """ Get an item from the database by its ID

        Args:
            item_barcode (str): The barcode value of the item to retrieve

        Returns: A tuple containing the status code and the JSON response

        """
        response = self.sess.get(f"{self._base_url}/items/barcode/{item_barcode}")

        try:
            status_code, json_response = response.status_code, response.json()
            response.raise_for_status()
        except Exception as e:
            return http.HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Connection Error: {e}"}
        return status_code, json_response
