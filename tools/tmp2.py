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
