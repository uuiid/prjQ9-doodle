import sqlalchemy.orm

import DoodleServer
import shutil
import pathlib

# sqlBd = DoodleServer.DoodleSql.commMysql("dubuxiaoyao");
doodle_set = DoodleServer.DoodleSet.Doodlesetting()

copy_root = pathlib.Path("V:\\")


class con:
    sub_clss_add = []

    def __init__(self):
        self.log = ""

    def run(self):
        ass = DoodleServer.DoodleCore.PrjAss(doodle_set=doodle_set)
        file_classs = ass.queryAssClass()
        for file_class in file_classs:
            # 创建新的file_clas
            sub_file_class = DoodleServer.DoodleOrm.fileClass(file_class=file_class.file_class)
            self.sub_clss_add.append(sub_file_class)
            for file_ass_class in file_class.addass_class:
                # 创建新的ass_claa
                sub_file_ass_class = DoodleServer.DoodleOrm.assClass(file_name=file_ass_class.file_name,
                                                                     file_class=sub_file_class)
                for file_type in file_ass_class.addfileType:
                    # 创建新的 file_type
                    sub_file_type_class = DoodleServer.DoodleOrm.fileType(file_type=file_type.file_type,
                                                                          file_class=sub_file_class,
                                                                          ass_class=sub_file_ass_class)
                    ass.file_class = file_class
                    ass.ass_class = file_ass_class
                    ass.file_type = file_type
                    _file_ = file_type.addfileAttributeInfo[0]
                    _file_path = doodle_set.project.joinpath(_file_.file_path.parent)
                    _file_.file_path = ass.commPath()

                    if _file_path.is_dir():
                        sub_file = DoodleServer.DoodleOrm.fileAttributeInfo()
                        sub_file.file_path = ass.commPath().joinpath(_file_.file_path.name)
                        sub_file.user = _file_.user
                        sub_file.file = _file_.file
                        sub_file.version = _file_.version
                        sub_file.infor = _file_.infor
                        sub_file.file_class = sub_file_class
                        sub_file.ass_class = sub_file_ass_class
                        sub_file.file_type = sub_file_type_class
                        shutil.copytree(_file_path,copy_root.joinpath(ass.commPath()))
                    else:
                        self.log += "\n" + file_ass_class.file_name + ":\n" + _file_path.as_posix()
        pathlib.Path("D:\\log.txt").write_text(self.log)

    def subclass(self):
        com_lur = "mysql+mysqlconnector" \
                  "://{_departmen}:{_password}@" \
                  "192.168.10.213:3306/{_mybd}".format(_departmen="Effects", _password="Effects", _mybd="dubuxiaoyao3")
        engine = sqlalchemy.create_engine(com_lur, encoding='utf-8')
        tmp_session = sqlalchemy.orm.sessionmaker(bind=engine)
        sessionclass = sqlalchemy.orm.scoped_session(tmp_session)
        session: sqlalchemy.orm.session.Session = sessionclass()
        return session

    def sub(self):
        print("dsa")
        s = self.subclass()
        for i in self.sub_clss_add:
            s.add(i)
        s.commit()
        s.close()


if __name__ == '__main__':
    test = con()
    test.run()
    test.sub()
