from datetime import datetime

from PyQt5.QtCore import QSettings

from ftp_download.version1.ftp_download import Ui_MainWindow


class ConfigData(Ui_MainWindow):

    def save_ftp_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        # settings = QSettings("mysoft","myapp")                        #方法2：使用注册表
        settings.setValue("account", self.self.lineEdit_2.text())
        settings.setValue("password", self.self.lineEdit.text())
        settings.setValue("addr", self.lineEdit_3.text())
        settings.setValue("port", self.lineEdit_4.text())
        settings.setValue("ftppath", self.lineEdit_5.text())
        settings.setValue("savepath", self.lineEdit_6.text())

        # 初始化登录信息
    def init_ftp_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        # settings = QSettings("mysoft","myapp")                        #方法2：使用注册表
        the_account = settings.value("account")
        the_password = settings.value("password")
        ftp_addr = settings.value("addr")
        ftp_port = settings.value("port")
        ftp_path=settings.value("ftppath")
        save_path = settings.value("savepath")
        ########
        self.lineEdit_3.setText(ftp_addr)
        self.lineEdit_2.setText(the_account);
        self.lineEdit.setText(the_password);
        self.lineEdit_4.setText(ftp_port)
        self.lineEdit_5.setText(ftp_path)
        self.lineEdit_6.setText(save_path)

        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%Y%m%d")
        self.lineEdit_7.setText(formatted_date)


            # self.on_pushButton_enter_clicked()
