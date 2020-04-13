import mysql.connector

bd = mysql.connector.connect(
    host='192.168.10.226',
    port='3306',
    user='texiao',
    passwd="texiao",
    auth_plugin='caching_sha2_password',
    db='testdb'
)
cursor = bd.cursor()

cursor.execute('CREATE DATABASE testdb')
cursor.execute('SHOW DATABASES')
cursor.execute('CREATE TABLE testdb (name VARCHAR(255), url VARCHAR(255))')
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""
# cursor.execute(sql)
cursor.execute('SHOW DATABASES')
databases = cursor.fetchall()

print(databases)

for i in cursor:
    print(i)

bd.close()
