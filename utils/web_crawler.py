from re import findall
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from urllib.request import urlopen, Request
from utils.utils import randint, random_sleep


class ProxyCrawler(object):
    def __init__(self, url: str, keyword: str, is_headless: bool, user_agents: list):
        self.proxies = []
        self.is_headless = is_headless
        self.browser = None
        self.user_agents = user_agents
        self.url, self.keyword = url, keyword
        self.page_index_max = 100  # Search results page index max

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
        # To view FF profile open the browser and enter about:support
        host, port = proxy
        firefox_opts = Options()
        firefox_opts.page_load_strategy = 'eager'
        firefox_opts.set_preference('network.proxy.type', 1)
        firefox_opts.set_preference('network.proxy.http', host)
        firefox_opts.set_preference('network.proxy.http_port', int(port))
        firefox_opts.set_preference('network.proxy.ssl', host)
        firefox_opts.set_preference('network.proxy.ssl_port', int(port))
        firefox_opts.set_preference('general.useragent.override', self.get_agent())
        if self.is_headless:
            firefox_opts.add_argument('--headless')
            firefox_opts.add_argument('--headless')
            firefox_opts.add_argument('-disable-gpu')
            firefox_opts.add_argument('--window-size=1920,1080')
            firefox_opts.add_argument('--no-sandbox')
            firefox_opts.add_argument('--disable-dev-shm-usage')

        print('searching with socket: %s:%s' % proxy)
        self.browser = webdriver.Firefox(options=firefox_opts)
        self.browser.set_page_load_timeout(30.0)
        self.browser.get('https://www.duckduckgo.com')
        random_sleep()
        assert 'DuckDuckGo' in self.browser.title

        for search_box in self.browser.find_elements(By.TAG_NAME, 'input'):
            if search_box.get_attribute('type') == 'text':
                search_box.send_keys(self.keyword)
                break
        else:
            raise RuntimeError('failed to locate input tag search box')

        random_sleep(short=True)
        search_box.send_keys(Keys.RETURN)
        random_sleep()

        # Search until the desired URL is found
        page_index = 0
        link_url = ''
        while not link_url:
            if page_index > self.page_index_max:
                raise RuntimeError('search results exceeded max page index')
            for anchor in self.browser.find_elements(By.TAG_NAME, 'a'):
                link = anchor.get_attribute('href')
                if link is not None and self.url in link:
                    link_url = link
                    break
            else:
                page_index += 1
                self.browser.find_element(By.ID, 'more-results').click()
                random_sleep(short=True)

        # Found target page if at this point
        print('found %s at search index %d' % (link_url, page_index + 1))
        random_sleep(short=True)
        self.browser.get(link_url)
        random_sleep()

        page_links = [anchor for anchor in self.browser.find_elements(By.TAG_NAME, 'a')
                      if anchor.get_attribute('href') is not None
                      and 'mailto' not in anchor.get_attribute('href')
                      and 'https' in anchor.get_attribute('href')
                      and anchor.get_attribute('href') != self.browser.current_url
                      and 'google.com' not in anchor.get_attribute('href')]

        random_sleep(short=True)
        page_links[randint(0, len(page_links) - 1)].click()
        random_sleep()
        print('Visited %s' % self.browser.current_url)

    def start_search(self):
        self.scrape_sockets()
        for proxy in self.proxies:
            try:
                self.search(proxy)
            except KeyboardInterrupt:
                raise
            except Exception as error:
                print(error)
                print('trying next socket...')
            finally:
                if self.browser is not None:
                    self.browser.close()
