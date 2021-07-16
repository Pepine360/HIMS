from pyzbar.pyzbar import decode
import cv2
from imager import imageTaker
from finder import FindBarcode

def BarcodeReader():
    # image = cv2.imread("c2.png")
    image = cv2.imread("barcode3.png")
    barcodes = decode(image)

    if not barcodes:
        print("No barcodes detected")

    else:
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x-10, y-10),
                          (x + w + 10, y + h + 10), (255, 0, 0), 2)
            if barcode.data != "":
                print(barcode.data.decode("utf-8"))
                print(barcode.type)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    


if __name__ == "__main__":
    BarcodeReader()
