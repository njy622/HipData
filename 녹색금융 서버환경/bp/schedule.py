from flask import Blueprint, request, render_template, session
from flask import redirect, flash
import json, calendar
from datetime import date, timedelta
import util.sched_util as su
import db_sqlite.anniversary_dao as adao
import db_sqlite.schedule_dao as sdao

schdedule_bp = Blueprint('schdedule_bp', __name__)
menu = {'ho':0, 'us':0, 'cr':0, 'ma':0, 'sc':1}

# 2023년 8월 1일로 가정
@schdedule_bp.route('/calendar/<arrow>')
def calendar_func(arrow):
    today = date.today()
    date_name = '월 화 수 목 금 토 일'.split()[today.weekday()]
    year = today.year
    month = today.month
    today = f'{year}-{month:02d}-{today.day:02d}({date_name})'
    try:
        _ = session['uid']
    except:
        flash('로그인을 먼저 하세요.')
        return redirect('/user/login')

    try: 
        _ = session['year']
        year = int(session['year'])
        month = int(session['month'])
    except:
        pass

    if arrow == 'left':
        month -= 1
        if month == 0:
            year, month = year - 1, 12
    elif arrow == 'right':
        month += 1
        if month == 13:
            year, month = year + 1, 1
    elif arrow == 'left2':
        year -= 1
    elif arrow == 'right2':
        year += 1
    session['year'] = str(year)
    session['month'] = str(month)

    first_day = date(year, month, 1)
    first_date = first_day.weekday()
    last_day = calendar.monthrange(year, month)[1]
    last_date = date(year, month, last_day).weekday()

    schedule_month = []
    number_of_weeks = 0
    # 첫번째 주
    week = []
    if first_date != 6:     # 30일, 31일 가져옴.
        prev_sunday = first_day - timedelta(days=(first_date+1)%7)      # 월요일이 0
        for i in range(first_date+1):       # 2023년 8월 경우 0, 1이 됨.
            oneday = prev_sunday + timedelta(days=i)
            week.append(su.gen_schday(oneday, month, session['uid']))
    for k, i in enumerate(range((first_date + 1) % 7, 7)):      # i : 1일 화 1+1, 7, k : 0 ~ 4
        oneday = date(year, month, k+1)     # year, month 오늘날짜. 8월 1일로 가정.
        week.append(su.gen_schday(oneday, month, session['uid']))
    schedule_month.append(week)
    number_of_weeks += 1

    # 둘째 주 ~ 마지막 전 주
    day = 8 - (first_date+1) % 7        # 8월 1일 화 index 1 / 8 - (1+1)%7
    duration = last_day - day + 1       # 8월 6일~31일 둘다 포함. + 1
    count = duration // 7
    for i in range(count):
        week = []
        for k in range(7):
            oneday = date(year, month, i*7+k+day)       # i : 주, k : 일, day : 두번째주 시작일
            week.append(su.gen_schday(oneday, month, session['uid']))
        schedule_month.append(week)         # [schedule_month[week{su.get_schday}]]
    number_of_weeks += count

    # 마지막 주
    if count * 7 + day <= last_day:
        start_day = count * 7 + day     # 3 * 7 + 6 = 27일
        week = []
        for i in range(7):
            oneday = date(year, month, start_day) + timedelta(days=i)
            week.append(su.gen_schday(oneday, month, session['uid']))
        schedule_month.append(week)
        number_of_weeks += 1

    time_list = su.gen_time()
    return render_template('schedule/calendar.html', menu=menu, 
                           today=today, year=year, month=f'{month:02d}', timeList=time_list,
                           schedule_month=schedule_month, number_of_weeks=number_of_weeks)

# Ajax로 클라이언트로부터 aid를 받아서, 상세 내용을 클라이언트에게 전달
@schdedule_bp.route('/detailAnniv/<aid>')
def detail_anniv(aid):
    anniv = adao.get_anniv(int(aid))        # db access하는 코드는 adao에 만듦.
    anniv_dict = {'aid':aid, 'aname':anniv[1], 'adate':anniv[2], 'isHoliday':anniv[3], 
                  'uid':anniv[4], 'suid':session['uid']}
    return json.dumps(anniv_dict)

@schdedule_bp.route('/insertAnniv', methods=['POST'])
def insert_anniv():
    aname = request.form['aname']
    anniv_date = request.form['annivDate'].replace('-','')
    try:
        _ = request.form['holiday']
        is_holiday = 1
    except:
        is_holiday = 0

    adao.insert_anniv((aname, anniv_date, is_holiday, session['uid']))
    return redirect('/schedule/calendar/this')

@schdedule_bp.route('/updateAnniv', methods=['POST'])
def update_anniv():
    try:
        _ = request.form['holiday']
        is_holiday = 1
    except:
        is_holiday = 0
    aid = request.form['aid']
    uid = request.form['uid']
    aname = request.form['aname']
    anniv_date = request.form['annivDate'].replace('-','')
    params = (aname, anniv_date, is_holiday, aid)
    if uid == session['uid']:
        adao.update_anniv(params)
    return redirect('/schedule/calendar/this')

@schdedule_bp.route('/deleteAnniv/<aid>/<uid>')
def delete_anniv(aid, uid):
    print('delete_anniv():', uid)
    if uid == session['uid']:
        adao.delete_anniv(int(aid))
    return redirect('/schedule/calendar/this')

# Ajax로 클라이언트로부터 sid를 받아서, 상세 내용을 클라이언트에게 전달
@schdedule_bp.route('/detail/<sid>')
def detail(sid):
    sched = sdao.get_sched(int(sid))
    day = f'{sched[2][:4]}-{sched[2][4:6]}-{sched[2][6:]} '
    sched_dict = {'sid':sid, 'title':sched[3], 'place':sched[4],
                  'startTime':day+sched[5], 'endTime':day+sched[6], 
                  'isImportant':sched[7], 'memo':sched[8]}
    return json.dumps(sched_dict)       # onclick="schedClick({{sched[0]}}) > calender.js

@schdedule_bp.route('/insert', methods=['POST'])
def insert():
    try:
        _ = request.form['importance']
        is_important = 1
    except:
        is_important = 0
    title = request.form['title']
    sdate = request.form['startDate'].replace('-','')
    start_time = request.form['startTime']
    end_time = request.form['endTime']
    place = request.form['place']
    memo = request.form['memo']
    uid = session['uid']
    params = (uid, sdate, title, place, start_time, end_time, is_important, memo)
    sdao.insert_sched(params)
    return redirect('/schedule/calendar/this')

@schdedule_bp.route('/update', methods=['POST'])
def update():
    try:
        _ = request.form['importance']
        is_important = 1
    except:
        is_important = 0
    sid = int(request.form['sid'])
    title = request.form['title']
    sdate = request.form['startDate'].replace('-','')
    start_time = request.form['startTime']
    end_time = request.form['endTime']
    place = request.form['place']
    memo = request.form['memo']
    uid = session['uid']
    params = (uid, sdate, title, place, start_time, end_time, is_important, memo, sid)
    sdao.update_sched(params)
    return redirect('/schedule/calendar/this')

@schdedule_bp.route('/delete/<sid>')
def delete(sid):
    sdao.delete_sched(int(sid))
    return redirect('/schedule/calendar/this')