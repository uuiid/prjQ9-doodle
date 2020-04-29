import pathlib
import script.MySqlComm


# # 定义类型检查
# def Typed(expected_type, cls=None):
#     if cls is None:
#         return lambda cls: Typed(expected_type, cls)
#     super_set = cls.__set__
#
#     def __set__(self, instance, value):
#         if not isinstance(value, expected_type):
#             raise TypeError('expected ' + str(expected_type))
#         super_set(self, instance, value)
#
#     cls.__set__ = __set__
#     return cls
#
#
# @Typed(int)
# class integer():
#     pass


class PrjCode():
    id: int  # = integer(int)
    mysqllib: str
    _root: pathlib.Path
    version: int

    def __init__(self, mysql_lib: str, sort_root: str, prj_root: str):
        """
        初始化一些属性
        :param mysql_lib: str
        :param sort_root: str
        :param prj_root: str
        """
        self._root = pathlib.Path(sort_root).joinpath(prj_root)
        self.mysqllib = mysql_lib

    def MysqlData(self, table_name="", modle="get", sort="", one=False, *query, **limit) -> list:
        """mysql命令,get需要query set不需要

        """
        data = self.mysqllib
        sql_com = ""
        file_data = [""]
        if modle in ["get", 'like']:
            _query = ','.join(query)
            sql_com = "SELECT DISTINCT {qu} FROM `{ta}` ".format(qu=_query, ta=table_name)

            if limit:
                _limit = " AND ".join(["{} = {}".format(key, value) if isinstance(value, int)
                                       else "{} = '{}'".format(key, value) for key, value in limit.items()])
                sql_com += " WHERE {}".format(_limit)
            # if modle == "like":
            #     pass
            if sort:
                sql_com += " ORDER BY {st}".format(st=sort)
            if one:
                sql_com += " LIMIT 1"
            file_data = script.MySqlComm.selsctCommMysql(data,
                                                         "",
                                                         "", sql_com)
        elif modle == "set":
            tmp = [[key, value] if isinstance(value, int) else [key, "'" + value + "'"] for key, value in limit.items()]
            _query = ','.join([i[0] for i in tmp])
            _limit = ",".join([str(i[1]) for i in tmp])

            sql_com = "INSERT INTO `{table}`({clume}) VALUE ({va})".format(table=table_name, clume=_query, va=_limit)

            file_data = script.MySqlComm.inserteCommMysql(data,
                                                          "self.setlocale.department",
                                                          "self.setlocale.department", sql_com)
        elif modle == "cre":
            pass
        elif modle == "updata":
            pass
        return file_data

    def submitInfo(self, filename: str, suffix: str, user: str, version: int, filepathAndname: str, infor=""):
        pass

    def getScreenshot(self):
        pass

    def getScreenshotPath(self):
        pass

    def getFileName(self, version: int, user_: str, suffix: str, prefix: str = "") -> str:
        pass

    def getFilePath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        pass

    def getMaxVersion(self) -> int:
        pass

    def queryFlipBook(self, ass_type: str) -> pathlib.Path:
        pass


