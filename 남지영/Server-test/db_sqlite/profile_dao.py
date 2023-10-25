import sqlite3

def get_profile(email):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'select * from profile where email=?'
    cur.execute(sql, (email,))
    row = cur.fetchone()

    cur.close()
    conn.close()
    return row

def insert_profile(email):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'insert into profile(email) values(?)'
    cur.execute(sql, (email,))
    conn.commit()

    cur.close()
    conn.close()

def update_profile(params):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'update profile set image=?, stateMsg=?, github=?, insta=?, addr=? where email=?'
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()

def delete_profile(email):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'delete from profile where email=?'
    cur.execute(sql, (email,))
    conn.commit()

    cur.close()
    conn.close()