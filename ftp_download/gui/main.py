import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

from ftp_download.gui.Ftp_downloads_gui import FtpDownloads


def init_config():
    settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
    settings.setIniCodec('UTF-8')  # 方法2：使用注册表
    settings.setValue("paramsnum", '0')

if __name__=='__main__':
    #init_config()
    app = QtWidgets.QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    widget = FtpDownloads()
    widget.show()
    sys.exit(app.exec_())