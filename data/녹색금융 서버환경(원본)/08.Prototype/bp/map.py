from flask import Blueprint, render_template, current_app, request
import util.map_util as mu


map_bp = Blueprint('map_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':0, 'ma':1,'cb':0, 'sc':0}

@map_bp.route('/station', methods=['GET','POST'])
def station():
    if request.method == 'GET':
        return render_template('/map/station_form.html' ,menu=menu)
    else:
        stations = request.form.getlist('station')
        stations = [station for station in stations if len(station.strip()) != 0]
        mu.get_station_map(current_app.root_path, stations)     # static/img/station_map.html 파일
        return render_template('/map/station_res.html', menu=menu)

@map_bp.route('/cctv')
def cctv():
    mu.get_cctv(current_app.static_folder)      # static/img/cctv.html 파일
    return render_template('/map/cctv.html')

@map_bp.route('/cctv_pop', methods=['GET','POST'])
def cctv_pop():
    if request.method == 'GET':
        columns = ['CCTV댓수','최근증가율','인구수','내국인','외국인','고령자','외국인 비율','고령자 비율']
        colormaps = ['RdPu','Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd',  'BuPu',
                        'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
        return render_template('/map/cctv_pop_form.html', columns=columns, colormaps=colormaps, menu=menu)
    else:
        column = request.form['column']
        colormap = request.form['colormap']
        mu.get_cctv_pop(current_app.static_folder, column, colormap)    # static/img/cctv_pop.html 파일
        return render_template('/map/cctv_pop_res.html', column=column, colormap=colormap, menu=menu)
    