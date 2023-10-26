import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



'''영수증으로 얻을 수 있는 포인트 알아보기'''
def receipt_get_point(receipt_data):
    # 영수증 전처리
    receipt = receipt_data.split('\n')
    receipt_df = pd.DataFrame(receipt, columns=['title'])
    receipt_df['title'] = receipt_df['title'].apply(lambda x: re.sub('[^가-힣\s]', '', x))
    receipt_df = receipt_df[receipt_df.title != '']
    receipt_df.set_index('title', inplace=True)
    receipt_df.reset_index(inplace=True)

    # 비교 데이터프레임 호출
    list_df = pd.read_csv('../data/eco_product.csv')

    # TF-IDF 벡터화
    tv = TfidfVectorizer()
    receipt_tv = tv.fit_transform(receipt_df['title'])
    list_tv = tv.transform(list_df['title_mod'])

    # 코사인 유사도 계산
    cosine_similarities = cosine_similarity(receipt_tv, list_tv)

    # 유사도 컬럼으로 추가
    receipt_df['cosine_similarity'] = cosine_similarities.max(axis=1)

    # 유사한 항목 추가
    most_similar_indices = cosine_similarities.argmax(axis=1)
    most_similar_items = list_df.loc[most_similar_indices, 'title_mod'].values
    receipt_df['most_similar_item'] = most_similar_items
    receipt_df['point'] = list_df.loc[most_similar_indices, 'point'].values
    receipt_df['title'] = list_df.loc[most_similar_indices, 'title'].values

    # cosine_similarity의 값이 0.5 이상인 경우만 추출
    receipt_df = receipt_df[receipt_df['cosine_similarity'] >= 0.5]

    # 결과
    receipt_list = []
    point_list = []
    for i in receipt_df.index:
        point_list.append(receipt_df['point'][i])
        receipt_list.append(f'''{receipt_df['title'][i]}({str(receipt_df['point'][i])+'% 적립' if receipt_df['point'][i] == 10 else str(receipt_df['point'][i])+'p'})''')
    total_item = '\n'.join(receipt_list)
    accu = 0
    t_point = 0
    for i in point_list:
        if i == 10:
            accu += i
        else:
            t_point += i

    if accu == 0:
        total_point = f'\n\n총 {t_point}p'
    elif t_point == 0:
        total_point = f'\n\n총 {accu}% 적립'
    else:
        total_point = f'\n\n총 {accu}% 적립 + {t_point}p'

    total_result = total_item + total_point
    return total_result

