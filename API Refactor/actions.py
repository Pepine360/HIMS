#flask-related classes
from flask import request
from werkzeug.utils import secure_filename

#manipulation classes
from pyzbar.pyzbar import decode
import numpy as np
from PIL import Image
from typing import List

#custom classes
from product import Product
from storage import Storage
from errors import WrongActionError, NotAnItemError

class Actions():

    #method to decode the image
    #the path is the image path from the file system
    #path can be hardcoded, or is returned by the saveFile() class method
    @classmethod
    def DecodeBarcode(self, path):
        img = Image.open(path)
        barcodes = decode(np.asarray(img))

        if not barcodes:
            return "No barcodes detected"
        
        else:
            for barcode in barcodes:
                if barcode != "":
                    return barcode.data.decode("utf-8")

        return ValueError("No barcode found")

    #Method to save a file coming in from a request
    #It takes the file as the argument, then saves it to the filesystem
    #It then return the path of the file
    #Can be used with the DecodeBarcode() method to get the request's file and decode it
    @classmethod
    def SaveFile(self, file):
        filePath = f"./files/{secure_filename(file.filename)}"
        file.save(filePath)
        return filePath

    @classmethod
    def HandleStorage(self, manipulation : str, item : Product, dbPath : str = "storage.db"):
        if manipulation.lower() == "create":
            Storage.CreateItem(item, dbPath)
        elif manipulation.lower() == "read":
            Storage.ReadItem()
        elif manipulation.lower() == "update":
            Storage.UpdateItem()
        elif manipulation.lower() == "delete":
            Storage.DeleteItem()
        else:
            raise WrongActionError("The action does not exist in the current context!")

    #Method that takes in the barcode and returns all the products fitting the barcode
    #barcode : Product's barcode
    #amount : Minimum amount of products for a specific barcode
    # @classmethod
    # def GetAllData(barcode: str, amount: int = 0) -> list(dict):
    #     pass

