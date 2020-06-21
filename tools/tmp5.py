mydirt = {"a":"aa","bb":[{"b":2,"c":"3"},"d"],"f":"aa"}

class Mytest(object):
    def tomap(self,data):
        self.__dict__.update(data)


def run():
    t = Mytest()
    t.tomap(mydirt)
    print(t.a)
    print(t.bb)
    print(t.f)

if __name__ == '__main__':
    run()
