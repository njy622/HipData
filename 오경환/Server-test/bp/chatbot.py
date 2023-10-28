from flask import Blueprint, render_template, request, current_app, jsonify, session
import json, os
import bardapi, openai
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
# tesseract
import util.tesseract_util as tess
# receipt
import util.receipt_util as rece
# item_analysis
import util.item_analysis as item
import db_sqlite.chat_dao as cdb


chatbot_bp = Blueprint('chatbot_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':0, 'ma':0, 'cb':1, 'sc':0}


#############################################녹색금융####################################################################
@chatbot_bp.before_app_first_request
def before_app_first_request():
    global model, wdf
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    filename = os.path.join(current_app.static_folder, 'core_data_mod.csv')
    wdf = pd.read_csv(filename)
    wdf.embedding = wdf.embedding.apply(json.loads)

@chatbot_bp.route('/counsel', methods=['GET','POST'])
def counsel():
    if request.method == 'GET':
        return render_template('chatbot/counsel.html', menu=menu)
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
    

###########################################이력DB저장##########################################
@chatbot_bp.route('/savedatatodb', methods=['POST'])
def save_data_to_db():
    current_date = request.form['currentDate']
    user_question = request.form['userQuestion']
    chatbot_answer = request.form['chatbotAnswer']
    uid = session['uid']
    params = (uid, user_question, chatbot_answer, current_date)
    cdb.insert_chat(params)
    return ' '

    
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
            file_path = os.path.join(current_app.static_folder, f'upload/{file.filename}')
            file.save(file_path)

            receipt_data = tess.get_item_from_img(file.filename)
            result = rece.receipt_get_point(receipt_data)

            return str(result)


@chatbot_bp.route('/receipt2', methods=['POST'])
def receipt2():
    user_input = request.form['userInput']
    result = item.get_title_market(user_input)
    return json.dumps(result)


########################################################################################################
   




        


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
 