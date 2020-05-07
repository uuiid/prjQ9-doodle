# import script.MySqlComm
# data = 'dubuxiaoyao'
# for i in range(1,13):
#     create_date ="""alter table `ep{:0>3d}`
# add column `infor` varchar(4096) ,
# add column `filetime` datetime default current_timestamp on update current_timestamp """.format(i)
#     script.MySqlComm.inserteCommMysql(data, '', '', create_date)
# import script.doodleLog
#
# ta_log = script.doodleLog.ta_log
#
#
# @script.doodleLog.errorDecorator(ta_log)
# def zero_divide():
#     taa = {}
#     print(taa['da'])
#
# if __name__ == '__main__':
#     zero_divide()

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import script.MySqlComm

base = sqlalchemy.ext.declarative.declarative_base()
Base = sqlalchemy.ext.declarative.declarative_base()


class mytest(base):
    __tablename__ = "mainshot"
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True)
    episodes: int = sqlalchemy.Column(sqlalchemy.SMALLINT)
    test: int = sqlalchemy.Column(sqlalchemy.SMALLINT)

    def getep(self, mysql_lib):
        eps = []
        ttest = "a"
        eng = script.MySqlComm.commMysql(mysql_lib)
        # eps = eng.session().query(self.episodes).all()
        # session: sqlalchemy.orm.session.Session = sqlalchemy.orm.sessionmaker(bind=eng.engine)()
        # eps = session.query(mytest.episodes).all()
        with eng.session() as session:
            eps = session.query(mytest.episodes).all()
            #     print(eps)
            ttest = "adsad"
        print(eps)
        print(ttest)


if __name__ == '__main__':
    t = mytest()
    # eng = script.MySqlComm.commMysql("dubuxiaoyao")
    # eps = eng.session().query(self.episodes).all()
    # engine = sqlalchemy.create_engine("mysql+mysqlconnector://Effects:Effects@192.168.10.213:3306/dubuxiaoyao",
    #                                   encoding='utf-8')
    # session: sqlalchemy.orm.session.Session = sqlalchemy.orm.sessionmaker(bind=eng.engine)()
    # eps = session.query(t.episodes).all()
    # print(eps)
    t.getep("dubuxiaoyao")
