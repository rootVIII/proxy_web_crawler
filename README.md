### Search for a website with a different proxy each time
This script automates the process of searching for a website via keyword
and the Bing search engine.... page after page
<br><br>
Pass a complete URL and at least 1 keyword as command line arguments:
<br>
<code>python proxy_crawler.py -u https://www.example.com -k keyword</code>
<br><br>
<code>python proxy_crawler.py -u https://www.whatsmyip.org -k "my ip"</code>
<br><br>
Run headless (no GUI):
<br>
<code>python proxy_crawler.py -u https://www.whatsmyip.org -k "my ip" -x</code>
<br><br>
<ul>
    <li>
        A list of proxies from the web are scraped first
        using <a href="https://www.sslproxies.org">sslproxies.org</a>
    </li>
    <li>
        Then using a new proxy socket for each iteration, the specified <b>keyword(s)</b>
        is searched for via Bing until the desired <b>website</b> is found
    </li>
    <li>
        The website is then visited, and one random link is clicked within the website
    </li>
    <li>
        The bot is slowed down on purpose, but will also run fairly slow due to proxy connection
    </li>
</ul>
<hr>
<ul>
    <li>
        Requirements: python3, selenium, Firefox browser, and geckodriver
    </li>
    <li>
        Download the latest geckodriver from <a href="https://github.com/mozilla/geckodriver/releases">Mozilla</a>
    </li>
    <li>
        Unzip the file and place geckodriver into the geckodriver/ directory
    </li>
    <li>
        Ensure selenium is installed: <code>pip install -r requirements.txt</code>
    </li>
</ul>

<hr>
<img src="https://github.com/rootVIII/proxy_web_crawler/blob/master/sc.png" alt="screenshot" height="675" width="700">
<hr>
This was developed on Ubuntu 16.04.4 LTS with selenium/geckodriver and firefox 60.0
<br>
<b>Author: rootVIII  2018-2020</b>
