import ftputil

def run():
    with ftputil.FTPHost("192.168.10.213","anonymous") as host:
        print(host.path.isfile("/MOD/072_YeYU)72_YeYu.fbx"))

if __name__ == '__main__':
    run()