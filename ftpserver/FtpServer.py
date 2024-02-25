
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class FtpServer:

    def ftpStart(self):
        # 实例化虚拟用户，这是FTP验证首要条件
        authorizer = DummyAuthorizer()

        authorizer.add_user('user', '12345', 'D:/ftpFile', perm='elradfmw')
        # 添加匿名用户 只需要路径
        authorizer.add_anonymous('D:/ftpFile/test')

        handler = FTPHandler
        handler.authorizer = authorizer
        # 添加被动端口范围
        handler.passive_ports = range(2000, 9333)
        # 监听ip 和 端口,使用21端口
        server = FTPServer(('127.0.0.1', 21), handler)
        # server.set_pasv(False)
        # 开始服务
        server.serve_forever()



if __name__=='__main__':
   FtpServer().ftpStart();
   # C:\Users\ht\AppData\Roaming\Microsoft\Windows\Start
   # Menu\Programs\Python
   # 3.9
   #
   # pip config set  trusted-host  mirrors.aliyun.com





