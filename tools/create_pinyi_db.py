import re
import sqlite3
import pathlib


def run():
    sql = """INSERT INTO `pinyin`(znch, en) VALUES {};"""
    subInfo = []
    myFile = pathlib.Path(r"C:\Users\teXiao\Downloads\Compressed\cedict_1_0_ts_utf-8_mdbg\cedict_ts.u8")

    myre = re.compile(r"[\u4e00-\u9fa5]\s[\u4e00-\u9fa5]\s\[\w+\]")
    myre2 = re.compile(r"\w+")
    with myFile.open("r", encoding="utf-8") as opmyFile:
        for lin in opmyFile:
            subValue = myre.findall(lin)
            if subValue:
                subtmp = lin.split(" ")
                subInfo.append([subtmp[1], myre2.findall(subtmp[2])[0]])
    sql = sql.format(",".join(["('{}','{}')".format(i[0], i[1]) for i in subInfo]))
    conn = sqlite3.connect("D:/pinyin.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

    print("ok")


def createTable():
    sql = """CREATE TABLE IF NOT EXISTS pinyin (
    id integer primary key AUTOINCREMENT,
    znch text,
    en text
);"""
    sqlIndex = """CREATE INDEX _znch_ ON pinyin(znch);"""
    conn = sqlite3.connect("D:/pinyin.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.execute(sqlIndex)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    run()
