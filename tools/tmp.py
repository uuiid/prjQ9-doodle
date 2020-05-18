import script.MySqlComm

sql_com = """select table_name from information_schema.tables where table_schema='changanhuanjie'"""
tables = script.MySqlComm.selsctCommMysql("changanhuanjie", "", "", sql_command=sql_com)
tables = [t[0] for t in tables]
for table in tables:
    if table in ['configure', "mainshot"]:
        continue
    sql_com = f"""ALTER TABLE `{table}` ADD filestate varchar (64)"""
    script.MySqlComm.inserteCommMysql("changanhuanjie", "", "", sql_command=sql_com)
