from datetime import date
import db_sqlite.anniversary_dao as adao
import db_sqlite.schedule_dao as sdao

# Generate schedule day
def gen_schday(d, session_month, session_uid):
    schday = {}
    schday['day'] = d.day      # 1 ~ 31
    schday['webDate'] = (d.weekday() + 1) % 7
    anniv_list = adao.get_anniv_list(d.strftime('%Y%m%d'), d.strftime('%Y%m%d'), session_uid)
    schday['isHoliday'] = 0
    for anniv in anniv_list:
        if anniv[3] == 1:
            schday['isHoliday'] = 1
            break
    schday['isOtherMonth'] = 1 if d.month != session_month else 0
    schday['sdate'] = d.strftime('%Y%m%d')
    schday['annivList'] = anniv_list
    sched_list = sdao.get_sched_list((session_uid, d.strftime('%Y%m%d')))
    schday['schedList'] = sched_list
    return schday

def gen_time():
    time_list = []
    for hour in range(0, 24):
        for minute in [0, 30]:
            time_list.append(f'{hour:02d}:{minute:02d}')
    return time_list
