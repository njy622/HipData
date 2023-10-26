import pytesseract
import cv2
import re


def get_item_from_img():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\h\AppData\Local\tesseract.exe'
    path = 'static/receipts/receipt01.jpg'
    image = cv2.imread(path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    receipt_data = pytesseract.image_to_string(rgb_image, lang='kor')
    return receipt_data
