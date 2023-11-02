import pytesseract
import cv2
import re


def get_item_from_img(filename):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\thdal\AppData\Local\tesseract.exe'
    image = cv2.imread(f'./static/upload/{filename}')
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    receipt_data = pytesseract.image_to_string(rgb_image, lang='kor')
    print(receipt_data)
    return receipt_data


##### 해당 영수증 업로드 할때 해야하는 사전 작업
## 1. https://github.com/UB-Mannheim/tesseract/wiki 에서 tesseract-ocr 다운로드
## 2. C:\Users사용자_이름\AppData\Local\ 경로에 설치   !! 한글설치 필수
## 3. pip install pytesseract
## 3. pip install opencv-python