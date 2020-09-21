from urllib import request as R
from bs4 import BeautifulSoup as Bs
import sys,time

class UrlDebugger():
    def __init__(self):
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
        self.GetArgs()
        self.parse_urls()


    def GetArgs(self):
        if len(sys.argv)>1:
            args = sys.argv[1:]
            self.url = args[0]

    def parse_urls(self):
        base_uri = self.url
        web_server_split_url = R.urlparse(base_uri)
        web_server = web_server_split_url.scheme + "://" + web_server_split_url.netloc
        print("\tcontacting host @" + web_server + ' ...' )
        time.sleep(1)

        try:
            R.urlopen(self.url)
        except R.URLError as e:
            print("\t\tConnection Error: Check your connectivity if it is down or server might be down\n")
        else:
            self.online = True
            # create a web handler object
            webhandler = Bs(R.urlopen(self.url) , features = 'lxml')

            print("\n\n\t\tScrapping the page for urls ...")
            time.sleep(.5)

            # find all a tags on the webpage
            net_urls = webhandler.find_all('a')

            # extract the urls absolute links
            for value in net_urls:
                if value['href']:
                    self.extracted_urls[value.text.strip()] = value['href']

            print("\t\t\t\t\t============URLS discovered============\n\n\t\t\tlink name \t\t\t destination")
            for url in self.extracted_urls.items():
                if R.urlparse(url[1]).scheme == '':
                    self.extracted_urls[url[0]] = web_server+url[1]
                    print("\t\t\t{} => \t\t\t{}".format(url[0],web_server+url[1]),end= '\n')
                else:
                    print("\t\t\t{} => \t\t\t{}".format(url[0],url[1]),end= '\n')


    def start_debug(self):
        if self.online:
            if R.urlopen(self.url):
                for url in self.extracted_urls.items():
                    try:
                        R.urlopen(url[1])
                    except Exception as e:
                        # print(url)
                        self.dead_links.append(url)
                    else:
                        self.clean_links.append(url)
                self.dead_links = dict(self.dead_links)
                self.clean_links = dict(self.clean_links)
                return {
                        "error":False,
                        "dead_links":self.dead_links,
                        "clean_links":self.clean_links
                        }

            else:
                return {
                    "error":True,
                    "info":"The main page might be links is invalid, please chck again"
                }
        else:
            return {
                "error":True,
                "info":"The main page might be links is invalid, please chck again"
            }

if __name__ == '__main__':
    UrlDebugger = UrlDebugger()
    urls_info = UrlDebugger.start_debug()
    if urls_info['error']:
        print(urls_info['info'])
    else:
        print("\n\t\t\t===========Dead Links===========")

        if len(urls_info['dead_links'].items())<1:
            print("\t\t\tThe are not Dead Links")
        else:
            for target in urls_info['dead_links'].items():
                print("\t\t\t" + target[0] + "\t=>" + target[1])

        print("\n\n\t\t\t===========Clean Links ===========")

        if len(urls_info['clean_links'].items())<1:
            print("\t\t\tThe are not clean Links")
        else:
            for target in urls_info['clean_links'].items():
                print("\t\t\t"+ target[0] + "\t=> " + target[1])
