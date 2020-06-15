import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.sql

import script.MySqlComm
import script.ormClass

sql = script.MySqlComm.commMysql("test_db", "", "")
# dbxy = script.MySqlComm.commMysql("dubuxiaoyao", "", "")


# script.MySqlComm.Base.metadata.create_all(sql.engine)


def run():
    getsps = """SELECT episodes from mainshot"""
    eps = script.MySqlComm.selsctCommMysql("dubuxiaoyao", "", "", getsps)
    for ep in eps:
        ep_obj = script.ormClass.Episodes(episodes=1)
        sql_shots = f"""SELECT shot,shotab FROM `ep{ep[0]:0>3d}`"""
        for shot in script.MySqlComm.selsctCommMysql("dubuxiaoyao", "", "", sql_shots):
            shot_obj = script.ormClass.Shot(shot_=shot[0],shotab=shot[1])
            ep_obj.addShot.append(shot_obj)



if __name__ == '__main__':
    print("y")
    run()
    test_obj = script.ormClass.assUEScane(file="",fileSuffixes="",user="",version=0,filepath="",infor="",filestate="",)
    # script.MySqlComm.Base.metadata.create_all(sql.engine)