class PrjShot(PrjCode):
    # <editor-fold desc="Description">
    episodes: int  # = integer(int)
    shot: int  # = integer(int)
    shotab: str
    department: str
    dep_type: str

    # </editor-fold>

    def getEpsodes(self) -> list:
        """
        获得镜头列表
        :return: list
        """
        eps = self.MysqlData("mainshot", "get", "", False, "id", "episods")
        return ['ep{:0>3d}'.format(ep[1]) for ep in eps]

    def getShot(self, sort: str = "shot") -> list:
        """
        获得shot列表
        :return: list
        """
        shots = self.MysqlData(f"ep{self.episodes:0>3d}", "get", sort, False, "shot", "shotab",
                               episodes=self.episodes)
        # item = []
        # for ep in shots:
        #     try:
        #         item.append('sc{:0>4d}{}'.format(ep[0], ep[1]))
        #     except:
        #         item.append('sc{:0>4d}'.format(ep[0]))
        return ['sc{:0>4d}'.format(shot[0]) if shot[1] == ''
                else 'sc{:0>4d}{}'.format(shot[0], shot[1]) for shot in shots]

    def getDepartment(self) -> list:
        """
        获得部门列表
        :return: lsit
        """
        deps = self.MysqlData(f"ep{self.episodes:0>3d}", "get", '', False, "department",
                              episodes=self.episodes, shot=self.shot, shotab=self.shotab)

        return [dep[0] for dep in deps]

    def getDepType(self) -> list:
        """
        获得部门类型列表
        :return: list
        """
        dep_types = self.MysqlData(f"ep{self.episodes:0>3d}", "get", '', False, "Type",
                                   episodes=self.episodes, shot=self.shot, shotab=self.shotab,
                                   department=self.department)
        return [dep_type[0] for dep_type in dep_types]

    def getFile(self) -> list:
        """
        获得文件信息(版本,评论,上传者,后缀,id)
        :return:
        """
        files = self.MysqlData(f"ep{self.episodes:0>3d}", "get", '', False, "version", " infor", " user",
                               " fileSuffixes", "id",
                               episodes=self.episodes, shot=self.shot, shotab=self.shotab,
                               department=self.department, Type=self.dep_type)
        return files

    def getFilePath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        path = self._root.joinpath(f'ep{self.episodes:0>3d}',
                                   f'sc{self.shot:0>4d}',
                                   folder_type,
                                   self.department,
                                   self.dep_type
                                   )
        return path

    def getFileName(self, version: int, user_: str, suffix: str, prefix: str = "") -> str:
        name = f"{prefix}shot_ep{self.episodes:0>3d}_sc{self.shot:0>4d}{self.shotab}_" \
               f"{self.department}" \
               f"{self.dep_type}_v{version:0>4d}" \
               f"__{user_}_{suffix}"
        return name

    def getMaxVersion(self) -> int:
        try:
            # 查不到会产生错误
            file_data = self.MysqlData(f"ep{self.episodes:0>3d}", "get", 'version', True, "version",
                                       episodes=self.episodes, shot=self.shot, shotab=self.shotab,
                                       department=self.department, Type=self.dep_type)
            # 查到为空也会出错
            version_max: int = int(file_data[0][0])
            # 出错时直接返回 0
        except:
            version_max: int = 0
        return version_max

    def submitInfo(self, filename: str, suffix: str, user: str, version: int, filepathAndname: str, infor=""):
        """
        提交文件信息
        :param filename: str
        :param suffix:str
        :param user:str
        :param version:int
        :param filepathAndname:str
        :param infor: str
        :return:
        """
        if not isinstance(version, int):
            version = int(version)
        self.MysqlData(f"ep{self.episodes:0>3d}", "set", '', False,
                       episodes=self.episodes, shot=self.shot, shotab=self.shotab,
                       department=self.department, Type=self.dep_type,
                       file=filename, fileSuffixes=suffix, user=user,
                       version=version,
                       filepath=filepathAndname,
                       infor=infor)

    def subEpisodesInfo(self, episodes: int):
        create_date = f"""create table ep{episodes:0>3d}(
                      id smallint primary key not null auto_increment,
                      episodes smallint,
                      shot smallint,
                      shotab varchar(8),
                      department varchar(128),
                      Type varchar(128),
                      file varchar(128),
                      fileSuffixes varchar(32),
                      user varchar(128),
                      version smallint,
                      filepath varchar(1024),
                      itfor varchar(4096),
                      filetime datetime default current_timestamp on update current_timestamp not null 
                      );"""
        create_date_insert = f"""insert into mainshot(episods)
                                                        value ({episodes})"""
        script.MySqlComm.inserteCommMysql(self.mysqllib, '', '', create_date)
        script.MySqlComm.inserteCommMysql(self.mysqllib, '', '',
                                          create_date_insert)

    def queryFileName(self, query_id: int) -> pathlib.Path:
        file_data = self.MysqlData(f"ep{self.episodes:0>3d}", "get", '', True, "filepath",
                                   id=query_id)
        try:
            file_data = file_data[0][0]
        except:
            file_data = ""
        return pathlib.Path(file_data)

    def getScreenshot(self) -> pathlib.Path:
        path: pathlib.Path = self._root.joinpath(f'ep{self.episodes:0>3d}',
                                                 f'sc{self.shot:0>4d}{self.shotab}',
                                                 'Playblasts',
                                                 self.department,
                                                 self.dep_type,
                                                 "Screenshot",
                                                 f"ep{self.episodes:0>3d}_sc{self.shot:0>4d}{self.shotab}.jpg"
                                                 )
        return path

    def getScreenshotPath(self) -> pathlib.Path:
        file_data = self.MysqlData(f"ep{self.episodes:0>3d}", "get", '', True, 'filepath',
                                   episodes=self.episodes, shot=self.shot, shotab=self.shotab,
                                   department=self.department, Type=self.dep_type,
                                   fileSuffixes='.jpg')
        try:
            file_data = pathlib.Path(file_data[0][0])
        except:
            file_data = pathlib.Path("")
        return file_data

    def queryFlipBook(self, ass_type: str) -> pathlib.Path:
        path = self.MysqlData(f"ep{self.episodes:0>3d}", "get", 'filetime', True, "filepath",
                              episodes=self.episodes, shot=self.shot, shotab=self.shotab,
                              department=self.department, Type=ass_type, fileSuffixes='.mp4')
        try:
            path = pathlib.Path(path[0][0])
        except:
            path = pathlib.Path("")
        return path

    def queryFlipBookShot(self, shot: int) -> pathlib.Path:
        path = self.MysqlData(f"ep{self.episodes:0>3d}", "get", 'filetime', True, "filepath",
                              episodes=self.episodes, shot=shot, fileSuffixes='.mp4')
        try:
            path = pathlib.Path(path[0][0])
        except:
            path = pathlib.Path("")
        return path


