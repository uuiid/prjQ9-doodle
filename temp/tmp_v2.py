import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import queue     #如果不加载这个模板，pyinstaller打包后，可能无法运行requests模板
import requests
################################################


################################################
class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)

        # 增加进度条
        self.progressBar = QProgressBar(self, minimumWidth=400)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        # 增加下载按钮
        self.pushButton = QPushButton(self, minimumWidth=100)
        self.pushButton.setText("下载")
        layout.addWidget(self.pushButton)

        # 绑定按钮事件
        self.pushButton.clicked.connect(self.on_pushButton_clicked)




    # 下载按钮事件
    def on_pushButton_clicked(self):
        the_url = 'http://cdn2.ime.sogou.com/b24a8eb9f06d6bfc08c26f0670a1feca/5c9de72d/dl/index/1553820076/sogou_pinyin_93e.exe'
        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath ="D:/sogou_pinyin_93e.exe"
        the_fileobj = open(the_filepath, 'wb')
        #### 创建下载线程
        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()



    # 设置进度条
    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            QMessageBox.information(self, "提示", "下载成功！")
            return






##################################################################
#下载线程
##################################################################
class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)                        #创建信号

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer


    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)                #流下载模式
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)                            #设置指针位置
                self.fileobj.write(chunk)                            #写入文件
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))        #发送信号
            #######################################################################
            self.fileobj.close()    #关闭文件
            self.exit(0)            #关闭线程


        except Exception as e:
            print(e)





####################################
#程序入口
####################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
