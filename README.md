## search for a website with a different proxy each time
This script automates the process of searching for a website via keyword
and the Bing search engine.... page after page
<br><br>
Pass a complete URL and at least 1 keyword as command line arguments:
<br>
<code>python proxy_crawler.py -u https://www.example.com -k keyword</code>
<br><br>
<code>python proxy_crawler.py -u https://www.whatsmyip.org -k "my ip"</code>
<br><br>
If on a Linux system, proxy_crawler can run headless. Give the -x option (requires XVFB):
<br>
<code>python proxy_crawler.py -u https://www.whatsmyip.org -k "my ip" -x</code>
<br><br>
<ul>
    <li>
        It first scrapes a list of proxies from the web
        using <a href="https://www.sslproxies.org">SSL Proxies</a>
    </li>
    <li>
        Then using a new proxy socket for each iteration, the specified <b>keyword(s)</b>
        is searched for via Bing until the desired <b>website</b> is found
    </li>
    <li>
        The website is then visited, and one random link is clicked within the website
    </li>
    <li>
        The bot is slowed down on purpose
    </li>   
    <li>
        If searching with multiple keywords, wrap them in quotes: "example search phrase"
    </li>
</ul>
<br>
Along with Python 3 and geckodriver, the following are also required:
<pre>
    <code>
pip install selenium
apt-get install xvfb (Linux only)
    </code>
</pre>
<br><br>
proxy_crawler.py passes pep8/pycodestyle
<br><br>
I use this version of geckodriver on Ubuntu:
<br><br>
<code>wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz</code>
<br><br>
geckodriver should be unzipped and saved somewhere in your PATH... ie: <code>/usr/local/bin</code>
<hr>
<img src="https://github.com/rootVIII/proxy_web_crawler/blob/master/sc.png" alt="screenshot" height="675" width="700"><hr>
<hr>
This was developed on Ubuntu 16.04.4 LTS with selenium/geckodriver and firefox 60.0
<br>
Also tested on Ubuntu 18.04
<br>
<b>Author: rootVIII  2018-2020</b>
