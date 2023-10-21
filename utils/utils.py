from argparse import ArgumentParser


def get_cli_args():
    description = 'Usage: python proxy_crawler.py -u '
    description += '<https://example.com> -k <search keyword>'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        '-u', '--url', required=True, help='Target URL including https://')
    parser.add_argument(
        '-k', '--keyword', required=True, help='keyword(s) to search for')
    parser.add_argument(
        '-x', '--headless', required=False,
        action='store_true', help='requires pyvirtualdisplay & Linux OS')
    return parser.parse_args()
