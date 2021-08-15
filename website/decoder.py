from pyzbar.pyzbar import decode
from io import BytesIO
from PIL import Image

def BarcodeReader(image):
    barcodes = decode(Image.open(BytesIO(image)))

    if not barcodes:
        print("No barcodes detected")

    else:
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            if barcode.data != "":
                print(barcode.data.decode("utf-8"))
                print(barcode.type)
                return (True, barcode.data.decode("utf-8"))
    return (False, "No data could be decoded!")


if __name__ == "__main__":
    BarcodeReader()
