class Product():
    def __init__(self, barcode : str, amount : int) -> None:
        self.barcode = barcode
        self.amount = amount
    
    #Returns the data of the product
    def getProductData(self) -> str:
        return {
            "barcode" : self._barcode,
            "amount" : self._amount
        }

    @property
    def barcode(self):
        return self._barcode
    
    @barcode.setter
    def barcode(self, barcode : str):
        self._barcode = barcode

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount : int):
        if amount < 0:
            raise ValueError(f"{amount} is smaller than 0!")
        self._amount = amount
        