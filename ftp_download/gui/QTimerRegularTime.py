import time

from PyQt5.QtCore import QTimer, QSettings


class ThreadTimer(QTimer):
    def __init__(self):
        pass

    def ftp_task(self,num):
        self.timer = QTimer()  # 初始化定时器
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setIniCodec('UTF-8')  # 方法2：使用注册表
        the_account = settings.value("account" + num)
        the_password = settings.value("password" + num)
        ftp_addr = settings.value("addr" + num)
        ftp_port = settings.value("port" + num)
        ftp_path = settings.value("ftppath" + num)

        save_path = settings.value("savepath" + num)
        zip_name = settings.value("zipname" + num)
        select = settings.value("select" + num)
        intervalorfixedtime = settings.value("intervalorfixedtime" + num)

        if select == "interval":
            self.timer.timeout.connect(self.interval_task)
            self.timer.start(intervalorfixedtime*60*60*1000)

        if select == "fixedtime":
            self.timer.timeout.connect(self.time)
            self.timer.start(1000)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            date_time=time.strftime('%H:%M', time.localtime(time.time()))
            if date_time==intervalorfixedtime:
                pass


        # 定义时间任务是一次性任务，当是一次性任务的时候self.timer.start()不需要指定时间
        # self.timer.setSingleShot(True)

    def time(self):
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    def interval_task(self):
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


    def stopTimer(self):
        self.timer.stop()

    def startTimer(self):
        self.timer.start(1000)

