import sqlite3 as sq

def get_sched(sid):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()

    sql = 'select * from schedule where sid=?'
    cur.execute(sql, (sid,))
    row = cur.fetchone()

    cur.close()
    conn.close()
    return row

def get_sched_list(params):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()

    sql = 'select * from schedule where uid=? and sdate=? order by start_time'
    cur.execute(sql, params)        # (uid, sdate)
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

def insert_sched(params):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()

    sql = 'insert into schedule(uid, sdate, title, place, start_time, end_time, is_important, memo) values(?, ?, ?, ?, ?, ?, ?, ?)'
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()

def update_sched(params):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()

    sql = 'update schedule set uid=?, sdate=?, title=?, place=?, start_time=?, end_time=?, is_important=?, memo=? where sid=?'
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()

def delete_sched(sid):
    conn = sq.connect('./db_sqlite/test.db')
    cur = conn.cursor()

    sql = 'delete from schedule where sid=?'
    cur.execute(sql, (sid,))
    conn.commit()

    cur.close()
    conn.close()