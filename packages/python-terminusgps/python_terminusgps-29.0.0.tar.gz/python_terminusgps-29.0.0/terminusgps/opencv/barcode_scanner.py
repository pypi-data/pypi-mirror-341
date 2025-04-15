import cv2 as cv
import numpy as np


def scan_barcode(img: np.ndarray) -> tuple:
    detector = cv.barcode.BarcodeDetector()
    return detector.detectAndDecode(img)
