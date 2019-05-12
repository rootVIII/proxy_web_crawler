#! /usr/bin/python3
from sys import exit
from time import sleep
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.keys import Keys
from re import findall, sub
from argparse import ArgumentParser
from random import randint, random
from requests import get


# Search for a given website by a string of text
# using a different proxy each iteration.
# Page indexes are printed to the console including
# final index of the site.
# Once the site is found, a random link on the site
# will be clicked.
class ProxyCrawler:
    def __init__(self, url, keyword):
        self.socket_list = []
        self.keyword = keyword
        self.url = url
        self.scrape_socket()

    # Get a list of sockets from https://www.sslproxies.org.
    # Use http lib/requests here if desired.
    def scrape_socket(self):
        string_builder = ""
        temp_browser = webdriver.Firefox()
        temp_browser.get("https://www.sslproxies.org/")
        td_tags = temp_browser.find_elements_by_tag_name('td')
        for tag in td_tags:
            string_builder += tag.text + " "
        temp_browser.quit()
        pattern = r"\d+.\d+.\d+.\d+\s+\d+"
        self.socket_list = findall(pattern, string_builder)

    # Search with the given proxy.
    # If an exception occurs, loop continues and the next proxy is used.
    def start_search(self):
        for socket in self.socket_list:
            temp_socket = socket.split()
            PROXY_HOST = temp_socket[0]
            PROXY_PORT = temp_socket[1]
            fp = webdriver.FirefoxProfile()
            fp.set_preference("network.proxy.type", 1)
            fp.set_preference("network.proxy.http", PROXY_HOST)
            fp.set_preference("network.proxy.http_port", int(PROXY_PORT))
            fp.set_preference("network.proxy.ssl", PROXY_HOST)
            fp.set_preference("network.proxy.ssl_port", int(PROXY_PORT))
            fp.set_preference("general.useragent.override", "whater_useragent")
            fp.update_preferences()
            browser = webdriver.Firefox(firefox_profile=fp)
            try:
                browser.get('https://www.bing.com/')
                assert "Bing" in browser.title
            except Exception:
                print("retrying Bing with different socket")
                browser.quit()
                continue
            print("using socket: " + PROXY_HOST + ":" + PROXY_PORT)
            print("searching for keyword(s):   " + self.keyword)
            search_box = browser.find_element_by_name("q")
            sub_button = browser.find_element_by_name("go")
            sleep(randint(20, 30) + random())
            search_box.send_keys(self.keyword)
            sleep(randint(20, 30) + random())
            sub_button.send_keys(Keys.RETURN)
            sleep(randint(20, 30) + random())
            page_index = 0
            extractor = sub(r".*//", "", self.url)
            if "www." in extractor:
                domain = extractor[4:]
            else:
                domain = extractor
            while domain not in browser.current_url:
                page_index += 1
                print("current index:   " + str(page_index))
                page_links = browser.find_elements_by_xpath("//a[@href]")
                found_link = ""
                for link in page_links:
                    try:
                        if domain in link.get_attribute("href"):
                            sleep(1)
                            found_link = link
                    except Exception:
                        print("stale element")
                        browser.quit()
                        break
                if found_link:
                    print("Found " + domain + " at index " + str(page_index))
                    found_link.click()
                sleep(5 + random())
                try:
                    if domain not in browser.current_url:
                        sleep(randint(5, 10) + random())
                        try:
                            idx = str(page_index + 1)
                            browser.find_element_by_link_text(idx).click()
                        except Exception:
                            print("Exception occurred: trying next socket")
                            browser.quit()
                            break
                    else:
                        page_index = 0
                except Exception:
                    print("Exception occurred: trying next socket")
                    browser.quit()
                    break
            sleep(randint(30, 60) + random())
            try:
                target_links = browser.find_elements_by_xpath("//a[@href]")
            except Exception:
                browser.quit()
                continue
            random_page_num = randint(0, len(target_links) - 1)
            sleep(randint(30, 60) + random())
            target_link = target_links[random_page_num]
            try:
                target_link.click()
            except Exception:
                print("Invalid target link... retrying with next socket")
                browser.quit()
                sleep(1 + random())
                continue
            sleep(randint(10, 15) + random())
            print("visiting random page:   " + browser.current_url)
            sleep(randint(30, 60) + random())
            browser.quit()


if __name__ == "__main__":
    description = 'Usage: python proxy_crawler.py -u <https://example.com> '
    description += '-k <search keyword> -d (optional - run with display)'
    parser = ArgumentParser(description=description)
    parser.add_argument('-u', '--url', required=True, help='url')
    parser.add_argument('-k', '--keyword', required=True, help='keyword')
    parser.add_argument('-d', '--display', help='display', action='store_true')
    d = parser.parse_args()
    try:
        req = get(d.url)
    except Exception as e:
        print(e)
        exit(1)
    if req.status_code != 200:
        print('Invalid URL')
        exit(1)
    if not d.display:
        with Display():
            while True:
                bot = ProxyCrawler(d.url, d.keyword)
                bot.start_search()
    else:
        while True:
            bot = ProxyCrawler(d.url, d.keyword)
            bot.start_search()
