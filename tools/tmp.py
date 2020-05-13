import script.MySqlComm

sql_com = """select table_name from information_schema.tables where table_schema='dubuxiaoyao'"""
tables = script.MySqlComm.selsctCommMysql("dubuxiaoyao", "", "", sql_command=sql_com)
tables = [t[0] for t in tables]
for table in tables:
    if table in ['configure', "mainshot"]:
        continue
    sql_com = f"""ALTER TABLE `{table}` DROP COLUMN problem"""
    script.MySqlComm.inserteCommMysql("dubuxiaoyao", "", "", sql_command=sql_com)
