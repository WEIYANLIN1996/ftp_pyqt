import datetime
import gc
import os
import sys
import threading
import time
import zipfile
from ftplib import error_perm
import psutil
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSettings, QTimer, QProcess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QAction, QMenu, QSystemTrayIcon, \
    qApp

from ftp_download.gui.FtpLIstGui import FtpListGui
from ftp_download.gui.FtpParamsGui import FtpParamsGui
from ftp_download.ui.Ftp_downloads import Ui_MainWindow
from ftpclient.FtpClientOperation import FtpClient

from ftp_download.ui import resourses_rc

#pyinstaller -F  --icon=D:\pythonProject\ftp\ftp_download\resoure\icon.ico main.py
#----2023-10-02
#pyinstaller -F  -i D:\pythonProject\ftp\ftp_download\gui\resoure\icon.ico main.py  --noconsole

class FtpDownloads(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(FtpDownloads, self).__init__()
        self.setupUi(self)
        self.init_config()
        self.actiondfd.triggered.connect(self.addParams)
        self.actionchakan.triggered.connect(self.viewParams)
        self.actionexit.triggered.connect(self.quit)
        self.actionnihap.triggered.connect(self.sync_download_pack)
        self.actiondingshixaizai.triggered.connect(self.fixed_download_pack)
        self.actiondangexaizai.triggered.connect(self.ftp_download)
        self.actionstopt_all_task.triggered.connect(self.stop_all_task)
        self.timer_list=[]

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(':resoure/favicon.ico'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        # self.init_ftp_info()
        # self.pushButton.clicked.connect(self.connect_ftp)
        # self.pushButton_4.clicked.connect(self.download_pack)
        self.createTrayIcon()
        self.trayIcon.show()

    def createTrayIcon(self):
        aRestore = QAction('恢复(&R)', self, triggered=self.show)
        aQuit = QAction('退出(&Q)', self, triggered=QApplication.instance().quit)

        menu = QMenu(self)
        menu.addAction(aRestore)
        menu.addAction(aQuit)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(':resoure/icon.jpg'))
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.activated.connect(self.iconActivated)

    def iconActivated(self, reason):
        if reason in (QSystemTrayIcon.DoubleClick, QSystemTrayIcon.MiddleClick):
            self.ui.show()

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QMessageBox.information(self, '系统托盘',
                                    '程序将继续在系统托盘中运行，要终止本程序，\n'
                                    '请在系统托盘入口的上下文菜单中选择"退出"')
            self.hide()
            event.ignore()


    def ftp_download(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')  # 方法2：使用注册表
        params_number = settings.value("paramsnum")
        if params_number == None:
            QMessageBox.information(self, '警告', 'ftp 未配置，请添加FTP配置信息!',
                                    QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            params_number=0
        for num in range(1, int(params_number) + 1):
            self.download_pack(str(num), False)
    def stop_all_task(self):
        for task in self.timer_list:
            task.stop()
            self.textBrowser.append("定时任务停止！" + str(task))
        self.timer_list=[]

    def sync_download_pack(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')  # 方法2：使用注册表
        params_number = settings.value("paramsnum")
        if params_number == None:
            QMessageBox.information(self, '警告', 'ftp 未配置，请添加FTP配置信息!',
                                    QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
        for num in range(1, int(params_number) + 1):
            self.download_pack(str(num),True)


    def fixed_download_pack(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')  # 方法2：使用注册表
        params_number = settings.value("paramsnum")
        if params_number == None:
            QMessageBox.information(self, '警告', 'ftp 未配置，请添加FTP配置信息!',
                                    QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return

        for num in range(1,int(params_number)+1):
            self.ftp_task(str(num))


    def ftp_task(self,num):
        timer = QTimer()  # 初始化定时器
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')  # 方法2：使用注册表
        select = settings.value("select" + num)
        intervalorfixedtime = settings.value("intervalorfixedtime" + num)
        try:
            if select == "interval":
                timer.timeout.connect(lambda:self.download_pack(num))
                #timer.start((intervalorfixedtime)*60*60*1000)
            if select == "fixedtime":
                timer.timeout.connect(lambda:self.fixedtime_task(num,intervalorfixedtime,timer))
                timer.start(1000)
            self.timer_list.append(timer)
        except error_perm as fe:
            print("执行异常:"+fe)  # 不能通过路劲打开必为文件，抓取其错误信息
            timer.stop()


    def interval_task(self,num):
        self.download_pack(num,True)

    def restart(self):
        # p=qApp.quit()
        # QtCore.QProcess.startDetached(qApp.applicationFilePath())
        #QtCore.QCoreApplication.quit()
        app = QApplication.instance()  # 获取当前应用程序对象
        app.exit()  # 关闭应用程序
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print("已重启status:"+str(status))
        # self.textBrowser.append("内存占用过大已重启，如定时任务不成功请手动开启定时任务！")
        # time.sleep(2000)
        # self.fixed_download_pack()

    def fixedtime_task(self,num,intervalorfixedtime,timer):
        now_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        date_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        print("定时任务："+num+'时间计数'+date_time)
        info = psutil.virtual_memory()
        use_memory=psutil.Process(os.getpid()).memory_info().rss/(1024*1024)
        self.textBrowser.append("已占用内存" + str(use_memory)+"M")
        if use_memory >= 45:
            print("内存占用过大，已占用内存：" + str(use_memory))
            self.textBrowser.append("内存占用过大，已占用内存" + str(use_memory)+"M")
            is_close=QMessageBox.information(self, '警告', "内存占用过大，已占用内存" + str(use_memory)+"M 是否关闭程序重启？",
                                    QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            if is_close==QMessageBox.Ok:
                self.restart()

        self.textBrowser.append("任务：" + num + '时间计数' + now_time)
        if date_time == intervalorfixedtime:
            gc.collect()
            print("垃圾回收对象"+str(gc.get_count())+" timer内存："+str(sys.getsizeof(timer)/(1024*1024))+"M")
            print(u'内存使用：', psutil.Process(os.getpid()).memory_info().rss)
            print(u'总内存：', info.total)
            print("执行下载任务:"+num)
            self.textBrowser.append("垃圾回收对象"+str(gc.get_count())+" timer内存："+str(sys.getsizeof(timer)))
            self.textBrowser.append("程序使用内存/M：" + str(use_memory) + " 总内存/M：" + str(info.total/(1024*1024)))
            settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
            settings.setIniCodec('UTF-8')  # 方法2：使用注册表
            current_date = datetime.date.today()
            formatted_date = current_date.strftime("%Y%m%d")
            settings.setValue("filter_str" + num, formatted_date)

            self.textBrowser.append("执行下载任务:"+num)
            self.download_pack(num, True)

    def download_pack(self,num,isPack):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')  # 方法2：使用注册表
        the_account = settings.value("account" + num)
        the_password = settings.value("password" + num)
        ftp_addr = settings.value("addr" + num)
        ftp_port = settings.value("port" + num)
        ftp_path = settings.value("ftppath" + num)
        savepath = settings.value("savepath" + num)
        zip_name = settings.value("zipname" + num)

        zip_file_name = settings.value("zipfilename" + num)

        filter_str = settings.value("filter_str" + num)
        self.ftpOperation = FtpClient(ftp_addr, int(ftp_port))
        ftpclient = self.ftpOperation.ftp_connect(the_account, the_password)
        print("ftp:" + ftpclient.getwelcome())
        self.textBrowser.append(ftpclient.getwelcome())
        self.textBrowser.append("ftp:" + ftp_addr+ " 链接成功！")
        dist_files = self.ftpOperation.get_files_info(ftp_path, filter_str)
        self.add_tableWidget(dist_files)

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

        if zip_file_name==None or zip_file_name=='':
            zip_save_path = savepath
            settings.setValue("zipfilename" + num,'测试')
        else:
            zip_save_path = savepath+ "/"+zip_file_name

        if os.path.exists(zip_save_path)==False:
            os.mkdir(zip_save_path)
        #res=self.ftpOperation.download_file(ftp_path,save_file_path,filter_str)
        try:
            thread = threading.Thread(target=self.ftpOperation.download_file,args=(ftp_path,save_file_path,filter_str))
            thread.start()
            while thread.is_alive():
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"正在下载文件中......")
            thread.join()
            if isPack:
                  self.pack_file(save_file_path, zip_save_path,filter_str+zip_name)
        except Exception as e:
            print("下载异常:"+str(e))

        # self.timeThread = DownloadThread(ftp_path,save_file_path,filter_str,zip_name,self.ftpOperation)  # 调用线程的程序
        # self.timeThread.start()  # 开启线程
        # self.timeThread.sinout.connect(lambda :self.pack_file(save_file_path, save_file_path,filter_str+zip_name))
        # # if res==0:
        #     self.textBrowser.append("下载完成:"+savepath)
        #     # 插入表格数据
        #     if isPack:
        #         self.pack_file(save_file_path, save_file_path,filter_str+zip_name)

    def add_tableWidget(self,dist_files):
        for key, value in dist_files.items():
            row_count = self.tableWidget.rowCount()  # 返回当前行数(尾部)
            self.tableWidget.insertRow(row_count)  # 尾部插入一行
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(key))
            self.tableWidget.setItem(row_count, 1, QTableWidgetItem(value))


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

    def addParams(self):
        w = FtpParamsGui()
        w.exec_()

    def viewParams(self):
        w = FtpListGui()
        w.exec_()

    def init_config(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')  # 方法2：使用注册表
        params_number = settings.value("paramsnum")
        if params_number == None:
            QMessageBox.information(self, '警告', 'ftp 未配置，请添加FTP配置信息!',
                                    QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return
        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%Y%m%d")
        for num in range(1, int(params_number) + 1):
            settings.setValue("filter_str" + str(num), formatted_date)


    def quit(self):
        app = QApplication.instance()  # 获取当前应用程序对象
        app.quit()  # 关闭应用程序





# if __name__=='__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     QApplication.setQuitOnLastWindowClosed(False)
#     widget = FtpDownloads()
#     # widget.showMinimized()
#     # tray = TrayIcon(widget)
#     # tray.show()
#     # sys.exit(app.exec_())
#     widget.show()
#     sys.exit(app.exec_())