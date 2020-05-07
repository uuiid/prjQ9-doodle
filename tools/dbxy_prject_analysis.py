import pathlib

import script.ProjectAnalysis.DBXYPathAnalysis

import script.MySqlComm

shot = pathlib.Path(r"W:\03_Workflow\Shots")
data = 'dubuxiaoyao'

def shotScan(episods):
    episods = episods
    paths = pathlib.Path(r"W:\03_Workflow\Shots")

    mitem = []
    for path in paths.iterdir():
        if path.match('{}*'.format(episods)):
            try:
                mitem.append(path.stem.split('-')[1])
            except:
                pass
    mitem = list(set(mitem))
    mitem.sort()
    mitem = filter(None, mitem)
    suffix = ''
    shotab = ''
    for itoa in mitem:
        try:
            shot = itoa[2:]
            try:
                shot = int(shot)
            except:
                try:
                    shot = int(shot[:-1])
                    shotab = shot[-1]
                except:
                    shot = ''
        except:
            break
        print(shot,shotab)
        if shot or shotab:
            epsh = paths.joinpath('{}-sc{:0>4d}{}'.format(episods,shot,shotab),'Scenefiles','anm','Animation')
            if epsh.is_dir():
                for file in epsh.iterdir():
                    if file.suffix in ['.ma','.mb']:
                        try:
                            filename = file.stem
                            suffix = file.suffix
                            version =int(filename.split('_')[4][1:])
                            user = filename.split('_')[-2]
                            file_path = file.as_posix()
                        except:
                            pass
                        else:
                            print(int(episods[2:]),shot,shotab,'anm','Animation',filename,suffix,user,file_path)
                            create_date = """insert into ep{:0>3d}(episodes, shot, shotab, department, Type, file, fileSuffixes, user, version, filepath) 
                            VALUE ({},{},'{}','{}','{}','{}','{}','{}',{},'{}')""".format(int(episods[2:]),int(episods[2:]),shot,shotab,'anm','Animation',filename,suffix,user,version,file_path)
                            print(create_date)
                            script.MySqlComm.inserteCommMysql(data, '', '', create_date)

    return mitem


def getEp():
    sql = """select id,episods from mainshot"""
    data = 'dubuxiaoyao'
    eps = script.MySqlComm.selsctCommMysql(data,
                                           's',
                                           's', sql)
    item = []
    for ep in eps:
        if ep[1] == 0:
            item.append('pv')
        else:
            d__format = 'ep{:0>2d}'.format(ep[1])
            item.append(d__format)
            # create_date = """create table {}(
            #                               id smallint primary key not null auto_increment,
            #                               episodes smallint,
            #                               shot smallint,
            #                               department varchar(128),
            #                               Type varchar(128),
            #                               file varchar(128),
            #                               fileSuffixes varchar(32),
            #                               user varchar(128),
            #                               filepath varchar(1024)
            #                               );""".format(d__format)
            # script.MySqlComm.inserteCommMysql(data, '', '', create_date)
    return item


if __name__ == '__main__':
    for i in getEp():
        shotScan(i)
