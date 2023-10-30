from flask import Blueprint, render_template, current_app, request, Flask
import util.crawl_util as cu
import pandas as pd
import csv

app = Flask(__name__)

crawl_bp = Blueprint('crawl_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':1, 'ma':0,'cb':0,  'sc':0}

#################은행 상품 리스트 ########################
bank_products = [
    {
        "id": 100,
        "name": "우리 으쓱(ESG) 적금",
        "description": "3.60%, 우리카드로 대중교통 이용시 연 0.4%p 금리우대, 환경보호 실천운동 달성시 연 0.4%p 금리우대",
        "image_url": "../static/img/우리은행.jpg",
        "image_url2": "../static/img/우리적금.jpg"
    },
    {
        "id": 101,
        "name": "KB맑은하늘적금",
        "description": "1.95%, 만기해지 할 때까지 이 적금을 종이통장으로 발행한 이력이 없는 경우 0.1%p 우대 영업점의 디지털창구 및 KB태블릿브랜치, 비대면채널(인터넷뱅킹/KB스타뱅킹/스마트상담부)을 통해 이 적금을 가입한 경우  연0.2%p 이 적금의 신규일이 포함된 월의 1일부터 만기일이 포함된 월을 기준으로 전전월 말일까지, 본인명의 KB국민(신용/체크)카드(KB국민비씨카드 제외) 대중교통 이용실적(주) 발생월수가 계약기간의 1/2 이상인 경우 만기해지 할 때까지 이 적금 전용화면을 통해 미세먼지 관련 퀴즈(총 3문항)를 모두 맞춘 경우 연 0.1%p",
        "image_url": "../static/img/국민은행.png",
        "image_url2": "../static/img/국민하늘적금.jpg"
    },
    {
        "id": 102,
        "name": "KB맑은바다적금",
        "description": "2.25%,이 적금 신규 시 해양쓰레기 줄이기 활동에 동의한 경우 [동의문] 본인은 맑은바다를 위한 해양쓰레기 줄이기 활동에 동참하고자 장바구니를 생활화하고 플라스틱 일회용품 사용을 최소화하겠습니다. 연 0.1%p 이 적금 만기해지 할 때까지 종이통장으로 발행한 이력이 없는 경우 연 0.1%p 이 적금 만기해지 할 때까지 본인명의 예금이 「손으로 출금(영업점창구/자동화기기」 이용계좌로 등록되어 있는 경우 연 0.3%p 이 적금 신규월의 다음월 말일 기준으로 아래 2가지 조건 모두 충족한 경우 ① 오픈뱅킹 다른금융 계좌 등록 ②[은행] 개인(신용)정보 수집·이용 (상품서비스 안내 등 및 오픈뱅킹 활용 상품서비스 안내 등) 동의 연 0.3%p ",
        "image_url": "../static/img/국민은행.png",
        "image_url2": "../static/img/국민바다적금.jpg"
    },
    {
        "id": 103,
        "name": "아름다운 용기 적금",
        "description": "2.60%, 우대이자율 (2023.04.28 현재 세전) 준법감시인 사전심사필 제2023-11792-4호 (2023. 04. 28 2024. 04. 28)  다음의 우대요건 충족시 우대이자율 최고 연 1.5% 적용 가능 '1회용 컵 보증금 제도」 알고 실천하기 서약 한 경우 연 0.5% 비대면 또는 무통장 신규 고객 디지털창구 신규 고객 연 0.5% 신한 쏠(SOL)에 다회용기 사용 실천사진 업로드 및 공유 한 경우 연 0.5%  이 예금 신규시점에 예금주가 만 65세 이상 고객인 경우 연 0.5%  ※계약기간 만기 전 중도해지한 계좌에 대해서는 적용하지 않습니다.  ※ 위 우대요건은 만기 전일까지 충족해야 우대이자율 적용 됩니다.",
        "image_url" : "../static/img/신한은행.png",
        "image_url2": "../static/img/신한적금.jpg"
    },
    {
        "id": 5,
        "name": "탄소Zero챌린지적금Ⅱ",
        "description": "2%, 친환경, 저탄소 농축산물 인증서 보유 시 0.01~0.5%p 친환경, 저탄소 농축산물 인증제도 학습 시 0.01~0.5%p ‘탄소중립생활 실천’ 동참 서약 시 0.01~0.5%p 영업점 특별 우대 0.01~0.5%p",
        "image_url": "../static/img/NH농협.png",
        "image_url2": "../static/img/농협적금.jpg"
    },
]
##################################

@crawl_bp.route('/bank')
def bank():
    return render_template('/crawling/bank.html', menu=menu, bank_products=bank_products)



