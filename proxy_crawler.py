#! /usr/bin/python3
# rootVIII | proxy_crawler.py
from sys import exit
from threading import Thread
from crawler.crawl import ProxyCrawler, HeadlessProxyCrawler
from crawler.arguments import ArgParser


def main():
    while True:
        if not args.headless:
            bot = ProxyCrawler(args.url, args.keyword)
        else:
            bot = HeadlessProxyCrawler(args.url, args.keyword)
        bot.start_search()


if __name__ == "__main__":
    args = ArgParser().get_args()
    if 'https://' not in args.url:
        print('Include protocol in URL: https://')
        exit(1)
    try:
        thread = Thread(target=main)
        thread.daemon = True
        thread.start()
        thread.join()
    except KeyboardInterrupt:
        print('\nExiting\n')
