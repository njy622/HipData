import pandas as pd
import re, requests
from urllib.parse import quote
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


'''품목을 취급하는 매장 3곳'''
def get_title_market(title):
    # 품목 리스트 데이터프레임 화
    list_df = pd.read_csv('data/eco_product.csv')

    ### 찾는 품목이 '무' 또는 '김'처럼 한 글자일 경우 에러
    ### TfidfVectorizer의 Default 값으로 한 글자 단어는 제외하게 되어있으므로
    ### 하이퍼 파라미터로 해결 23.10.25

    title = [title.strip(' ')]

    try:
        # 품목이 한 글자일 경우
        if len(title[0]) == 1:
            # TF-IDF 벡터화
            tv = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}')
            title_tv = tv.fit_transform(title).toarray()
        else:
            # 품목 데이터프레임 화
            title_df = pd.DataFrame(title, columns=['title'])
            # TF-IDF 벡터화
            tv = TfidfVectorizer()
            title_tv = tv.fit_transform(title_df['title'])
    except:
        return ['올바른 상품명을 입력해주세요.']

    # 품목 리스트 TF-IDF 벡터화
    list_tv = tv.transform(list_df['title'])

    # 코사인 유사도 계산
    cosine_similarities = cosine_similarity(title_tv, list_tv)

    # 유사도 컬럼으로 추가
    list_df['cosine_similarity'] = cosine_similarities.reshape(-1,1)

    # cosine_similarity의 값이 1.0인 경우만 추출
    list_df = list_df[list_df['cosine_similarity'] == 1.0]

    # 관련된 매장명
    global market
    market = list(set(list_df['market'].values))[:3]
    if market == []:
        return ['해당 상품을 취급하는 매장이 없습니다.']
    
    return market



### 주소 잘못 입력 시, 또는 근처에 매장이 없을 시 리턴 메세지 추가 23.10.24
'''입력한 주소 근처에 매장이 있는지 알아보기'''
def get_market_info(addr):
    # get_title_market 리턴값인 market 가져오기
    market_list = market

    # 고객이 입력한 주소 ['시', '구'] 가져오기
    ### ['군', '면', '리'] 정보 추가 23.10.24
    addr_list = addr.split(' ')
    addr_list1 = []
    addr_list2 = []
    for i in addr_list:
        if i[-1] == '시':
            addr_list1.append(i)
        elif i[-1] == '구':
            addr_list1.append(i)
        elif i[-1] == '군':
            addr_list2.append(i)
        elif i[-1] == '면':
            addr_list2.append(i)
        elif i[-1] == '리':
            addr_list2.append(i)

    addr1 = ' '.join(addr_list1)
    addr2 = ' '.join(addr_list2)

    if addr1 != '':
        addr = addr1
    else:
        addr = addr2
    addr
    # 고객이 입력한 주소 좌표 구하기
    try:
        with open('keys/카카오api.txt') as file:
            kakao_key = file.read()

        base_url = 'https://dapi.kakao.com/v2/local/search/address.json'
        header = {'Authorization': f'KakaoAK {kakao_key}'}
        url = f'{base_url}?query={quote(addr)}'
        result = requests.get(url, headers=header).json()
        lng = float(result['documents'][0]['x'])
        lat = float(result['documents'][0]['y'])
    except:
        return '주소 형식이 올바르지 않습니다.'

    # 정보를 담을 리스트
    results = []

    for mart_name in market_list:

        # 네이버 플레이스 셀레니움으로 들어가기
        n_place_url = f'https://m.place.naver.com/place/list?x={lng}&y={lat}&query={mart_name} {addr}'
        driver = webdriver.Chrome()
        driver.get(n_place_url)

        # '목록보기' 클릭
        filter = driver.find_element(By.XPATH, '//*[@id="_place_portal_root"]/div/a') 
        filter.click()
        time.sleep(3)

        # '거리순' 클릭
        short_way = driver.find_element(By.XPATH, '//*[@id="_list_scroll_container"]/div/div/div[1]/div/div/div/span[2]/a') 
        short_way.click()
        time.sleep(3)

        # '상세 주소 화살표' 클릭
        try:
            juso_way = driver.find_elements(By.CLASS_NAME, 'uFxr1')
            juso_way[0].click()
            time.sleep(1)

            # 마켓 정보 불러오기
            soup = BeautifulSoup(driver.page_source)
            market_list = soup.find('ul', class_='eDFz9')
            mart = market_list.find('li', recursive=False)

            # 현재 위치에서 마켓 거리
            m_distance = mart.select_one('span.lWwyx.NVngW').get_text().split('서')[1]
            # 마켓 이름
            m_title = mart.select_one('span.place_bluelink.YwYLL').get_text()
            # 마켓 주소
            # 지번만 있을 경우
            if mart.select_one('div.zZfO1').get_text()[:2] == '지번':
                m_addr = mart.select_one('div.zZfO1').get_text()[2:-2]
            # 도로명 주소일 경우
            else:
                m_addr = mart.select_one('div.zZfO1').get_text()[3:-2]
            # 딕셔너리 형태로 저장
            market_data = {
                '거리': m_distance,
                '매장명': m_title,
                '주소': m_addr
            }
        except:
            market_data = '근처에 매장이 없습니다.'

        # 딕셔너리 형태로 저장한 것을 리스트에 저장 (3가지 마켓을 넣어야 하므로)
        results.append(market_data)

        for i in range(len(results)):
            if results[i] == '근처에 매장이 없습니다.':
                results[i] = f'{market[i]} 없음'

    return results