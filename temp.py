import pathlib

import script.doodlePlayer
if __name__ == '__main__':
    in_filename = pathlib.Path(r'D:\EP01_4.3.mp4')
    file = pathlib.Path(r"D:\test\EP01_.png")
    test = script.doodlePlayer.videoConvert(in_filename, file)
    lll_std = test.videoToImage()
    print(lll_std)