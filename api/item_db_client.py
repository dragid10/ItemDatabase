import arrow
import requests


class ItemDBClient:
    def __init__(self):
        self._base_url = "http://localhost:8000"
        self.sess = requests.Session()

    def add_item(self, item):
        # Convert any empty fields to None
        for key, value in item.items():
            if not value:
                item[key] = None

        # If purchase date field isn't null or empty, use arrow to convert to python date object
        if item["purchase_date"]:
            item["purchase_date"] = arrow.get(item["purchase_date"]).datetime.date()

        response = self.sess.post(f"{self._base_url}/items", json=item)
        json_response = response.json()
        return response.status_code, json_response
