#flask-related classes
from flask import request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

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
    #It takes the file (FileStorage type) as the argument, then saves it to the filesystem
    #It then return the path of the file
    #Can be used with the DecodeBarcode() method to get the request's file and decode it
    @classmethod
    def SaveFile(self, file):

        if type(file) == FileStorage:
            filePath = f"./files/{secure_filename(file.filename)}"
            file.save(filePath)
            return filePath
        raise TypeError(f"{str(file)} is not a FileStorage object")

    @classmethod
    def HandleStorage(self, manipulation : str, item : Product, dbPath : str = "storage.db"):
        if manipulation.lower() == "create":
            Storage.CreateItem(item, dbPath)
        elif manipulation.lower() == "read":
            return Storage.ReadItem(item, dbPath)
        elif manipulation.lower() == "update":
            Storage.UpdateItem()
        elif manipulation.lower() == "delete":
            Storage.DeleteItem()
        else:
            raise WrongActionError("The action does not exist in the current context!")


    @classmethod
    def scrub(self, text : str):
        return ("".join( char for char in text if char.isalnum() or char ==  '_')) if text != None else text

    #Method that takes in the barcode and returns all the products fitting the barcode
    #barcode : Product's barcode
    #amount : Minimum amount of products for a specific barcode
    # @classmethod
    # def GetAllData(barcode: str, amount: int = 0) -> list(dict):
    #     pass

