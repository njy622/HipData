import sqlite3

def get_chat_history(uid):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'select * from chat where uid=?'
    cur.execute(sql, (uid,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

def insert_chat(params):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'insert into chat(uid, u_question, c_answer, c_date) values(?, ?, ?, ?)'
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()

def delete_chat(uid):
    conn = sqlite3.connect('./db_sqlite/project.db')
    cur = conn.cursor()

    sql = 'delete from user where uid=?'
    cur.execute(sql, (uid,))
    conn.commit()

    cur.close()
    conn.close()