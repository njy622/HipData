from flask import Blueprint, render_template, request, current_app, jsonify, session, flash, redirect
import json, os
import bardapi, openai
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import util.item_analysis as item
import db_sqlite.chat_dao as cdb

chatbot_bp = Blueprint('chatbot_bp', __name__)

menu = {'ho':0, 'us':0, 'gr':0, 'cr':0, 'ma':0,'cb':1,  'sc':0}


#############################################녹색금융####################################################################

from flask import Flask, render_template, request, current_app, jsonify
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import pandas as pd
# tesseract
import util.tesseract_util as tess
# receipt
import util.receipt_util as rece
# item_analysis
import util.item_analysis as item

@chatbot_bp.before_app_first_request
def before_first_request():
    global model, wdf
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    filename = os.path.join(current_app.static_folder, 'core_data_mod.csv')
    wdf = pd.read_csv(filename)
    wdf.embedding = wdf.embedding.apply(json.loads)


items_per_page = 5

@chatbot_bp.route('/counsel', methods=['GET', 'POST'])
def counsel():
    if request.method == 'GET':
        try:
            uid = session['uid']
        except:
            flash('로그인 해주세요')
            return redirect('/user/login')
        chat_history_ = cdb.get_chat_history_reverse(uid)
        chat_history = [ item[-1] for item in chat_history_[0:5] ]
        print(chat_history)
        return render_template('chatbot/counsel.html', menu=menu, chat_history=chat_history)
    else:
        user_input = request.form['userInput']
        embedding = model.encode(user_input)
        wdf['유사도'] = wdf.embedding.map(
            lambda x: cosine_similarity([embedding], [x]).squeeze())
        answer = wdf.loc[wdf.유사도.idxmax()]
        result = {
            'category': answer.구분, 'user': user_input, 'chatbot': answer.챗봇, 'similarity': answer.유사도
        }
        return json.dumps(result)

@chatbot_bp.route('/load_messages', methods=['POST'])
def load_messages():
    uid = session['uid']
    chat_history_ = cdb.get_chat_history_reverse(uid)
    page = int(request.form.get('page', 0))
    messages_per_page = 5
    start = page * messages_per_page
    end = (page + 1) * messages_per_page
    messages = [ item[-1] for item in chat_history_[start:end] ]
    return jsonify(messages=messages)

# 영수증 이미지 입력받아  포인트를 친환경 상품명과 리턴

@chatbot_bp.route('/receipt', methods=['GET', 'POST'])
def receipt():
    if request.method == 'GET':
        return render_template('chatbot/counsel.html')
    else:
        print('receipt() post')
        file_image = request.files['image']
        filename = os.path.join(current_app.static_folder, f'upload/{file_image.filename}')
        file_image.save(filename)
        print(f'{file_image.filename}')

        receipt_data = tess.get_item_from_img(f'{file_image.filename}')
        result = rece.receipt_get_point(receipt_data)

        return '<h5>친환경 상품(에코포인트) 내역</h5> <hr> '+str(result)+'를 적립 예상합니다.'

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
    print(addr_input)
    result = item.get_market_info(addr_input)
    print(result)
    # Send this json_data as a response to your AJAX request
    return json.dumps(result)


if __name__ == '__main__':
    chatbot_bp.run(debug=True)




###########################################이력DB저장##########################################
@chatbot_bp.route('/savedatatodb', methods=['POST'])
def save_data_to_db():
    current_date = request.form['currentDate']
    print(current_date)
    user_question = request.form['userQuestion']
    chatbot_answer = request.form['chatbotAnswer'].replace('<br>', '\n')
    origin_data = request.form['originData']
    uid = session['uid']
    params = (uid, user_question, chatbot_answer, current_date, origin_data)
    cdb.insert_chat(params)
    return ' '
    


    
##########################################################################################################



        


@chatbot_bp.route('/bard', methods=['GET','POST'])
def bard():
    if request.method == 'GET':
        return render_template('chatbot/bard.html', menu=menu)
    else:
        with open(os.path.join(current_app.static_folder, 'keys/bardApiKey.txt')) as file:
            os.environ['_BARD_API_KEY'] = file.read()
        user_input = request.form['userInput']
        response = bardapi.core.Bard().get_answer(user_input)
        result = {'user':user_input, 'chatbot':response['content']}
        return json.dumps(result)

@chatbot_bp.route('/genImg', methods=['GET','POST'])
def gen_img():
    if request.method == 'GET':
        return render_template('chatbot/genImg.html', menu=menu)
    else:
        with open(os.path.join(current_app.static_folder, 'keys/openAiApiKey.txt')) as file:
            openai.api_key = file.read()
        user_input = request.form['userInput'] 
        size = request.form['size']

        gpt_prompt = [
            {'role': 'system', 
             'content': 'Imagine the detail appearance of the input. Response it shortly around 20 English words.'},
            {'role': 'user', 'content': user_input}      
        ]
        gpt_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo', messages=gpt_prompt
        )
        prompt = gpt_response['choices'][0]['message']['content']
        dalle_response = openai.Image.create(
            prompt=prompt, size=size         # '1024x1024', '512x512', '256x256'
        )
        img_url = dalle_response['data'][0]['url']
        result = {'img_url':img_url, 'translated_text': prompt}
        return json.dumps(result) 
 