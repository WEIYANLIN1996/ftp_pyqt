import ftplib
import os
import sys
from ftplib import FTP
from pathlib import Path

import ftpclient
from ftpclient.FtpFileInfo import FTPFileGet
from utils.StringUtils import isNotNull, isNull

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)


class FtpClient:
    def __init__(self,address,port):
        self.ftpClient=FTPFileGet(address);


    def ftp_connect(self,user,password):
        #self.ftpClient.connect(host=address, port=port)
        self.ftpClient.login(user,password)

        return self.ftpClient;

    # 文件上传
    def upload(self,fname):
        fd = open(fname, 'rb')
        new_name = os.path.basename(fname)
        print(new_name)
        # 以二进制的形式上传
        self.ftpClient.storbinary("STOR %s" % new_name, fd)
        fd.close()
        print("upload finished")
        return 0;

    # 文件下载
    def download(self,fname):
        # 构建文件的存储路径，这里用的是D盘,可以自行设置
        new_path = "D:/pythonProject/ftp/downloanFile/" + fname
        fd = open(new_path, 'wb')
        # 以二进制形式下载，注意第二个参数是fd.write，上传时是fd
        self.ftpClient.retrbinary("RETR %s" % fname, fd.write)
        fd.close()
        print("download finished")
        return new_path;

    def ftp_quit(self):
        self.ftpClient.quit();

    def download_file(self,ftp_file_path,local_save_path,filter_str):
        """
        从ftp下载文件到本地
        :param ftp_file_path: ftp下载文件路径
        :param local_save_path: 本地存放路径
        :param filter_str: 文件过滤
        :return:
        """
        buffer_size = 204800  # 默认是8192
        ftp = self.ftpClient
        # print(ftp.getwelcome())  # 显示登录ftp信息
        # if isNull(ftp_file_path):
        #     file_list = ftp.nlst(ftp.pwd())
        # else:
        #     file_list = ftp.nlst(ftp_file_path)
        # print(file_list)
        file_list=self.get_ftp_files(ftp_file_path,filter_str)
        for file_name in file_list:  # 循环获取ftp目录下的所有文件
            print("file_name:" + file_name)  # 打印出来的文件路径包括了ftp_file_path的/test/1.py
            if isNotNull(filter_str) and (filter_str not in str(file_name)):
                print("该文件被过滤")
                continue
            #ftp_file = os.path.join(ftp_file_path, file_name)  # 将文件名和路径拼接
            ftp_file = ftp_file_path+'/'+file_name  # 将文件名和路径拼接
            if ftp.checkFileDir(ftp_file) == "Dir":
                continue
                #self.download_file(ftp_file,local_save_path,filter_str)
                # continue
            print("ftp_file:" + ftp_file)
            #write_file = os.path.join(local_save_path, file_name)
            write_file = local_save_path+'/'+ os.path.basename(ftp_file)
            #write_file =local_save_path
            print("下载文件到本地:" + write_file)
            f = open(write_file, "wb")
            ftp.retrbinary('RETR %s' % ftp_file, f.write, buffer_size)
            # f.close()
        ftp.quit()
        return 0

    def delete_file(self,filepath):
        try:
            ftp = self.ftpClient
            ftp.delete(filepath)
            print("文件删除成功！"+filepath)
        except ftplib.all_errors as e:
            print("文件删除失败：", e)
            return 1
        return 0


    def get_ftp_files(self,ftp_file_path,filter_str):
        print(self.ftpClient.getwelcome())  # 显示登录ftp信息
        if isNull(ftp_file_path):
            file_list = self.ftpClient.nlst(self.ftpClient.pwd())
        else:
            file_list = self.ftpClient.nlst(ftp_file_path)
        res_list=[]
        if isNotNull(filter_str):
            for file_name in file_list:
                if filter_str not in file_name:
                    continue
                res_list.append(file_name)
            return res_list
        return file_list

    def get_files_info(self,ftp_file_path,filter_str):
        file_list=self.get_ftp_files(ftp_file_path,filter_str)
        dict_res={}
        for file in file_list:
            print(file)
            #f = Path(file)
            #file_size=f.stat().st_size
            #file_size=FTP.size(file)
            dict_res[file]='yes'
        return dict_res






# if __name__=='__main__':
#     ftpConnect=FtpClient("127.0.0.1","21").ftp_connect("user","12345")
#     ftp=ftpConnect.ftpClient;
#     ftp.dir()
#     ftp.getwelcome()
#     ftpConnect.upload("D:/个人资料/备忘笔记/常用账号密码.txt")
#     ftpConnect.ftp_quit()
