import mysql.connector


def inserteCommMysql(mybd: str, departmen, password, sql_command):
    data_base = mysql.connector.connect(
        host='192.168.10.213',
        port='3306',
        user='Effects',
        passwd="Effects",
        auth_plugin='caching_sha2_password',
        db=mybd
    )
    cursor = data_base.cursor()
    try:
        cursor.execute(sql_command)
        data_base.commit()
    except:
        data_base.rollback()
    data_base.close()


def selsctCommMysql(mybd: str, departmen, password, sql_command):
    data_base = mysql.connector.connect(
        host='192.168.10.213',
        port='3306',
        user='Effects',
        passwd="Effects",
        auth_plugin='caching_sha2_password',
        db=mybd
    )
    cursor = data_base.cursor()
    try:
        cursor.execute(sql_command)
        date = cursor.fetchall()
    except:
        None
    data_base.close()
    return date

# def inserteMysql(mybd: str,department:str,**args):
#     my_sql_db = commMysql(mybd,department)
#     sql = """"""