########## 금융상품 리스트 ################
# CSV 파일에서 데이터를 읽어오기
def read_csv():
    financial_products = pd.read_csv('static/data/증권사상품.csv')
    financial_products.drop(columns='Unnamed: 0', inplace=True)    
    return financial_products

# 상품 리스트를 전역 변수로 초기화
financial_products = read_csv()

##############################################

@crawl_bp.route('/finance')
def finance():
    return render_template('/crawling/finance.html',  menu=menu, financial_products=financial_products)


#################카드 리스트##############
products = [
    {
        "id": 1,
        "name": "삼성 iD EV 카드",
        "description": "전기차 충전 50%·70%할인 || 주차장·하이패스·대리운전·배달앱 10% 할인 || 스트리밍 정기결제 20% 할인 등, 30만원 이상, 15000원",
        "image_url": "../static/img/삼성iDEV카드.jpg"
    },
    {
        "id": 2,
        "name": "삼성 iD ENERGY 카드",
        "description": "주유 10000원 할인 || 대중교통·택시·전기차 충전·주차장·대리운전 10% 할인 || 스타벅스 드라이브 스루 30% 할인 등, 50만원 이상, 20000원",
        "image_url": "../static/img/삼성 iD ENERGY 카드.png"
    },
    {
        "id": 3,
        "name": "우리 NU Nature",
        "description": "전기차 충전 60% 적립 || 대중교통 10% 적립 || 스트리밍 정기결제 10% 적립 || 스타벅스 커피 10% 적립 || 주요 간편결제 1.6% 적립 등,30만원 이상, 12000원",
        "image_url": "../static/img/우리 NU Nature.png"
    },
    {
        "id": 4,
        "name": "KB국민 Green Wave 1.5℃카드",
        "description": "전기/수소차 충전·대중교통 10% 적립 || 공유 모빌리티(자전거·킥보드 등)·친환경 마켓 20% 적립 || 스트리밍 정기결제 1천점 적립,40만원 이상, 15000원",
        "image_url": "../static/img/KB국민 Green Wave 1.5℃카드.png"
    },
    {
        "id": 5,
        "name": "NH농협 국민행복카드",
        "description": "병원·조산원·산후조리원·대중교통·온라인 쇼핑몰(쿠팡·11번가 등) 5% 할인 || 카페(스타벅스·커피빈 등) 20% 할인 등,30만원 이상, 없음",
        "image_url": "../static/img/NH농협 국민행복카드.png"
    },
    {
        "id": 6,
        "name": "NH농협 그린카드v2",
        "description": "국내 가맹점 0.2%~1.0% 적립 || 온라인(쇼핑)·생활요금(통신·전기·관리비) 5% 적립 || 대중교통 10%~20% 적립 등 || 영화 할인 || 카페 10% 할인 등, 20만원 이상, 10000원/12000원",
        "image_url": "../static/img/NH농협 그린카드v2.png"
    },
    {
        "id": 7,
        "name": "NH농협 국민행복 체크카드",
        "description": " [B-type: 어린이집·유치원 3%  놀이공원 50% 할인] || A-type: 병/의원/산후조리원 3% 할인 || [C-type: 국내 가맹점 0.2%~0.5% 적립] || 대중교통 3%·카페 10% 할인 등, 30만원 이상, 없음",
        "image_url": "../static/img/NH농협 국민행복 체크카드.png"
    },
    {
        "id": 8,
        "name": "IBK기업 그린카드v2",
        "description": "국내 가맹점 0.2%~1.0% 적립 || 온라인(쇼핑)·생활요금(통신·전기·관리비) 5% 적립 || 대중교통 10%~20% 적립 등 || 영화 할인 || 카페 10% 할인 등, 20만원 이상, 없음/10000원",
        "image_url": "../static/img/IBK기업 그린카드v2.png"
    },
    {
        "id": 9,
        "name": "IBK기업 국민행복카드",
        "description": "청소년산모·건강보험(임신·출산)·보육료 등 지원 || 대중교통 10%~20% 적립 || 어린이집·학원·병원·카페 등 적립, 30만원 이상, 없음",
        "image_url": "../static/img/IBK기업 국민행복카드.png"
    },
    {
        "id": 10,
        "name": "IBK기업 국민행복 체크카드",
        "description": "[B-type: 어린이집·유치원 3% 놀이공원 50% 할인] || A-type: 병/의원/산후조리원 3% 할인 || [C-type: 국내 가맹점 0.2%~0.5% 적립] || 대중교통 3%·카페 10% 할인 등, 20만원 이상, 없음",
        "image_url": "../static/img/IBK기업 국민행복 체크카드.png"
    },
    {
        "id": 11,
        "name": "제주 국민행복카드",
        "description": " [B-type: 어린이집·유치원 5%  놀이공원 50% 할인] || A-type: 병/의원/산후조리원 5% 할인 || [C-type: 국내 가맹점 0.2%~1.0% 적립] || 공통: 온라인 쇼핑몰/대중교통 5% || 통신요금 1천원 할인 || 카페 20% 할인 등 , 없음, 없음",
        "image_url": "../static/img/제주 국민행복카드.gif"
    },
    {
        "id": 12,
        "name": "제주 그린카드",
        "description": "[B-type: 어린이집·유치원 3% 놀이공원 50% 할인] || A-type: 병/의원/산후조리원 3% 할인 || [C-type: 국내 가맹점 0.2%~0.5% 적립] || 대중교통 3%·카페 10% 할인 등, 30만원 이상, 없음",
        "image_url": "../static/img/제주 그린카드.gif"
    },
    
    {
        "id": 13,
        "name": "제주 그린체크카드",
        "description": "영화 2000원 할인 || 카페 10% 할인 || 국내 가맹점 0.2%~0.5% 적립 등, 30만원 이상, 없음",
        "image_url": "../static/img/제주 그린체크카드.gif"
    },
    {
        "id": 14,
        "name": "제주 국민행복 체크카드",
        "description": " || 편의점 7% 할인 || [A-type: 병/의원/산후조리원 3% 할인] || [B-type: 어린이집·유치원 3% | 놀이공원 50% 할인] || [C-type: 국내 가맹점 0.2%~0.5% 적립] || 대중교통 3%·카페 10% 할인 등 , 30만원 이상, 없음",
        "image_url": "../static/img/제주 국민행복 체크카드.gif"
    },
    {
        "id": 15,
        "name": "광주 그린카드v2",
        "description": " ||온라인(쇼핑)·KTX/고속버스·통신요금·카페 5% 적립 || 대중교통 10% 적립 || 국내 가맹점 0.3% 적립 등, 30만원 이상, 10000원/12000원",
        "image_url": "../static/img/광주 그린카드v2.png"
    },
    {
        "id": 16,
        "name": "DGB대구 그린카드v2",
        "description": "국내 가맹점 0.1%~1.0% 적립 || 온라인(쇼핑)·생활요금(통신·전기·관리비) 5% 적립 || 대중교통 10%~20% 적립 등 || 영화 할인 || 카페 10% 할인 등, 40만원 이상, 10000원/12000원",
        "image_url": "../static/img/DGB대구 그린카드v2.png"
    },
    {
        "id": 17,
        "name": "DGB대구 국민행복 체크카드",
        "description": "|| A-type: 병/의원/산후조리원 3% 할인 || [B-type: 어린이집·유치원 3% || 놀이공원 50% 할인] || [C-type: 국내 가맹점 0.2%~0.5% 적립] || 대중교통 3%·카페 10% 할인 등, 없음, 없음",
        "image_url": "../static/img/DGB대구 국민행복 체크카드.gif"
    },
    {
        "id": 18,
        "name": "BNK부산 그린카드v2",
        "description": "국내 가맹점 0.1%~1.0% 적립 || 온라인(쇼핑)·생활요금(통신·전기·관리비) 5% 적립 || 대중교통 10%~20% 적립 등 || 영화 할인 || 카페 10% 할인 등, 40만원 이상, 10000원/12000원",
        "image_url": "../static/img/BNK부산 그린카드v2.png"
    },
    {
        "id": 19,
        "name": "SBI저축 함께그린카드",
        "description": "|| 대형마트·전통시장·유치원·학원·병원 5% 할인 || 외식 주중 5% / 주말 10% 할인 || 영화 2500원 할인 || 금융 수수료 면제, 없음, 없음",
        "image_url": "../static/img/SBI저축 함께그린카드.png"
    },
    {
        "id": 20,
        "name": "SBI저축 내가그린카드",
        "description": "|| 온라인(쇼핑)·점심·서적 5% 할인 || 카페 10% 할인 || 영화·공연·전시 3천원 할인 || 통신요금 2천원 할인 || 금융 수수료 면제, 20만원 이상, 없음",
        "image_url": "../static/img/SBI저축 내가그린카드.png"
    },
    {
        "id": 21,
        "name": "우체국 우리동네plus카드",
        "description": "|| [타입 중 1종 선택] 우체국·마트·백화점·의료·놀이·항공·면세 할인 등, 30만원 이상, 없음",
        "image_url": "../static/img/우체국 우리동네plus카드.png"
    },
]
##########################################################################################


@crawl_bp.route('/card')
def card():    
    num = [0, 1, 2, 3, 4, 5, 6]
    return render_template('/crawling/card.html', menu=menu, products=products, num=num)