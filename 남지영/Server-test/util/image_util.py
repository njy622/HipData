import os
import numpy as np
from PIL import Image

# Pillow format의 img를 읽어서 중심부의 정사각형 이미지를 Pillow format으로 반환
def center_image(img):
    h, w, _ = np.array(img).shape
    diff = abs(h - w) // 2
    if w > h:           # landscape image
        final_img = np.array(img)[:, diff:diff+h, :]
    else:               # portrait image
        final_img = np.array(img)[diff:diff+w, :, :]
    return Image.fromarray(final_img)

def change_profile(static_folder, filename, uid):
    img = Image.open(filename)
    new_fname = os.path.join(static_folder, 'profile/' + uid + '.png')
    center_image(img).save(new_fname, format='png')
    return int(os.stat(new_fname).st_mtime)     # 마지막으로 파일이 수정된 시각(int type으로 반환)