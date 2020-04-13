import codecs
import pathlib


def debug(mystr: str):
    log = pathlib.Path("{}{}".format(pathlib.Path.home(), '\\Documents\\doodle\\log.txt'))
    try:
        pathlib.Path("{}{}".format(pathlib.Path.home(), '\\Documents\\doodle')).mkdir()
    except:
        pass
    pathlib.Path.touch(log)
    with codecs.open(log, mode='a', encoding="utf-8") as f:
        f.write(mystr + '\n')
    if log.stat().st_size > 1048576:
        log.unlink()
