from argparse import ArgumentParser
from random import randint, random
from time import sleep


def get_cli_args():
    description = 'Usage: python proxy_crawler.py -u '
    description += '<https://example.com> -k <search keyword>'
    parser = ArgumentParser(description=description)
    parser.add_argument('-u', '--url',
                        required=True,
                        help='target URL including https://')
    parser.add_argument('-k', '--keyword',
                        required=True,
                        help='keyword(s) to search for')
    parser.add_argument('-x', '--headless',
                        required=False,
                        action='store_true',
                        help='run crawler withou GUI (command prompt only)')
    return parser.parse_args()


def random_sleep(short: bool = False):
    sleep(randint(30, 60) + random()) if not short else sleep(randint(5, 10) + random())
