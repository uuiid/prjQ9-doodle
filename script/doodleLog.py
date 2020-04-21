# import logging
import logging.config
import pathlib
import traceback
import functools
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

def erorrDecorator(function):

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        log = ta_log
        try:
            return function(*args, **kwargs)
        except BaseException as erroor:
            log.info('靠,有错(+_+)?===:%s %s', function.__name__, traceback.format_exc())
            # 重新引发异常
            raise

    return wrapper




@erorrDecorator
def zero_divide():
    taa = {}
    print(taa['das'])


if __name__ == '__main__':
    zero_divide()
