import contextlib


@contextlib.contextmanager
def myYieldTest():
    ok = "test"
    print("准备")
    try:
        yield ok
    except BaseException:
        print("失败")
    else:
        print("结束")

if __name__ == '__main__':
    with myYieldTest() as t:
        print(t)
"""
-rwxrwxrwx   1 owner    group    345722336 Sep 03 12:31 doodle.exe\r\n
drwxrwxrwx   1 owner    group        4096 Sep 03 12:26 doodle_tray\r\n
-rw-rw-rw-   1 owner    group       39558 Aug 03 12:13 key.jpg\r\n
-rw-rw-rw-   1 owner    group         356 Aug 03 12:15 key.txt\r\n
-rw-rw-rw-   1 owner    group    21433958 Aug 03 12:11 v2rayN.zip\r\n

"""