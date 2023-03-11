import qrcode
import cv2


def write(bracket: str):
    img = qrcode.make(bracket)
    img.save(f"{bracket}.png")

    qr = qrcode.QRCode()
    qr.add_data(bracket)
    img = qr.make_image(fill_color=(0xFF, 0xCC, 0x00), back_color=(0x00, 0x33, 0x66))
    img.save(f"{bracket}_styled.png")


def read(filename: str):
    img = cv2.imread(filename)
    det = cv2.QRCodeDetector()
    bracket, _, _ = det.detectAndDecode(img)
    return bracket
