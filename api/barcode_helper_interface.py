from abc import ABC, abstractmethod


class BarcodeHelper(ABC):
    @property
    @abstractmethod
    def base_url(self):
        return

    @abstractmethod
    def lookup_barcode(self, barcode: str):
        pass
