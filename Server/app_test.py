""" from flask import Flask, render_template, request, current_app
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import pandas as pd

app = Flask(__name__)


@app.before_first_request
def before_first_request():
    global model, wdf
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    filename = os.path.join(current_app.static_folder, 'core_data_mod.csv')
    wdf = pd.read_csv(filename)
    wdf.embedding = wdf.embedding.apply(json.loads)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
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


if __name__ == '__main__':
    app.run(debug=True)
 """