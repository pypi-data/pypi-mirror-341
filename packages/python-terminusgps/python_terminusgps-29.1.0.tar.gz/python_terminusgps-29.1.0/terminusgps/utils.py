import numpy as np
from pyzbar.pyzbar import decode


def scan_barcode(img: np.ndarray) -> list:
    return decode(img)
