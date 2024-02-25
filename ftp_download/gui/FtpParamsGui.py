import os
import sys
import datetime

from ftp_download.ui.ftp_param import Ui_Dialog
from utils.StringUtils import isNull

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QMessageBox, QLineEdit


class FtpParamsGui(QDialog,Ui_Dialog):
    def __init__(self):
        super(FtpParamsGui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.saveParams)
        self.checkBox.clicked.connect(self.checkSetNull_1)
        self.checkBox_2.clicked.connect(self.checkSetNull_2)
        self.checkBox_2.hide()
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(False)
        self.lineEdit_5.setPlaceholderText("定时任务请以'12:00:00'格式输入")
        self.init_ftp_info(str(1))
        self.lineEdit_4.setEchoMode(QLineEdit.Password)

    def checkSetNull_1(self):
        if self.checkBox_2.isChecked():
            self.checkBox_2.setChecked(False)

    def checkSetNull_2(self):
        if self.checkBox.isChecked():
            self.checkBox.setChecked(False)


    def saveParams(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')
        print("----")
        params_number = settings.value("paramsnum")
        if params_number==None:
           params_number=0
        if int(params_number)<3:
            print("地址:" + self.lineEdit.text() + ",用户名:" + self.lineEdit_3.text() + "," + self.lineEdit_4.text())
            if isNull(self.lineEdit.text()) == True or isNull(self.lineEdit_3.text()) == True or isNull(self.lineEdit_4.text()) == True:
                QMessageBox.information(self, '警告', 'ftp ip地址或用户名或密码不能为空，请检查!',
                                        QMessageBox.Ok | QMessageBox.Close,
                                        QMessageBox.Close)
            params_number=str(int(params_number)+1)
            settings.setValue("paramsnum", params_number)
            settings.setValue("account"+params_number, self.lineEdit_3.text())
            settings.setValue("password"+params_number, self.lineEdit_4.text())
            settings.setValue("addr"+params_number, self.lineEdit.text())
            settings.setValue("port"+params_number, self.lineEdit_2.text())
            settings.setValue("ftppath"+params_number, self.lineEdit_8.text())
            settings.setValue("savepath"+params_number, self.lineEdit_9.text())
            settings.setValue("zipname"+params_number, self.lineEdit_7.text())
            settings.setValue("filter_str" + params_number, self.lineEdit_6.text())
            settings.setValue("zipfilename" + params_number, '测试')
            select = "fixedtime"
            # if self.checkBox.isChecked():
            #     select = "fixedtime"
            # if self.checkBox_2.isChecked():
            #     select="interval"
            settings.setValue("select" + params_number, select)
            settings.setValue("intervalorfixedtime" + params_number, self.lineEdit_5.text())
            QMessageBox.warning(self, self.tr("My Application"),
                                self.tr("添加成功!"),
                                QMessageBox.Ok |  QMessageBox.No,
                                QMessageBox.Ok )
        else:
            QMessageBox.warning(self, self.tr("My Application"),
                                self.tr("ftp配置超过三个!"),
                                QMessageBox.Ok |  QMessageBox.No,
                                QMessageBox.Ok )


    def init_ftp_info(self,num):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')                     #方法2：使用注册表
        the_account = settings.value("account"+num)
        the_password = settings.value("password"+num)
        ftp_addr = settings.value("addr"+num)
        ftp_port = settings.value("port"+num)
        ftp_path=settings.value("ftppath"+num)

        save_path = settings.value("savepath"+num)
        zip_name = settings.value("zipname"+num)
        select = settings.value("select"+num)
        intervalorfixedtime = settings.value("intervalorfixedtime"+num)
        ########
        self.lineEdit.setText(ftp_addr)
        self.lineEdit_3.setText(the_account);
        self.lineEdit_4.setText(the_password);
        self.lineEdit_2.setText(ftp_port)
        self.lineEdit_8.setText(ftp_path)

        ########
        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%Y%m%d")
        self.lineEdit_9.setText(save_path)
        self.lineEdit_7.setText(zip_name)
        self.lineEdit_6.setText(formatted_date)
        self.lineEdit_5.setText(intervalorfixedtime)

        if select == "interval":
            self.checkBox.setChecked(True)
            self.checkBox_2.setChecked(False)
        if select == "fixedtime":
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(True)



# if __name__=='__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     widget = FtpParamsGui()
#     widget.show()
#     sys.exit(app.exec_())