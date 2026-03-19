# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "opencv-python>=4.13.0.92",
#     "qrcode[pil]>=8.2",
# ]
# ///
import os
import sys

import qrcode
import cv2


def write(bracket: str):
    options = {
        # "fill_color": (0xFF, 0xCC, 0x00),
        # "back_color": (0x00, 0x33, 0x66),
    }
    qr = qrcode.QRCode()
    qr.add_data(bracket)
    img = qr.make_image(**options)
    img.save(f"{bracket}.png")


def read(filename: str):
    img = cv2.imread(filename)
    det = cv2.QRCodeDetector()
    bracket, _, _ = det.detectAndDecode(img)
    return bracket


if __name__ == "__main__":
    param = sys.argv[1] if len(sys.argv) > 1 else "FoASVv4ou3U"
    if os.path.isfile(param):
        print(read(param), end="\n\n")
    else:
        write(param)
