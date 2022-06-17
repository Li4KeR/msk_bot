import sqlite3
from datetime import datetime
from config import DataBase, log_path



"""Работа с бд"""
def ins_sql(pacid, fio, phone, doc, dtime, comm, spek, date_cr, accepted):
    try:
        conn = sqlite3.connect(DataBase)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS blog_telegram(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pacid INT,
                    fio TEXT,
                    phone TEXT,
                    doc TEXT,
                    dtime TEXT,
                    comm TEXT,
                    spek TEXT,
                    date_cr TEXT,
                    accepted BOOLEAN,
                    acc_time TEXT);
                     """)
        sql = """INSERT INTO blog_telegram(pacid, fio, phone, doc, dtime, comm, spek, date_cr, accepted) 
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        param = (pacid, fio, phone, doc, dtime, comm, spek, date_cr, accepted)
        cursor.execute(sql, param)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        f = open(log_path,'w')
        f.write(str(error_text))


def update_acc_sql(pacid, dtime, acc_time):
    try:
        conn = sqlite3.connect(DataBase)
        cursor = conn.cursor()
        sql = """UPDATE blog_telegram SET accepted = 1, acc_time = ? WHERE pacid = ? AND dtime = ?"""
        param = acc_time, pacid, dtime
        cursor.execute(sql, param)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        f = open(log_path,'w')
        f.write(str(error_text))

def info_acc_sql(pacid, dtime):
    try:
        conn = sqlite3.connect(DataBase)
        cursor = conn.cursor()
        sql = """select * from blog_telegram where accepted = 1 and pacid = ? and dtime = ?"""
        param = pacid, dtime
        data = cursor.execute(sql, param)
        for row in data:
            fio = row[2]
            phone = row[3]
            doc = row[4]
            date_pr = row[5]
        cursor.close()
        return fio, phone, doc, date_pr
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        f = open(log_path,'w')
        f.write(str(error_text))

def all_treat_pac(tele_id):
    date_now = datetime.today().strftime('%d.%m')
    try:
        conn = sqlite3.connect(DataBase)
        cursor = conn.cursor()
        sql = """select * from blog_telegram where pacid = ?"""
        param = (tele_id,)
        data = cursor.execute(sql, param)
        all_tr = []
        for row in data:
            if row[5].split(' ')[0] > date_now:
                id_treat = row[0]
                doc = row[4]
                data_threat = (id_treat, doc)
                all_tr.append(data_threat)
        cursor.close()
        return all_tr
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        f = open(log_path,'w')
        f.write(str(error_text))

def custom_treat(id_treat):
    try:
        conn = sqlite3.connect(DataBase)
        cursor = conn.cursor()
        sql = """select * from blog_telegram where id = ?"""
        param = (id_treat,)
        data = cursor.execute(sql, param)
        for row in data:
            doc = row[4]
            tr_date = row[5]
            spek = row[7]
        cursor.close()
        return doc, tr_date, spek
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        f = open(log_path,'w')
        f.write(str(error_text))
