#! /usr/bin/python3
# James Loye Colley
# 22MAY2018
# https://www.roboshout.com

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
import random
import re
import pyautogui


class ProxyCrawler:
    def __init__(self, socket_list=[]):
        self.__scrape_socket()
        self.keyword = ""
        self.pages = [
            "Robocall Extensions", "Youtube Call",
            "Mass Robocalls", "Robocall Recorder (Portal)",
            "Text (Send/Receive)", "Twenty Texts", "Robocall",
            "Text Bombardment", "Mass-Texts", "Text Blaster",
            "Free Anonymous Call", "Free Anonymous Text"
        ]

    def __set_keyword(self):
        keywords = [
            "anonymous robot call", "send anonymous text", "send 1000 texts"
            "online text roboshout", "anonymous sms", "free text roboshout",
            "free call roboshout", "anonymous online call", "receive sms online",
            "text from computer", "internet text", "send a text", "call recorder",
            "send online text", "anonymous text", "make a robocall", "roboshout sms",
            "robocall roboshout", "roboshout send text", "online call roboshout",
            "free online text",  "anonymous mms", "robocall", "anonymous call",
            "send and receive anonymous texts", "youtube call", "robot call"
        ]
        search_term = random.randint(0, 24)
        self.keyword = keywords[search_term]

    def __scrape_socket(self):
        string_builder = ""
        browser1 = webdriver.Firefox()
        browser1.get("https://www.sslproxies.org/")
        time.sleep(2)
        td_tags = browser1.find_elements_by_tag_name('td')
        for tag in td_tags:
            string_builder += tag.text + " "
        browser1.quit()
        self.socket_list = re.findall("\d+.\d+.\d+.\d+\s+\d+", string_builder)

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
            browser2 = webdriver.Firefox(firefox_profile=fp)
            try:
                browser2.get('https://www.bing.com/')
                assert "Bing" in browser2.title
            except:
                print("retrying Bing with different socket")
                browser2.quit()
                continue
            self.__set_keyword()
            print("\n--------------------------------------------")
            print("using socket: " + PROXY_HOST + ":" + PROXY_PORT)
            print("searching for keyword(s):   " + self.keyword)
            time.sleep(random.randint(30, 60) + random.random())
            pyautogui.typewrite(self.keyword)
            time.sleep(random.randint(30, 60) + random.random())
            pyautogui.press('enter')
            time.sleep(random.randint(20, 30) + random.random())
            page_index = 0
            while not "roboshout.com" in browser2.current_url:
                page_index += 1
                try:
                    selected_link = browser2.find_element_by_partial_link_text("Roboshout").click()
                except:
                    print("current page index:   " + str(page_index))
                time.sleep(random.randint(20, 30) + random.random())
                if "roboshout.com" in browser2.current_url:
                    print("https://www.roboshout.com found at index:   " + str(page_index))
                    page_selection = random.randint(0, 11)
                    try:
                        link = browser2.find_element_by_link_text(self.pages[page_selection])
                        link.click()
                        print(browser2.current_url)
                        time.sleep(random.randint(30, 100) + random.random())
                    except:
                        print("could not find a link")
                else:
                    time.sleep(random.randint(2, 6) + random.random())
                    browser2.find_element_by_link_text(str(page_index + 1)).click()
            browser2.quit()


if __name__ == "__main__":
    bot = ProxyCrawler()
    while True:
        bot.start_search()
