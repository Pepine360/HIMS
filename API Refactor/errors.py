class Error(Exception):
    pass

class WrongActionError(Error):
    pass

class NotAnItemError(Error):
    pass

class InvalidBarcodeError(Error):
    pass