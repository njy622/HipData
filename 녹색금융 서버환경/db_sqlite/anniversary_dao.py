import sqlite3 as sq

def get_anniv(aid):
    conn = sq.connect('./db_sqlite/test.db')        # app.py 의 아래 폴더 ./
    cur = conn.cursor()

    sql = 'select * from anniversary where aid=?'
    cur.execute(sql, (aid, ))
    result = cur.fetchone()

    cur.close()
    conn.close()
    return result

# start date ~ end date, uid가 'admin' 또는 uid
def get_anniv_list(sdate, edate, uid):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()
    
    if uid == 'admin':
        sql = 'select * from anniversary where adate between ? and ? and uid=?'
    else:
        sql = "select * from anniversary where adate between ? and ? and (uid='admin' or uid=?)"
    cur.execute(sql, (sdate, edate, uid))
    results = cur.fetchall()

    cur.close()
    conn.close()
    return results


def insert_anniv(params):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()

    sql = 'insert into anniversary(aname, adate, is_holiday, uid) values(?, ?, ?, ?)'
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()

def insert_anniv_many(params_list):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()

    sql = 'insert into anniversary(aname, adate, is_holiday, uid) values(?, ?, ?, ?)'
    cur.executemany(sql, params_list)
    conn.commit()

    cur.close()
    conn.close()

def update_anniv(params):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()

    sql = 'update anniversary set aname=?, adate=?, is_holiday=? where aid=?'
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()

def delete_anniv(aid):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()

    sql = 'delete from anniversary where aid=?'
    cur.execute(sql, (aid, ))
    conn.commit()

    cur.close()
    conn.close()