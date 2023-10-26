from flask import Flask, render_template, request, flash, session, current_app, jsonify
from bp.crawling import crawl_bp
from bp.map import map_bp
from bp.user import user_bp
from bp.chatbot import chatbot_bp
from bp.schedule import schdedule_bp
import os, json, random
import util.map_util as mu
import util.weather_util as wu
import util.image_util as iu
import db_sqlite.profile_dao as pdao
# tesseract
import util.tesseract_util as tess
# receipt
import util.receipt_util as rece
# item_analysis
import util.item_analysis as item


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/receipts'


app.register_blueprint(crawl_bp, url_prefix='/crawling')    # localhost:5000/crawling/* 는 crawl bp가 처리
app.register_blueprint(map_bp, url_prefix='/map')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
app.register_blueprint(schdedule_bp, url_prefix='/schedule')

# for AJAX ###################################################

""" 프로파일 날씨정보 불러오기 """
@app.route('/weather')
def weather():
    # 서울시 영등포구 + '청' -> 도로명 주소 -> 카카오 로컬 -> 좌표 획득
    addr = request.args.get('addr') 
    lat, lng = mu.get_coord(app.static_folder, addr + '청')
    html = wu.get_weather(app.static_folder, lat, lng)
    return html



""" 프로파일 정보 """
@app.route('/changeProfile', methods=['GET','POST'])
def change_profile():
    if request.method == 'GET':
        profile = pdao.get_profile(session['profile'][0])
        return json.dumps(profile)
    else:
        email = request.form['email']
        try:
            file_image = request.files['image']
            image = file_image.filename
            filename = os.path.join(app.static_folder, f'upload/{file_image.filename}')
            file_image.save(filename)
            mtime = iu.change_profile(app.static_folder, filename, session['uid'])
        except:
            image = request.form['hiddenImage']     # image의 변화가 없으면 hiddenImage값을 사용
            mtime = 0
        state_msg = request.form['stateMsg']
        github = request.form['github']
        insta = request.form['insta']
        addr = request.form['addr']
        params = [image, state_msg, github, insta, addr, email]
        pdao.update_profile(params)
        # github, insta, addr 값이 추가되면 need_refresh 값을 1로 세팅 --> 윈도우 Reload 하게 함
        need_refresh = 0 if session['profile'][3] and session['profile'][4] and session['profile'][5] else 1
        profile = [email, image, state_msg, github, insta, addr]
        session['profile'] = profile
        profile.append(session['uid'])
        profile.append(mtime)
        profile.append(need_refresh)
        return json.dumps(profile)
####################################################################################################

@app.route('/')
def home():
    menu = {'ho':1, 'us':0, 'cr':0, 'ma':0, 'cb':0, 'sc':0}
    # flash('Welcome to my Web!!!')
    return render_template('home.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)

############################ 영수증 데이터 불러오기 ############################################


@chatbot_bp.route('/receipt', methods=['GET', 'POST'])
def receipt():
    if request.method == 'GET':
        return render_template('receipt.html')
    else:
        if 'image' not in request.files:
            return jsonify({'message': '이미지가 없습니다.'}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({'message': '이미지 파일을 선택하세요.'}), 400

        if file:
            file.save(os.path.join(
                chatbot_bp.config['UPLOAD_FOLDER'], "receipt01.jpg"))

            receipt_data = tess.get_item_from_img()
            result = rece.receipt_get_point(receipt_data)

            return str(result)

# 23.10.24
# 품목명(titleInput)을 입력받아 품목별 포인트를 리턴


@chatbot_bp.route('/receipt2', methods=['POST'])
def receipt2():
    user_input = request.form['userInput']
    result = item.get_title_market(user_input)
    return json.dumps(result)

# 23.10.25
# 주소(AddrInput)를 입력받아 해당 주소 근처에 있는 매장 리턴


@chatbot_bp.route('/receipt3', methods=['POST'])
def receipt3():
    addr_input = request.form['addrInput']
    result = item.get_market_info(addr_input)
    # Send this json_data as a response to your AJAX request
    return json.dumps(result)


########################################################################################################
   



""" ############################ 영수증 데이터 불러오기 ############################################

@app.route('/receipt', methods=['GET', 'POST'])
def receipt():
    if request.method == 'GET':
        return render_template('receipt.html')
    else:
        if 'image' not in request.files:
            return jsonify({'message': '이미지가 없습니다.'}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({'message': '이미지 파일을 선택하세요.'}), 400

        if file:
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], "receipt01.jpg"))

            receipt_data = tess.get_item_from_img()
            result = rece.receipt_get_point(receipt_data)

            return str(result)


@app.route('/receipt2', methods=['POST'])
def receipt2():
    user_input = request.form['userInput']
    result = item.get_title_market(user_input)
    return json.dumps(result)

########################################################################################################
 """