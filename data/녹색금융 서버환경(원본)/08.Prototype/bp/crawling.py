from flask import Blueprint, render_template, current_app, request
import util.crawl_util as cu


crawl_bp = Blueprint('crawl_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':1, 'ma':0,'cb':0,  'sc':0}

@crawl_bp.route('/melon')
def melon():
    print(current_app.root_path)       #bp module에서는 app 대신에 current_app을 사용
    song_list = cu.get_melon_chart()
    return render_template('/crawling/melon.html', song_list=song_list, menu=menu)

@crawl_bp.route('/interpark')
def interpark():
    print(current_app.root_path)
    book_list = cu.get_bestseller()
    return render_template('/crawling/10.interpark.html', book_list=book_list, menu=menu)


@crawl_bp.route('/siksin08')
def siksin08(place):    
    rest_list = cu.get_restaurant_list(place)    
    return render_template('/crawling/08.siksin.html', rest_list=rest_list, menu=menu, place=place)


@crawl_bp.route('/siksin', methods=['GET','POST'])
def siksin():
    print(current_app.root_path)
    if request.method == 'GET':
        return render_template('/crawling/siksin.html', menu=menu)
    else:
        print(current_app.root_path)
        place = request.form['place']
        rest_list = cu.get_restaurant_list(place)        
        return render_template('/crawling/08.siksin.html', menu=menu, place=place, rest_list=rest_list)


