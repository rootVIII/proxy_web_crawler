#! /usr/bin/python3
# rootVIII
from sys import exit
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from re import findall
from argparse import ArgumentParser
from random import randint, random
from requests import get


class ProxyCrawler:
    def __init__(self, url, keyword):
        self.socket_list = []
        self.keyword = keyword
        self.url = url
        self.proxy_host = ''
        self.proxy_port = 0
        self.fp = None
        self.browser = None
        self.request_count = 0
        self.request_MAX = 5
        self.scrape_socket()

    def set_current_proxy(self):
        self.fp = webdriver.FirefoxProfile()
        self.fp.set_preference("network.proxy.type", 1)
        self.fp.set_preference("network.proxy.http", self.proxy_host)
        self.fp.set_preference("network.proxy.http_port", self.proxy_port)
        self.fp.set_preference("network.proxy.ssl", self.proxy_host)
        self.fp.set_preference("network.proxy.ssl_port", self.proxy_port)
        self.fp.set_preference("general.useragent.override", self.agent())
        self.fp.update_preferences()

    # Use urllib/requests here if desired...
    # It would be much faster
    def scrape_socket(self):
        string_builder = ''
        temp_browser = webdriver.Firefox()
        temp_browser.get('https://www.sslproxies.org/')
        td_tags = temp_browser.find_elements_by_tag_name('td')
        for tag in td_tags:
            string_builder += tag.text + " "
        temp_browser.quit()
        pattern = r"\d+.\d+.\d+.\d+\s+\d+"
        self.socket_list = findall(pattern, string_builder)

    def search(self, socket):
        temp_socket = socket.split()
        self.proxy_host = temp_socket[0]
        self.proxy_port = int(temp_socket[1])
        self.set_current_proxy()
        self.browser = webdriver.Firefox(firefox_profile=self.fp)
        self.browser.get('https://www.bing.com/')
        assert "Bing" in self.browser.title
        print("using socket: %s:%d" % (self.proxy_host, self.proxy_port))
        print("searching for keyword(s):   %s" % self.keyword)
        self.random_sleep('short')
        search_box = self.browser.find_element_by_name("q")
        sub_button = self.browser.find_element_by_name("go")
        self.random_sleep('short')
        search_box.send_keys(self.keyword)
        self.random_sleep('long')
        sub_button.send_keys(Keys.RETURN)
        self.random_sleep('long')
        page_index = 0
        while self.url not in self.browser.current_url:
            page_index += 1
            print("current index:   %s" % str(page_index))
            page_links = self.browser.find_elements_by_xpath("//a[@href]")
            found_link = ''
            for link in page_links:
                if self.url in link.get_attribute("href"):
                    found_link = link
            if found_link:
                print("Found %s at index %d" % (self.url, page_index))
                found_link.click()
            self.random_sleep('short')
            if self.url not in self.browser.current_url:
                self.random_sleep('short')
                idx = str(page_index + 1)
                self.browser.find_element_by_link_text(idx).click()
        self.random_sleep('short')
        target_links = self.browser.find_elements_by_xpath("//a[@href]")
        random_page_num = randint(0, len(target_links) - 1)
        self.random_sleep('long')
        target_link = target_links[random_page_num]
        target_link.click()
        self.random_sleep('long')
        print("visiting random page: " + self.browser.current_url)
        self.random_sleep('short')

    def start_search(self):
        for socket in self.socket_list:
            try:
                self.search(socket)
            except Exception as e:
                print(type(e).__name__, e)
                print('Trying next socket...')
                self.browser.quit()
                continue
            else:
                self.browser.quit()
            finally:
                self.request_count += 1
                if self.request_count > self.request_MAX:
                    self.request_count = 0
                    self.scrape_socket()

    # Add/remove desired user-agents below
    @staticmethod
    def agent():
        agents = [
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
        return agents[randint(0, len(agents) - 1)]

    @staticmethod
    def random_sleep(length):
        if length != 'long':
            sleep(randint(5, 10) + random())
        else:
            sleep(randint(30, 60) + random())


if __name__ == "__main__":
    description = 'Usage: python proxy_crawler.py -u '
    description += '<https://example.com> -k <search keyword>'
    parser = ArgumentParser(description=description)
    parser.add_argument('-u', '--url', required=True, help='url')
    parser.add_argument('-k', '--keyword', required=True, help='keyword')
    d = parser.parse_args()
    try:
        req = get(d.url)
    except Exception:
        print('Unable to make request to %s' % d.url)
        exit(1)
    else:
        if req.status_code != 200:
            print('Invalid URL')
            exit(1)
    while True:
        bot = ProxyCrawler(d.url, d.keyword)
        bot.start_search()
