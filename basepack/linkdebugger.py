from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit,QLineEdit,QMessageBox,QListWidget,QCommandLinkButton,QLabel
from urllib import request as R
from bs4 import BeautifulSoup as Bs
from threading import Thread
import sys,time,re

class UrlDebugger():
    def __init__(self , parent,parent1):
        author = """
                Author  @ @
                        @    @      @   @       @ @          @   @
                        @    @      @   @      @    @       @
                        @  @          @        @    @        @   @

                email @ duncansantiago18@gmail.com
        """
        print(author)
        self.extracted_urls = dict()
        self.clean_links = list()
        self.dead_links = list()
        self.url = "https://google.com/"
        self.online = False
        self.parent = parent
        self.parent1 = parent1
        self.hostcomm = self.parent.findChild(QLabel , "hostcomm")
        self.host_error = self.parent.findChild(QLabel , "host_error")

    def GetArgs(self):
        if len(sys.argv)>1:
            args = sys.argv[1:]
            self.url = args[0]

    def daemon_handler(self , web_server):
        self.hostcomm.setText("\tcontacting host @" + web_server + ' ...' )

    def parse_urls(self , url):
        self.url = url
        capture_regex = "^http.?://"
        if not re.match(capture_regex , self.url):
            self.url = "http://" + self.url

        web_server_split_url = R.urlparse(self.url)
        web_server = web_server_split_url.scheme + "://" + web_server_split_url.netloc
        daemon = Thread(target = self.daemon_handler , args=(web_server ,))
        daemon.start()
        daemon.join()

        try:
            R.urlopen(self.url)
        except R.URLError as e:
            self.host_error.setText("Connection Error: Check your connectivity if it is down or server might be down\n")
        else:
            self.online = True
            # create a web handler object

            webhandler = Bs(R.urlopen(self.url) , features = 'lxml')

            print("\n\t\tScrapping the page for urls ...")
            time.sleep(.5)

            # find all a tags on the webpage
            net_urls = webhandler.find_all('a')
            self.catalogue = self.parent1.findChild(QListWidget , "urls_found")

            # extract the urls absolute links
            for value in net_urls:
                if value['href']:
                    self.extracted_urls[value.text.strip()] = value['href']

            self.catalogue.addItem("\t\t\t\t============URLS discovered============\n\n\tlink name \t\t\t destination")
            for url in self.extracted_urls.items():
                if R.urlparse(url[1]).scheme == '':
                    self.extracted_urls[url[0]] = web_server+url[1]
                    self.catalogue.addItem("\t{} => \t\t\t{}".format(url[0],web_server+url[1]))
                else:
                    self.catalogue.addItem("\t{} => \t\t\t{}".format(url[0],url[1]))


    def start_debug(self):
        self.dead_links.clear()
        self.clean_links.clear()
        if self.online:
            print("\n\t\t\tAnalyzing urls ... ")
            if R.urlopen(self.url):
                for url in self.extracted_urls.items():
                    try:
                        R.urlopen(url[1])
                    except Exception as e:
                        # print(url)
                        self.dead_links.append(url)
                    else:
                        self.clean_links.append(url)

                return {
                        "error":False,
                        "dead_links":dict(self.dead_links),
                        "clean_links":dict(self.clean_links)
                        }

            else:
                return {
                    "error":True,
                    "info":"The main page might be links is invalid, please check again"
                }
        else:
            return {
                "error":True,
                "info":"The main page might be links is invalid, please check again"
            }
