'''
1.
https://github.com/UB-Mannheim/tesseract/wiki
에서 tesseract-ocr 다운로드

2.
C:\Users\사용자_이름\AppData\Local\ 
경로에 설치

!! 한글설치 필수

3.
pip install pytesseract

3.
pip install opencv-python

'''


import pytesseract
import cv2
import re


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\h\AppData\Local\tesseract.exe'

path = 'image/M.1401006816.5629.4.jpg'
image = cv2.imread(path)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

text = pytesseract.image_to_string(rgb_image, lang='kor')
text_list = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣\\n]', '', text).split('\n')
text_list

