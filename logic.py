import sqlite3
from config import DataBase, log_path



"""Работа с бд"""
def ins_sql(pacid, fio, phone, doc, dtime, comm, spek, date_cr, accepted):
    try:
        conn = sqlite3.connect(DataBase)
        cursor = conn.cursor()
        #cursor.execute("SELECT id, metro, kolvo FROM viezdi")
        cursor.execute("""CREATE TABLE IF NOT EXISTS blog_telegram(
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
        f.write(error_text)


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
        f.write(error_text)

def info_acc_sql(pacid, dtime):
    try:
        conn = sqlite3.connect(DataBase)
        cursor = conn.cursor()
        sql = """select * from blog_telegram where accepted = 1 and pacid = ? and dtime = ?"""
        param = pacid, dtime
        x = cursor.execute(sql, param)
        for row in x:
            fio = row[2]
            phone = row[3]
            doc = row[4]
            date_pr = row[5]
        cursor.close()
        return fio, phone, doc, date_pr
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        f = open(log_path,'w')
        f.write(error_text)