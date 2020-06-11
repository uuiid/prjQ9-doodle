import multiprocessing
import time
import ftputil


def run():
    with ftputil.FTPHost("192.168.10.213", "dubuxiaoyao", "12345") as host:
        if host.path.isfile("/run.bat"):
            host.makedirs("/tool/backup")
            host.rename("/tool/maya_VFX.exe","/tool/backup/maya_VFX.exe")


if __name__ == '__main__':
    run()
