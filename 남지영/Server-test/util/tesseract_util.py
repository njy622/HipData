import pytesseract
import cv2
import re


def get_item_from_img(filename):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\mwsong\AppData\Local\Tesseract-OCR\tesseract.exe'
    image = cv2.imread(f'./static/upload/{filename}')
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    receipt_data = pytesseract.image_to_string(rgb_image, lang='kor')
    return receipt_data