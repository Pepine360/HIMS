class Product():
    def __init__(self, barcode : str, amount : int, name : str ) -> None:
        self.barcode = barcode
        self.amount = amount
        self.name = name
    
    #Returns the data of the product
    def GetProductData(self) -> str:
        return {
            "name" : self._name,
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
    

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name : str):
        self._name = name