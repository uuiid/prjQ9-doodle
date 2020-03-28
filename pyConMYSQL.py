import mysql.connector

bd = mysql.connector.connect(
    host='192.168.10.226',
    port='3306',
    user='texiao',
    passwd="texiao",
    auth_plugin='caching_sha2_password'
)
cursor = bd.cursor()

sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""
cursor.execute(sql)
# cursor.execute('SHOW DATABASES')
# databases = cursor.fetchall()
#
# print(databases)
#
# for i in databases:
#     print(i)

