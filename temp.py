import pathlib
import subprocess
import time
# import script.doodlePlayer
# if __name__ == '__main__':
#     in_filename = pathlib.Path(r'D:\EP01_4.3.mp4')
#     file = pathlib.Path(r"D:\test\EP01_.png")
#     test = script.doodlePlayer.videoConvert(in_filename, file)
#     lll_std = test.videoToImage()
#     print(lll_std)
path = pathlib.Path(r"D:\image")
image = [str(i) for i in path.iterdir()]
# image = "D:/image/ep010_sc0001_VFX_test_zhang-yu-bin.0159.png"
djv = subprocess.Popen(['tools/bin/ffplay.exe',
                        "-i","-",
                        ],stdin=subprocess.PIPE,bufsize=10**8,universal_newlines=True)
ssss= " ".join(image)
djv.stdin.write(ssss)
# for image in path.iterdir():
#     data = image.read_bytes()
#     print(data)
#     djv.communicate(data)
#     time.sleep(0.04)
image = pathlib.Path(image)