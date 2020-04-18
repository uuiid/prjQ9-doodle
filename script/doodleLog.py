# import logging
import logging.config
import pathlib


def get_logger(name='root'):
    config_log = pathlib.Path.cwd()
    config_log = Lookingconfig(config_log).joinpath('doodleLogConfig.ini')
    logging.config.fileConfig(config_log)
    return logging.getLogger(name)


def Lookingconfig(paths: pathlib.Path):
    for path in paths.iterdir():
        if path.stem == 'config':
            return path
    return Lookingconfig(paths.parent)


ta_log = get_logger(__name__)
if __name__ == '__main__':
    print('asdsa{}',1111111)
