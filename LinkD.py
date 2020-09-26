from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit,QLineEdit,QMessageBox,QListWidget,QCommandLinkButton,QLabel
from basepack import linkdebugger as LD
from threading import Thread
from PyQt5 import uic
import sys

class LinkDebugger(QMainWindow):
    def __init__(self):
        super(LinkDebugger, self).__init__()
        uic.loadUi("LinkDebugger.ui", self)
        self.startBtn = self.findChild(QPushButton , 'startBtn')
        self.startBtn.clicked.connect(self.startDefault)
        self.show()

    def startDefault(self):
        self.hide()
        self.default = Default(self)

class Default(QMainWindow):
    def __init__(self , parent):
        super(Default, self).__init__()
        uic.loadUi("base.ui", self)
        self.Search_Uri = self.findChild(QPushButton , 'searchUri')
        self.view_results = self.findChild(QPushButton , 'view_results')
        self.host_error = self.findChild(QLabel , "host_error")
        self.view_results.hide()
        self.infor_urls = self.findChild(QLabel , 'infor_urls')
        self.infor_urls.hide()
        self.Search_Uri.clicked.connect(self.startDebug)
        self.show()
        self.Launcher()

    def Launcher(self):
        self.target_host = self.findChild(QLineEdit , "target_host")
        self.View = Results(self)
        self.daemon = LD.UrlDebugger(self,self.View)

    def daemon_handler(self):
        self.infor_urls.show()

    def startDebug(self):
        if self.target_host.text():
            self.daemon_parse_url = Thread(target = self.daemon.parse_urls,args = (self.target_host.text(),))
            self.daemon_parse_url.start()
            self.daemon_parse_url.join()
            self.daemon_handler()

            urls_info = self.daemon.start_debug()

            self.View.urls_info = urls_info
            self.view_results = self.findChild(QPushButton , "view_results")
            self.View.target_host = self.target_host.text()
            self.view_results.clicked.connect(self.View.manage_results)
            self.view_results.show()
        else:
            self.host_error.setText("Invalid url provided, please try again.")

class Results(QMainWindow):
    def __init__(self , parent):
        super(Results, self).__init__()
        uic.loadUi("results.ui", self)
        self.target_host = ''
        self.catalogue = self.findChild(QListWidget , "urls_found")
        self.urls_info = ''

    def manage_results(self):
        self.show()
        # title = self.findChild(QLabel , "title")
        # title_info = title.text() + self.target_host
        # title.setText(title_info)

        if self.urls_info['error']:
            print(self.urls_info['info'])
        else:
            self.catalogue.addItem("\n\n\t\t\t===========Dead Links===========")

            if len(self.urls_info['dead_links'].items())<1:
                self.catalogue.addItem("\t\t\tThe are not Dead Links")
            else:
                for target in self.urls_info['dead_links'].items():
                    self.catalogue.addItem("\t\t\t" + target[0] + "\t=>" + target[1])

                    self.catalogue.addItem("\n\n\t\t\t===========Clean Links ===========")

                    if len(self.urls_info['clean_links'].items())<1:
                        self.catalogue.addItem("\t\t\tThe are not clean Links")
                    else:
                        for target in self.urls_info['clean_links'].items():
                            self.catalogue.addItem("\t\t\t"+ target[0] + "\t=> " + target[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    base = LinkDebugger()
    app.exec_()