class PrjAss(PrjCode):
    sort: str
    ass_class: str
    ass_type: str

    def getAssClass(self) -> list:
        """
        获得资产类型
        :return: list
        """
        datas = self.MysqlData(self.sort, "get", '', False, "name")
        return [data[0] for data in datas]

    def getAssType(self) -> list:
        """
        获得资产类型细分
        :return:
        """
        datas = self.MysqlData(self.sort, "get", '', False, "type", name=self.ass_class)
        return [data[0] for data in datas]

    def getFileInfo(self) -> list:
        """
        获得文件信息(版本,评论,制作人,后缀)
        :return:
        """
        file_data = self.MysqlData(self.sort, "get", '', False, "version", "infor", "user", "fileSuffixes",
                                   "id", name=self.ass_class, type=self.ass_type)
        return file_data

    def getFilePath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        path = self._root.joinpath(self.sort,
                                   self.ass_class,
                                   folder_type,
                                   self.ass_type
                                   )
        return path

    def getFileName(self, version: int, user_: str, suffix: str, prefix: str = "") -> str:
        add_suffix = ""
        if self.ass_type in ["rig"]:
            add_suffix = "_rig"
        name = "{prefix}{cl}{su}{suffix}".format(cl=self.ass_class, su=add_suffix,
                                                 suffix=suffix, prefix=prefix)
        return name

    def getMaxVersion(self) -> int:
        file_data = self.MysqlData(self.sort, "get", "version", True, "version",
                                   name=self.ass_class, type=self.ass_type)
        if file_data:
            version_max: int = int(file_data[0][0])
        else:
            version_max: int = 0
        return version_max

    def submitInfo(self, file_name: str, suffix: str, user: str, version: int,
                   filepath_and_name: str, infor: str = ""):
        self.MysqlData(self.sort, "set", '', False,
                       name=self.ass_class, type=self.ass_type,
                       file=file_name, fileSuffixes=suffix,
                       user=user, version=version, infor=infor,
                       filepath=filepath_and_name)

    def queryFileName(self, id: int) -> pathlib.Path:
        file_data = self.MysqlData(self.sort, "get", '', True, "filepath",
                                   id=id)
        try:
            file_data = file_data[0][0]
        except:
            file_data = ""
        return pathlib.Path(file_data)

    def getScreenshot(self) -> pathlib.Path:
        path: pathlib.Path = self._root.joinpath(self.sort,
                                                 self.ass_class,
                                                 'Playblasts',
                                                 self.ass_type,
                                                 "Screenshot",
                                                 f"{self.ass_class}_{self.ass_type}.jpg"
                                                 )
        return path

    def getScreenshotPath(self) -> pathlib.Path:
        file_data = self.MysqlData(self.sort, "get", '', True, 'filepath',
                                   name=self.ass_class, type=self.ass_type,
                                   fileSuffixes='.jpg')
        try:
            file_data = pathlib.Path(file_data[0][0])
        except:
            file_data = pathlib.Path("")
        return file_data

    def queryFlipBook(self, ass_type: str) -> pathlib.Path:
        path = self.MysqlData(self.sort, "get", "filetime", True, "filepath",
                              name=self.ass_class, type=ass_type,
                              fileSuffixes=".mp4")
        try:
            path = pathlib.Path(path[0][0])
        except:
            path = pathlib.Path("")
        return path
