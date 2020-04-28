import pathlib
import script.MySqlComm
import script.doodle_setting


class PrjCode():
    id: int
    mysqllib: str
    _root: pathlib.Path
    version: str

    def __init__(self, mysql_lib: str, sort_root: str, prj_root: str):
        """
        初始化一些属性
        :param mysql_lib: str
        :param prj_root: pathlib.Path
        :param set:script.doodle_setting.Doodlesetting
        """
        self._root = pathlib.Path(sort_root).joinpath(prj_root)
        self.mysqllib = mysql_lib

    def MysqlData(self, table_name="", modle="get", sort="", one=False, *query, **limit) -> list:
        """mysql命令,get需要query set不需要

        """
        data = self.mysqllib
        sql_com = ""
        file_data = [""]
        if modle == "get":
            _query = ','.join(query)
            sql_com = "SELECT DISTINCT {qu} FROM `{ta}` ".format(qu=_query, ta=table_name)

            if limit:
                _limit = " AND ".join(["{} = {}".format(key, value) if isinstance(value, int)
                                       else "{} = '{}'".format(key, value) for key, value in limit.items()])
                sql_com += " WHERE {}".format(_limit)
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


class PrjShot(PrjCode):
    # <editor-fold desc="Description">
    episodes: int
    shot: int
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

    def getShot(self) -> list:
        """
        获得shot列表
        :return: list
        """
        shots = self.MysqlData(f"ep{self.episodes:0>3d}", "get", '', False, "shot", "shotab",
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

    def getDepTYpe(self) -> list:
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

    def getFilePath(self) -> pathlib.Path:
        path = self._root.joinpath(f'ep{self.episodes:0>3d}',
                                   f'sc{self.shot:0>4d}',
                                   'Scenefiles',
                                   self.department,
                                   self.dep_type
                                   )
        return path

    def getFileName(self,version:int,user_:str,suffix:str) -> str:
        name = f"shot_ep{self.episodes:0>3d}_sc{self.shot:0>4d}{self.shotab}_" \
                                         f"{self.department}" \
                                         f"{self.dep_type}_v{version:0>4d}" \
                                         f"__{user_}_{suffix}"
        return name


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

    def getFile(self) -> list:
        """
        获得文件信息(版本,评论,制作人,后缀)
        :return:
        """
        file_data = self.MysqlData(self.sort, "get", '', False, "version", "infor", "user", "fileSuffixes",
                                   "id", name=self.ass_class, type=self.ass_type)
        return file_data

    def getFilePath(self) -> pathlib.Path:
        path = self._root.joinpath(self.sort,
                                   self.ass_class,
                                   'Scenefiles',
                                   self.ass_type
                                   )
        return path

    def getFileName(self,suffix) -> pathlib.Path:
        if self.ass_type in ["rig"]:
            add_suffix = "_rig"
        name = "{cl}{su}".format(cl=self.ass_class,su=add_suffix)
        return name