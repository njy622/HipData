from flask import Flask, render_template, request, flash, session, current_app, jsonify
from bp.crawling import crawl_bp
from bp.user import user_bp
from bp.chatbot import chatbot_bp
import os, json, random
import util.image_util as iu
import db_sqlite.profile_dao as pdao
from bp.greenservice import green_service_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/receipts'
app.config['SESSION_COOKIE_PATH'] = '/'
app.secret_key = 'qwer1234'

app.register_blueprint(crawl_bp, url_prefix='/crawling')    # localhost:5000/crawling/* 는 crawl bp가 처리
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
# green_service를 nav_bar에 추가
app.register_blueprint(green_service_bp, url_prefix='/greenservice')

# for AJAX ###################################################



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


@app.route('/')
def home():
    menu = {'ho':1, 'us':0, 'gr':0, 'cr':0, 'ma':0,'cb':0,  'sc':0}
    # flash('Welcome to my Web!!!')
    return render_template('home.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)