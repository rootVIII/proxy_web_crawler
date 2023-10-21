from os import path
from re import findall
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen, Request
from utils.utils import randint, random_sleep


class ProxyCrawler(object):
    def __init__(self, url: str, keyword: str, is_headless: bool, user_agents: list):
        self.proxies = []
        self.is_headless = is_headless
        self.browser = None
        self.user_agents = user_agents
        self.url, self.keyword, self.path = url, keyword, path

    def get_agent(self):
        return self.user_agents[randint(0, len(self.user_agents) - 1)]

    def scrape_sockets(self):
        resp = urlopen(Request('https://www.sslproxies.org/',
                               headers={'User-Agent': self.get_agent()}))
        if resp.getcode() != 200:
            raise RuntimeError('sslproxies.org is unreachable')
        text = resp.read().decode('utf-8')
        self.proxies = findall(r'<tr><td>(\d+\.\d+\.\d+\.\d+)<\W?td><td>(\d+)<\W?td>', text)

    def search(self, proxy: tuple):
        host, port = proxy
        firefox_opts = webdriver.FirefoxOptions()
        firefox_opts.set_preference('network.proxy.type', 1)
        firefox_opts.set_preference('network.proxy.http', host)
        firefox_opts.set_preference('network.proxy.http_port', port)
        firefox_opts.set_preference('network.proxy.ssl', host)
        firefox_opts.set_preference('network.proxy.ssl_port', port)
        firefox_opts.set_preference('general.useragent.override', self.get_agent())
        if self.is_headless:
            firefox_opts.add_argument('--headless')

        self.browser = webdriver.Firefox(options=firefox_opts)
        self.browser.set_page_load_timeout(30)
        self.browser.get('https://www.duckduckgo.com')
        print('socket: %s:%s' % proxy)
        random_sleep(short=True)
        assert 'DuckDuckGo' in self.browser.title

        for tag in self.browser.find_elements(By.TAG_NAME, 'input'):
            print(tag.get_attribute('type'))
        # search_box = self.browser.find_elements(By.TAG_NAME, 'input')
        random_sleep(short=True)
        # search_box.send_keys(self.keyword)
        # random_sleep(short=True)
        # search_box.send_keys(Keys.RETURN)
        # random_sleep(short=True)
        page_index = 0

        # Search until the desired URL is found
        # while True:
        #     page_index += 1
        #     page_links = self.browser.find_elements_by_xpath(''//a[@href]'')
        #     found_link = None
        #     for link in page_links:
        #         if self.url[8:] in link.get_attribute('href'):
        #             print('found %s at index: %d' % (self.url, page_index))
        #             found_link = link
        #             break
        #     if found_link is not None:
        #         found_link.click()
        #         break

        #     random_sleep()
        #     index = str(page_index + 1)
        #     self.browser.find_element_by_link_text(index).click()
        #     self.random_sleep(short=True)

        # Found page
        # self.random_sleep(short=True)
        # while self.url[8:] not in self.browser.current_url:
        #     print('waiting for page to load...')
        #     random_sleep()
        # random_sleep()
        # target_links = self.browser.find_elements_by_xpath(''//a[@href]'')
        # random_page_num = randint(0, len(target_links) - 1)
        # target_link = target_links[random_page_num]
        # random_sleep()
        # target_link.click()
        # random_sleep()
        # print('visiting random page: %s' % self.browser.current_url)
        # random_sleep()

    def start_search(self):
        self.scrape_sockets()
        for proxy in self.proxies:
            try:
                self.search(proxy)
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except Exception as error:
                print(error)
                print('trying next socket...')
            finally:
                if self.browser is not None:
                    self.browser.close()
