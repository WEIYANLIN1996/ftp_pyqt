import sys

from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication

from ftpclient.FtpGui import Ui_MainWindow


class Mainwindow(Ui_MainWindow, QMainWindow):
    def init(self):
        super(Mainwindow, self).init()
        self.setupUi(self)
        #self.menu_2.triggered(self.menuWindow)



    def paintEvent(self, event):  # 背景图片自适应
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap("../image/backgroup.jpeg")  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)



# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Mainwindow()
    ui = Ui_MainWindow()
    ui.setupUi(w)
    w.show()
    #w.result_show("1",1)
    sys.exit(app.exec_())
