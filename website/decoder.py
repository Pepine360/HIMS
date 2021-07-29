from pyzbar.pyzbar import decode
import numpy as np
from PIL import Image
# import cv2


def BarcodeReader(path):
    image = Image.open(path)
    data = np.asarray(image)
    barcodes = decode(data)
    decodedBarcodes = []
    if not barcodes:
        print("No barcodes detected")
    else:
        for barcode in barcodes:
            if barcode.data != "":
                decodedBarcodes.append((barcode.data.decode('utf-8'), barcode.type))
    
    print(decodedBarcodes)
    return decodedBarcodes
