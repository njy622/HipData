import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def receipt_get_point(receipt_data):
    # 영수증 전처리
    receipt = receipt_data.split('\n')
    receipt_df = pd.DataFrame(receipt, columns=['title'])
    receipt_df['title'] = receipt_df['title'].apply(lambda x: re.sub('[^가-힣]', '', x))
    receipt_df = receipt_df[receipt_df.title != '']
    receipt_df.set_index('title', inplace=True)
    receipt_df.reset_index(inplace=True)

    # 비교 데이터프레임 호출
    list_df = pd.read_csv('data/eco_product.csv')

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

    # 포인트 합계
    return receipt_df['point'].sum()

    # 비교 데이터프레임 호출
    list_df = pd.read_csv('data/eco_product.csv')

    # 검색어 데이터프레임 화
    title = [title]
    title_df = pd.DataFrame(title, columns=['title'])
    title_df

    # TF-IDF 벡터화
    tv = TfidfVectorizer()
    title_tv = tv.fit_transform(title_df['title'])
    list_tv = tv.transform(list_df['title'])

    # 코사인 유사도 계산
    cosine_similarities = cosine_similarity(title_tv, list_tv)

    # 유사도 컬럼으로 추가
    list_df['cosine_similarity'] = cosine_similarities.reshape(-1,1)

    # cosine_similarity의 값이 0.5 이상인 경우만 추출
    list_df = list_df[list_df['cosine_similarity'] >= 0.3]

    # 관련된 마켓명
    market = set(list_df['market'].values.tolist())
    return list(market)[:5]

