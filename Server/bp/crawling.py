from flask import Blueprint, render_template, current_app, request, Flask
import util.crawl_util as cu
import pandas as pd



crawl_bp = Blueprint('crawl_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':1, 'ma':0,'cb':0,  'sc':0}


@crawl_bp.route('/bank')
def index():
    df = pd.read_csv('../data/ESG_은행상품(임베딩).csv')
    df.drop(columns='embedding', inplace=True)    
    return render_template('/crawling/bank.html', menu=menu, tables=[df.to_html(classes='data')], titles=df.columns.values)


@crawl_bp.route('/finance')
def finance():
    df = pd.read_csv('../data/증권사상품.csv')      
    df.drop(columns='Unnamed: 0', inplace=True)    
    return render_template('/crawling/finance.html', menu=menu, tables=[df.to_html(classes='data')], titles=df.columns.values)


@crawl_bp.route('/card')
def card():    
    df = pd.read_csv('../data/친환경 카드.csv') 
    return render_template('/crawling/card.html', menu=menu, tables=[df.to_html(classes='data')], titles=df.columns.values)


@crawl_bp.route('/public')
def public():    
    df = pd.read_csv('../data/공공기관.csv') 
    return render_template('/crawling/public.html', menu=menu, tables=[df.to_html(classes='data')], titles=df.columns.values)
