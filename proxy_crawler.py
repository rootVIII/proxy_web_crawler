# rootVIII | proxy_crawler.py
from os import path
from pathlib import Path
from sys import exit
from utils.web_crawler import ProxyCrawler
from utils.utils import get_cli_args


def main(url: str, keyword: str, is_headless: bool):
    project_path = str(Path(__file__).parent)
    with open(path.join(project_path, 'user-agents.txt')) as file_in:
        user_agents = [line.strip() for line in file_in.readlines() if line.strip()]
    if not user_agents:
        raise RuntimeError('missing user-agents in user-agents.txt')

    while True:
        bot = ProxyCrawler(url, keyword, is_headless, user_agents)
        print('searching for %s keyword(s):  %s' % (url, keyword))
        bot.start_search()


if __name__ == "__main__":
    args = get_cli_args()
    if args.url[:8] != 'https://':
        print('include protocol in URL: https://')
        exit(1)
    try:
        main(args.url, args.keyword, args.headless)
    except KeyboardInterrupt:
        print('exiting...\n')
        exit()
    except Exception as err:
        print('encountered error, exiting...')
        print(err)
        exit(1)
