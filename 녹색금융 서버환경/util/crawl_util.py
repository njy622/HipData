import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

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
            rank = int(rank_data[0]['class'][1][-1])
        else:
            rank = int(rank_data[0]['class'][1][-1] + rank_data[1]['class'][1][-1])
        href = li.select_one('.coverImage > label > a')['href']     # 자식 셀렉터
        src = li.select_one('.coverImage img')['src']               # 자손 셀렉터
        title = li.select_one('.itemName').get_text().strip()
        author = li.select_one('.author').get_text().strip()
        company = li.select_one('.company').get_text().strip()
        price = li.select_one('.price > em').get_text().strip()
        price = int(price.replace(',', ''))
        data.append({'순위':rank, '제목':title, '저자':author, '출판사':company, 
                     '가격':f'{price:7,d}', 'href':base_url+href, 'src':src})

    return data

def get_melon_chart():
    url = 'https://www.melon.com/chart/index.htm'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    date_str = soup.select_one('.yyyymmdd').get_text().strip() + \
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
        data.append({'순위':rank, '제목':title, '아티스트':artist, '앨범':album, '이미지':img})    
    
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
