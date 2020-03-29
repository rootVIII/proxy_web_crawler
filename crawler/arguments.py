from argparse import ArgumentParser


class ArgParser:
    def __init__(self):
        description = 'Usage: python proxy_crawler.py -u '
        description += '<https://example.com> -k <search keyword>'

        self.parser = ArgumentParser(description=description)

        self.parser.add_argument(
            '-u', '--url', required=True, help='url')

        self.parser.add_argument(
            '-k', '--keyword', required=True, help='keyword')

    def get_args(self):
        return self.parser.parse_args()
