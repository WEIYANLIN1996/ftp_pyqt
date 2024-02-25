import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSettings, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QMessageBox, QMenu, QAction

from ftp_download.ui.ftp_list import Ui_Dialog


class FtpListGui(QDialog,Ui_Dialog):
    def __init__(self):
        super(FtpListGui, self).__init__()
        self.setupUi(self)
        self.load_ftp_info()
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.close)
        self.listWidget.setContextMenuPolicy(3)
        self.listWidget.customContextMenuRequested[QPoint].connect(self.listWidgetContext)

    def listWidgetContext(self):
        popMenu = QMenu()
        delete_action = QAction("删除", popMenu)
        delete_action.triggered.connect(self.delete_listItem)
        popMenu.addAction(delete_action)
        popMenu.exec_(QCursor.pos())
    def delete_listItem(self):
        item=self.listWidget.currentItem()
        text=item.text()
        if 'FTP-no-1' in text:
            params_number='1'
            self.remove_config(params_number)
        if 'FTP-no-2' in text:
            params_number = '2'
            self.remove_config(params_number)
        if 'FTP-no-3' in text:
            params_number='3'
            self.remove_config(params_number)

        self.listWidget.takeItem(self.listWidget.currentRow())
    def remove_config(self,params_number):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.remove("account" + params_number)
        settings.remove("password" + params_number)
        settings.remove("addr" + params_number)
        settings.remove("port" + params_number)
        settings.remove("ftppath" + params_number)
        settings.remove("savepath" + params_number)
        settings.remove("zipname" + params_number)
        settings.remove("filter_str" + params_number)
        settings.remove("select" + params_number)
        settings.remove("intervalorfixedtime" + params_number)
        new_number = settings.value("paramsnum")
        if new_number == '0':
            return
        settings.setValue("paramsnum", int(new_number) - 1)

    def load_ftp_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        params_number = settings.value("paramsnum")
        if params_number == None:
            QMessageBox.information(self, '警告', 'ftp 未配置，请添加FTP配置信息!',
                                    QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return 0
        for num in range(1, int(params_number) + 1):
            num=str(num)
            the_account = settings.value("account" + num)
            ftp_addr = settings.value("addr" + num)
            ftp_port = settings.value("port" + num)
            zip_name = settings.value("zipname" + num)
            item = QtWidgets.QListWidgetItem()
            brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
            brush.setStyle(QtCore.Qt.NoBrush)
            item.setBackground(brush)
            item.setCheckState(QtCore.Qt.Checked)
            item.setText('FTP-no-'+num+':'+str(ftp_addr)+':'+str(ftp_port)+' user:'+the_account+' 打包名:'+zip_name)
            self.listWidget.addItem(item)




# if __name__=='__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     widget = FtpListGui()
#     widget.show()
#     sys.exit(app.exec_())
