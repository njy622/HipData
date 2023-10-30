from flask import Flask, render_template, Blueprint

app = Flask(__name__)

green_service_bp = Blueprint('green_service_bp', __name__)

menu = {'ho':0, 'us':0, 'gr':1, 'cr':0, 'ma':0,'cb':0,  'sc':0}

@green_service_bp.route('/greenconsume')
def green_consume():
    return render_template('/greenservice/01.GreenConsume.html', menu=menu)

@green_service_bp.route('/publictransport')
def public_transport():
    return render_template('/greenservice/02.PublicTransport.html', menu=menu)

@green_service_bp.route('/energysaving')
def envergy_saving():
    return render_template('/greenservice/03.EnergySaving.html', menu=menu)

@green_service_bp.route('/publicbuilding')
def public_building():
    return render_template('/greenservice/04.PublicBuilding.html', menu=menu)