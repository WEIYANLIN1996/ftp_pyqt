

import os
import sys
import zipfile

from PyQt5.QtCore import QSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ftpclient.FtpClientOperation import FtpClient
from utils.StringUtils import isNull
import datetime

from ftp_download.version1.ftp_download import Ui_MainWindow


class Mainwindow:
    pass


class WindowRun(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(WindowRun, self).__init__()
        self.setupUi(self)
        self.init_ftp_info()
        self.pushButton.clicked.connect(self.connect_ftp)
        self.pushButton_4.clicked.connect(self.download_pack)



    def connect_ftp(self):
        print("---")
        self.save_ftp_info()
        addr = self.lineEdit_3.text();
        userName = self.lineEdit_2.text();
        password = self.lineEdit.text();
        port = self.lineEdit.text()
        print("地址:" + addr + ",用户名:" + userName + "," + password)
        if isNull(addr) == True or isNull(userName) == True or isNull(password) == True:
            QMessageBox.information(self, '警告', 'ftp ip地址或用户名或密码不能为空，请检查!',
                                    QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
        else:
            self.ftpOperation = FtpClient(addr, int(port))
            ftpclient = self.ftpOperation.ftp_connect(userName, password)
            print("ftp:" + ftpclient.getwelcome())
            self.textBrowser.append(ftpclient.getwelcome())
            self.textBrowser.append("ftp:" + addr + " 链接成功！")

    def download_pack(self):
        ftp_path=self.lineEdit_5.text()
        savepath = self.lineEdit_6.text()
        filter_str=self.lineEdit_7.text()
        zip_name = self.lineEdit_8.text()
        self.textBrowser.append("正在下载文件......")
        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%Y%m%d")
        save_file_path=savepath+"/"+formatted_date+'ftp_download'
        if os.path.exists(save_file_path):
            formatted_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            save_file_path=savepath+"/"+formatted_date+'ftp_download'
            os.mkdir(save_file_path)
        else:
            os.mkdir(save_file_path)
        res=self.ftpOperation.download_file(ftp_path,save_file_path,filter_str)
        if res==0:
            self.textBrowser.append("下载完成:"+savepath)
        self.pack_file(save_file_path,save_file_path,filter_str+zip_name)

    def pack_file(self,zip_file_path,save_path,pack_name):
        #folder_path = os.path.join(save_path, pack_name)
        folder_path = save_path+"/"+pack_name;
        #print("打包文件："+folder_path)
        self.textBrowser.append("正在打包文件....")
        self.textBrowser.append("打包文件名："+ folder_path)
        with zipfile.ZipFile(folder_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(zip_file_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    zip_file.write(file_path, os.path.relpath(file_path, folder_path))
        self.textBrowser.append("文件打包完成！" + folder_path )

    def save_ftp_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')                  #方法2：使用注册表
        settings.setValue("account", self.lineEdit_2.text())
        settings.setValue("password", self.lineEdit.text())
        settings.setValue("addr", self.lineEdit_3.text())
        settings.setValue("port", self.lineEdit_4.text())
        settings.setValue("ftppath", self.lineEdit_5.text())
        settings.setValue("savepath", self.lineEdit_6.text())
        settings.setValue("zipname", self.lineEdit_8.text())

        # 初始化登录信息
    def init_ftp_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')                     #方法2：使用注册表
        the_account = settings.value("account")
        the_password = settings.value("password")
        ftp_addr = settings.value("addr")
        ftp_port = settings.value("port")
        ftp_path=settings.value("ftppath")

        save_path = settings.value("savepath")
        zip_name = settings.value("zipname")
        ########
        self.lineEdit_3.setText(ftp_addr)
        self.lineEdit_2.setText(the_account);
        self.lineEdit.setText(the_password);
        self.lineEdit_4.setText(ftp_port)
        self.lineEdit_5.setText(ftp_path)

        ########
        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%Y%m%d")
        self.lineEdit_6.setText(save_path)
        self.lineEdit_8.setText(zip_name)
        self.lineEdit_7.setText(formatted_date)


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = WindowRun()
    widget.show()
    sys.exit(app.exec_())
