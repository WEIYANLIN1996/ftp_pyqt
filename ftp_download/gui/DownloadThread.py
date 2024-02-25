from ftplib import error_perm

from PyQt5.QtCore import QThread, pyqtSignal


class DownloadThread(QThread):
    sinout = pyqtSignal(str)  # 自定义信号，执行run()函数时，从相关线程发射此信号

    def __init__(self,ftp_path,save_file_path,zip_name,filter_str,ftp):
        super(DownloadThread, self).__init__()
        self.ftp_path=ftp_path
        self.save_file_path=save_file_path
        self.filter_str=filter_str
        self.ftpOperation=ftp
        self.zip_name=zip_name

    def run(self):
        # 需要执行的内容
        try:
            res=self.ftpOperation.download_file(self.ftp_path,self.save_file_path,self.filter_str)
            if res==0:
                self.sinout.emit(str(1))
        except error_perm as fe:
            print("下载异常:" + fe)  # 不能通过路劲打开必为文件，抓取其错误信息

        # 定义的槽函数，当xxxxx执行完成后就向UI界面（调用多线程的程序）发送一个指令，并让UI界面执行相应的内容。
        # str(1)-->发送的值，该值可以是xxxxx执行后返回的值，也可以是任意值（表示是否执行另一程序）


