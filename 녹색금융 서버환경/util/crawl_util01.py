import requests, time
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_bestseller():
    base_url = 'http://book.interpark.com'
    url = f'{base_url}/display/collectlist.do?_method=bestsellerHourNew&bookblockname=b_gnb&booklinkname=%BA%A3%BD%BA%C6%AE%C1%B8&bid1=w_bgnb&bid2=LiveRanking&bid3=main&bid4=001'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    lis = soup.select('.rankBestContentList > ol > li')

    data = []
    for li in lis:
        rank_data = li.select('.rankBtn_ctrl')
        if len(rank_data) == 1:
            rank = int(rank_data[0]['class'][-1][-1])
        else:
            rank = int(rank_data[0]['class'][-1][-1] + rank_data[1]['class'][-1][-1])
        title = li.select_one('.itemName').get_text().strip()
        author = li.select_one('.author').get_text().strip()
        company = li.select_one('.company').get_text().strip()
        price = li.select_one('.price > em').get_text().strip()
        price = int(price.replace(',', ''))
        href_ = li.select_one('.coverImage > label > a')['href']
        image_ = li.select_one('.coverImage > label > a > img')['src']
        data.append({'순위': rank, '제목':title, '저자':author, '출판사':company, '가격':f'{price:7,d}', '링크':base_url+href_, '이미지':image_})

    return data

def get_melonchart():
    url = 'https://www.melon.com/chart/index.htm'
    header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    date_str = soup.select_one('.yyyymmdd').get_text().strip() +\
                soup.select_one('.hhmm').get_text().strip()
    date_str = date_str.replace('.', '').replace(':', '')
    trs = soup.select('.lst50')
    data = []
    for tr in trs:
        rank = int(tr.select_one('.rank').get_text().strip())
        title = tr.select_one('.ellipsis.rank01').get_text().strip()
        artist = tr.select_one('.ellipsis.rank02 > a').get_text().strip()
        album = tr.select_one('.ellipsis.rank03').get_text().strip()
        img = tr.select_one('tr > td:nth-child(4) > div > a > img')['src']
        data.append({'순위' : rank, '제목' : title, '아티스트' : artist, '앨범' : album, '이미지' : img})
        
    return data

def get_restaurant_list_more(rest_name):
    base_url = 'https://www.siksinhot.com/search'
    url = f'{base_url}?keywords={quote(rest_name)}'
    # res = requests.get(url)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    for _ in range(2):
        atag_js = driver.find_element(By.CSS_SELECTOR, '.div_search_menu > div > a.moreBtn')
        atag_js.send_keys('\n')
        time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lis = soup.select('.localFood_list > li')
    data = []
    for li in lis:
        atag = li.select_one('figcaption > a')
        name = atag.select_one('h2').get_text().strip()
        score = atag.select_one('.score').get_text().strip()
        menu = li.select('.cate > a')[-1].get_text().strip()
        sub_href = atag['href']
        # sub_res = requests.get(sub_href)
        sub_res = driver.get(sub_href)
        time.sleep(2)
        sub_soup = BeautifulSoup(driver.page_source, 'html.parser')
        info = sub_soup.select('.pc_only > td')
        addr = info[0].select_one('div').get_text().split('지번')[0].strip()
        try:
            tel = info[1].select_one('div').get_text().strip()
        except:
            tel = ' '
        data.append({'업소명':name, '평점':score, '메뉴':menu, '주소':addr, '전화번호':tel})

    return data

def get_restaurant_list(place):
    base_url = 'https://www.siksinhot.com/search'
    url = f'{base_url}?keywords={quote(place)}'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    lis = soup.select('.localFood_list > li')
    data = []
    for li in lis:
        atag = li.select_one('figcaption > a')
        name = atag.select_one('h2').get_text().strip()
        score = atag.select_one('.score').get_text().strip()
        menu = li.select('.cate > a')[-1].get_text().strip()
        sub_href = atag['href']
        sub_res = requests.get(sub_href)
        sub_soup = BeautifulSoup(sub_res.text, 'html.parser')
        info = sub_soup.select('.pc_only > td')
        addr = info[0].select_one('div').get_text().split('지번')[0].strip()
        tel = info[1].select_one('div').get_text().strip()
        data.append({'업소명':name, '평점':score, '메뉴':menu, '주소':addr, '전화번호':tel})
    return data

def get_item_list():
    url = 'https://www.musinsa.com/ranking/best'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    driver.fullscreen_window()
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(10):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
    memberships = driver.find_elements(By.CSS_SELECTOR, '.li_inner > .article_info > .membership')
    time.sleep(2)
    data = []
    for index, member in enumerate(memberships):
        member.click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        lis = soup.select('.snap-article-list > .li_box')
        li = lis[index]
        ps = li.select('.item_title')
        brand = ps[-1].get_text().strip()
        link = li.select_one('.list_img > a')['href']
        img = li.select_one('div.list_img > a > img')['src']
        name = li.select_one('.article_info > .list_info > a').get_text().strip()
        price = int(li.select_one('.article_info > .price').get_text().strip().replace(',', '').replace('원', '').split('\n')[0])
        no_member_price = int(li.select_one('.member_price > ul > li > .txt_price_member').get_text().strip().replace(',', '').replace('원', ''))
        member_price_lis = li.select('.article_info > .member_price > ul > li')[1:10]
        member_dict = {}
        for member_li in member_price_lis:
            membership_name = member_li.get_text().strip(member_li.select_one('.txt_price_member').get_text().strip())
            membership_price = int(member_li.select_one('.txt_price_member').get_text().strip().replace(',', '').replace('원',''))
            member_dict[membership_name] = membership_price
        data.append({'브랜드' : brand, '링크': link, '이미지':img, '이름':name, '가격':f'{price:,d}', '비회원가격':f'{no_member_price:,d}', '멤버가격':member_dict})
        member.click()

    return data
        


