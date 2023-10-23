import requests, json, os, folium
import numpy as np
import pandas as pd
from urllib.parse import quote

def get_station_map(root_path, stations):
    # 도로명 주소 구하기
    # filename = '../04.지도시각화/keys/도로명주소apiKey.txt'
    filename = os.path.join(root_path, 'static/keys/도로명주소apiKey.txt')
    with open(filename) as file:
        road_key = file.read()

    base_url = 'https://www.juso.go.kr/addrlink/addrLinkApi.do'
    params1 = f'confmKey={road_key}&currentPage=1&countPerPage=10'
    road_addr_list = []
    for station in stations:
        params2 = f'keyword={quote(station)}&resultType=json'
        url = f'{base_url}?{params1}&{params2}'
        result = requests.get(url)
        if result.status_code == 200:
            res = json.loads(result.text)
            road_addr_list.append(res['results']['juso'][0]['roadAddr'])
        else:
            print(result.status_code)
    df = pd.DataFrame({'이름': stations, '주소': road_addr_list})

    # 위도, 경도 좌표 구하기
    filename = os.path.join(root_path, 'static/keys/카카오apiKey.txt')
    with open(filename) as file:
        kakao_key = file.read()
    base_url = 'https://dapi.kakao.com/v2/local/search/address.json'
    header = {'Authorization': f'KakaoAK {kakao_key}'}

    lat_list, lng_list = [], []
    for i in df.index:
        url = f'{base_url}?query={quote(df["주소"][i])}'
        result = requests.get(url, headers=header).json()
        lat_list.append(float(result['documents'][0]['y']))
        lng_list.append(float(result['documents'][0]['x']))
    df['위도'] = lat_list
    df['경도'] = lng_list

    # map 그리기
    map = folium.Map(location=[df.위도.mean(), df.경도.mean()], zoom_start=14)  # Center position
    for i in df.index:
        folium.Marker(
            location=[df.위도[i], df.경도[i]],       
            tooltip=df.이름[i],
            popup=folium.Popup(df.주소[i], max_width=200)
        ).add_to(map)   
    filename = os.path.join(root_path, 'static/img/station_map.html')
    map.save(filename)

def show_station_map():
    html = f'''
        <iframe src="../static/img/station_map.html" frameborder="1" width="800" height="500"></iframe>
    '''
    return html

def get_text_location(geo_str):
    gu_dict = {}
    for gu in geo_str['features']:
        for coord in gu['geometry']['coordinates']:
            geo = np.array(coord)
            gu_dict[gu['id']] = [np.mean(geo[:,1]), np.mean(geo[:,0])]
    return gu_dict

def get_cctv(static_path):
    filename = f'{static_path}/data/서울시 구별 CCTV 인구 현황.csv'
    df = pd.read_csv(filename, index_col='구별')
    geo_data = json.load(open(f'{static_path}/data/seoul_geo_simple.json', encoding='utf-8'))

    map = folium.Map([37.55, 126.98], zoom_start=11, tiles='Stamen Toner')
    folium.Choropleth(
        geo_data=geo_data,      # GEO 지도 데이터
        data=df.CCTV댓수,       # 단계구분도로 보여줄 데이터
        columns=[df.index, df.CCTV댓수],        # 데이터프레임에서 추출할 항목
        fill_color='RdPu',      # Colormap
        key_on='feature.id'     # 지도에서 조인할 항목
    ).add_to(map)
    gu_dict = get_text_location(geo_data)
    for gu_name in df.index:
        folium.map.Marker(
            location=gu_dict[gu_name],
            icon = folium.DivIcon(icon_size=(80,20), icon_anchor=(20,0),
                        html=f'<span style="font-size: 10pt">{gu_name}</span>')
    ).add_to(map)
    map.save(f'{static_path}/img/cctv.html')

def get_cctv_pop(static_path, column, colormap):
    filename = f'{static_path}/data/서울시 구별 CCTV 인구 현황.csv'
    df = pd.read_csv(filename, index_col='구별')
    geo_data = json.load(open(f'{static_path}/data/seoul_geo_simple.json', encoding='utf-8'))

    map = folium.Map([37.55, 126.98], zoom_start=11, tiles='Stamen Toner')
    folium.Choropleth(
        geo_data=geo_data,      # GEO 지도 데이터
        data=df[column],        # 단계구분도로 보여줄 데이터
        columns=[df.index, df[column]],     # 데이터프레임에서 추출할 항목
        fill_color=colormap,    # Colormap
        key_on='feature.id'     # 지도에서 조인할 항목
    ).add_to(map)
    gu_dict = get_text_location(geo_data)
    for gu_name in df.index:
        folium.map.Marker(
            location=gu_dict[gu_name],
            icon = folium.DivIcon(icon_size=(80,20), icon_anchor=(20,0),
                        html=f'<span style="font-size: 10pt">{gu_name}</span>')
    ).add_to(map)
    map.save(f'{static_path}/img/cctv_pop.html')

def show_cctv_pop(colormap):
    html = f'''<iframe src="../static/img/cctv_pop.html" frameborder="1"
        width="800" height="500"></iframe><br>
        <button class="btn btn-primary" onclick="location.href='/map/cctv_pop'">재실행</button>&nbsp;&nbsp;&nbsp;
        <span>선택한 컬러맵 : {colormap}</span>'''
    return html

def get_coord(static_path, place):
    # 도로명 주소 api
    filename = os.path.join(static_path, 'keys/도로명주소apiKey.txt')
    with open(filename) as file:
        road_key = file.read()
    base_url = 'https://www.juso.go.kr/addrlink/addrLinkApi.do'
    params1 = f'confmKey={road_key}&currentPage=1&countPerPage=10'
    params2 = f'keyword={quote(place)}&resultType=json'
    url = f'{base_url}?{params1}&{params2}'
    result = requests.get(url).json()
    road_addr = result['results']['juso'][0]['roadAddr']
    
    # kakao api
    filename = os.path.join(static_path, 'keys/카카오apiKey.txt')
    with open(filename) as file:
        kakao_key = file.read()
    base_url = 'https://dapi.kakao.com/v2/local/search/address.json'
    header = {'Authorization': f'KakaoAK {kakao_key}'}
    url = f'{base_url}?query={quote(road_addr)}'
    result = requests.get(url, headers=header).json()
    lat = float(result['documents'][0]['y'])
    lng = float(result['documents'][0]['x'])

    return lat, lng