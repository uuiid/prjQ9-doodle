import mysql.connector

bd = mysql.connector.connect(
    host='192.168.10.213',
    port='3306',
    user='Effects',
    passwd="Effects",
    auth_plugin='caching_sha2_password',
    db='dubuxiaoyao'
)
# db='testdb'
cursor = bd.cursor()

sql="""
    insert into mainshot(episods)
    values ({})""".format(1)
try:
    cursor.execute(sql)
    bd.commit()
except:
    bd.rollback()
bd.close()