from flask import Blueprint, render_template, current_app, request
import util.map_util as mu
import pandas as pd
from flask import Blueprint, render_template, request, current_app, jsonify
import json, os
import bardapi, openai
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


map_bp = Blueprint('map_bp', __name__)

menu = {'ho':0, 'us':0, 'gr':0, 'cr':0, 'ma':1,'cb':0,  'sc':0}

@map_bp.route('/public')
def public():    
    df = pd.read_csv(r'D:/IT 공부/Workspace/HipData/남지영/Server-test/static/data/공공기관.csv') 
    return render_template('/map/public.html', menu=menu, tables=[df.to_html(classes='data')], titles=df.columns.values)
