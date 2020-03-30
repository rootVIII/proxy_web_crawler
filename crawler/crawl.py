from re import findall
from random import randint, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import platform
from time import sleep
from urllib.request import urlopen, Request
# rootVIII 2018-2020

try:
    from pyvirtualdisplay import Display
    xvfb = True
except ImportError:
    xvfb = False


class ProxyCrawler(object):
    def __init__(self, url, keyword):
        self.sockets, self.agents = [], []
        self.url, self.keyword = url, keyword
        self.proxy_host, self.fp, self.browser = (None for _ in range(3))
        self.request_MAX, self.proxy_port, self.request_count = 5, 0, 0
        self.set_agents()
        self.scrape_sockets()

    @staticmethod
    def random_sleep(short=False):
        if not short:
            sleep(randint(30, 60) + random())
        else:
            sleep(randint(5, 10) + random())

    def set_current_proxy(self):
        self.fp = webdriver.FirefoxProfile()
        self.fp.set_preference('network.proxy.type', 1)
        self.fp.set_preference('network.proxy.http', self.proxy_host)
        self.fp.set_preference('network.proxy.http_port', self.proxy_port)
        self.fp.set_preference('network.proxy.ssl', self.proxy_host)
        self.fp.set_preference('network.proxy.ssl_port', self.proxy_port)
        self.fp.set_preference('general.useragent.override', self.agent())
        self.fp.update_preferences()

    def scrape_sockets(self):
        print('acquiring new proxies...')
        agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) '
        agent += 'AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.398'
        agent += '7.95 Mobile/15E148 Safari/605.1'
        resp = urlopen(Request(
            'https://www.sslproxies.org/',
            headers={'User-Agent': agent})).read().decode('utf-8')
        matches = findall(r'<td>\d+\.\d+\.\d+\.\d+</td><td>\d+</td>', resp)
        revised = [tag.replace('<td>', '') for tag in matches]
        self.sockets = [s[:-5].replace('</td>', ':') for s in revised]

    def search(self, socket):
        sock = socket.split(':')
        self.proxy_host, self.proxy_port = sock[0], int(sock[1])
        self.set_current_proxy()
        self.browser = webdriver.Firefox(firefox_profile=self.fp)
        self.browser.set_page_load_timeout(30)
        self.browser.get('https://www.bing.com/')
        assert 'Bing' in self.browser.title
        print('searching for keyword(s):   %s' % self.keyword)
        print('socket: %s:%d' % (self.proxy_host, self.proxy_port))
        self.random_sleep(short=True)
        search_box = self.browser.find_element_by_name('q')
        self.random_sleep(short=True)
        search_box.send_keys(self.keyword)
        self.random_sleep()
        search_box.send_keys(Keys.RETURN)
        self.random_sleep()
        page_index = 0

        # Search until the desired URL is found
        while True:
            page_index += 1
            page_links = self.browser.find_elements_by_xpath("//a[@href]")
            found_link = None
            for link in page_links:
                if self.url[8:] in link.get_attribute('href'):
                    print('found %s at index: %d' % (self.url, page_index))
                    found_link = link
                    break
            if found_link is not None:
                found_link.click()
                break
           
            self.random_sleep()
            index = str(page_index + 1)
            self.browser.find_element_by_link_text(index).click()
            self.random_sleep(short=True)

        # Found page
        self.random_sleep(short=True)
        while self.url[8:] not in self.browser.current_url:
            print('waiting for page to load...')
            self.random_sleep()
        self.random_sleep()
        target_links = self.browser.find_elements_by_xpath("//a[@href]")
        random_page_num = randint(0, len(target_links) - 1)
        target_link = target_links[random_page_num]
        self.random_sleep()
        target_link.click()
        self.random_sleep()
        print('visiting random page: %s' % self.browser.current_url)
        self.random_sleep()

    def start_search(self):
        for socket in self.sockets:
            try:
                self.search(socket)
            except Exception as e:
                print('%s: %s' % (type(e).__name__, str(e)))
                print('trying next socket...')
            finally:
                self.browser.quit()
                self.request_count += 1
                if self.request_count > self.request_MAX:
                    self.request_count = 0
                    self.scrape_sockets()

    def agent(self):
        return self.agents[randint(0, len(self.agents) - 1)]

    def set_agents(self):
        self.agents = [
            "Opera/9.80 (S60; SymbOS; Opera Mobi/498; U; sv)",
            "Mozilla/2.02 [fr] (WinNT; I)",
            "WeatherReport/1.2.2 CFNetwork/485.12.7 Darwin/10.4.0",
            "W3C_Validator/1.432.2.10",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
            "Cyberdog/2.0 (Macintosh; 68k)",
            "MJ12bot/v1.0.8 (http://majestic12.co.uk/bot.php?+)",
            "Exabot/2.0",
            "Mozilla/5.0 (compatible; news bot /2.1)",
            "curl/7.19.6 (i686-pc-cygwin)",
            "ConveraCrawler/0.4",
            "Mozilla/4.0 (MSIE 6.0; Windows NT 5.1; Search)",
            "EARTHCOM.info/1.6 [www.earthcom.info]",
            "librabot/1.0 (+http://search.msn.com/msnbot.htm)",
            "NetResearchServer/2.5(loopimprovements.com/robot.html)",
            "PHP/5.2.10",
            "msnbot-Products/1.0 (+http://search.msn.com/msnbot.htm)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;)"
        ]


class HeadlessProxyCrawler(ProxyCrawler):
    def __init__(self, url, keyword):
        super().__init__(url, keyword)
        if not xvfb or platform == 'win32':
            raise Exception('Unable to import pyvirtualdisplay')
        self.url = url
        self.keyword = keyword

    def start_search(self):
        for socket in self.sockets:
            with Display():
                try:
                    self.search(socket)
                except Exception as e:
                    print('%s: %s' % (type(e).__name__, str(e)))
                    print('trying next socket...')
                finally:
                    self.browser.quit()
                    self.request_count += 1
                    if self.request_count > self.request_MAX:
                        self.request_count = 0
                        self.scrape_sockets()
