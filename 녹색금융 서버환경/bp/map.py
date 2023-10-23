from flask import Blueprint, current_app, render_template, request
import util.map_util as mu
import json

map_bp = Blueprint('map_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':0, 'ma':1, 'sc':0}

@map_bp.route('/station', methods=['GET','POST'])
def station():
    if request.method == 'GET':
        return render_template('map/station_form.html', menu=menu)
    else:
        stations = []
        for i in range(1, 6):
            stations.append(request.values[f'station{i}'])
        # stations = request.values.getlist('station_list')      # input name="station"으로 받아오면 리스트로 받음.
        stations = [station for station in stations if len(station.strip()) != 0]
        mu.get_station_map(current_app.root_path, stations)     # static/img/station_map.html 파일에 저장
        result = mu.show_station_map()
        return result
        # return render_template('map/station_res.html', menu=menu)

@map_bp.route('/cctv_pop', methods=['GET','POST'])
def cctv_pop():
    if request.method == 'GET':
        columns = ['CCTV댓수', '최근증가율', '인구수', '내국인', '외국인', '고령자', '외국인 비율',	'고령자 비율']
        colormaps = ['RdPu', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
        return render_template('map/cctv_pop_form.html', columns=columns, colormaps=colormaps, menu=menu)
    else:
        column = request.values['column']
        colormap = request.values['colormap']
        mu.get_cctv_pop(current_app.static_folder, column, colormap)    # static/img/cctv_pop.html 파일
        result = mu.show_cctv_pop(colormap)
        return result