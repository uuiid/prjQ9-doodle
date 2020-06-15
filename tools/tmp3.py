import re

from script.MySqlComm import *


def run(dubuxiaoyao, ):
    updata = []
    #     sql2 = """SELECT episodes from mainshot"""
    #
    #     eps = selsctCommMysql(dubuxiaoyao, "", "", sql2)
    #     for ep in eps:
    #         paths = selsctCommMysql(dubuxiaoyao, "", "", f"""SELECT id,filepath FROM `ep{ep[0]:0>3d}`""")
    #         for path in paths:
    #             updata.append([path[0], convertPath(path[1])])
    #         tmp = "\n".join([f"WHEN {i[0]} THEN '{i[1]}'" for i in updata])
    #         tmp2 = "WHERE id IN ({})".format(",".join([str(i[0]) for i in updata]))
    #         #         print(f"""UPDATE `ep{ep[0]:0>3d}`
    #         # SET file_type=CASE id
    #         # {tmp}
    #         # END
    #         # {tmp2}""")
    #         #         print("\n")
    #         inserteCommMysql(dubuxiaoyao, "", "", f"""UPDATE `ep{ep[0]:0>3d}`
    # set filepath=CASE id
    # {tmp}
    # END UPDATE test_db.filetype set file_type = "" WHERE id = 1;
    # {tmp2}""")

    for ass in ["character", "effects", "props", "scane"]:
        data = selsctCommMysql(dubuxiaoyao,"","",f"""SELECT id,filepath FROM `{ass}`""")
        for path in data:
            inserteCommMysql(dubuxiaoyao, "", "", f"""UPDATE `{ass}` SET filepath = '{convertPath(path[1])}' WHERE id={path[0]}""")




def convertPath(path):
    if re.findall("^//", path):
        path = path[16:]
    elif re.findall("^[A-Z]:", path):
        path = path[2:]
    else:
        path = path
    return path

if __name__ == '__main__':
    run("dubuxiaoyao")