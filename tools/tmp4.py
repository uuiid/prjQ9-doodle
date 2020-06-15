import ffmpeg
import difflib
import pathlib
import re

def run(path: pathlib.Path):
    my_list = [p.name for p in path.iterdir()]
    my_list = [re.findall("\d*",i) for i in my_list[:]]
    print("\n".join(my_list))


if __name__ == '__main__':
    path = pathlib.Path("D:/shot/Ep007")
    run(path)
