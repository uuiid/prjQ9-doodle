class convertTool(object):
    def convert(self, my_dict: dict):
        self.__dict__.update(my_dict)
        for key, value in my_dict.items():
            if isinstance(value, dict):
                convert = convertTool()
                convert.convert(value)
                setattr(self, key, convert)
            elif isinstance(value,list):
                for index,sub in enumerate(value):
                    if isinstance(sub,dict):
                        value[index] = convertTool().convert(sub)
        return self


if __name__ == '__main__':
    mydirt = {"a": "aa", "bb": [{"b": 2, "c": "3"},"test"], "f": "aa"}
    test = convertTool().convert(mydirt)
    print(test.a)
    print(test.bb)
    print(test.bb[0].b)
    print(test.bb[0].c)
    print(test.f)
