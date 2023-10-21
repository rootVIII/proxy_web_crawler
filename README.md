### Search for a website with a different proxy each time
This script automates the process of searching for a website via keyword
and the DuckDuckGo search engine.... page after page
<br><br>
Pass a complete URL and at least 1 keyword as command line arguments to run program:
<br>
<code>python proxy_crawler.py -u &lt;url&gt; -k &lt;keyword(s)&gt;</code>
<br>
<code>python proxy_crawler.py -u "https://www.whatsmyip.org" -k "my ip"</code>
<br><br>
Add the -x option to run headless (no GUI):
<br>
<code>python proxy_crawler.py -u "https://www.whatsmyip.org" -k "my ip" -x</code>
<br>
<ul>
    <li>
        A list of proxies from the web are scraped first
        using <a href="https://www.sslproxies.org">sslproxies.org</a>
    </li>
    <li>
        Then using a new proxy socket for each iteration, the specified <b>keyword(s)</b>
        is searched for until the desired <b>website</b> is found
    </li>
    <li>
        The website is then visited, and one random link is clicked within the website
    </li>
    <li>
        The bot is slowed down on purpose, but will also run fairly slow due to proxy connection
    </li>
    <li>
        Browser windows may open and close repeatedly during runtime (due to connection errors) until a healthy/valid proxy is encountered
    </li>
</ul>
<hr>
<ul>
    <li>
        Requirements:
        <ul>
            <li>
                python3
            </li>
            <li>
                selenium
            </li>
            <li>
                Firefox browser
            </li>
            <li>
                geckodriver
            </li>
        </ul>
    </li>
    <li>
        Download the latest geckodriver from <a href="https://github.com/mozilla/geckodriver/releases">Mozilla</a>
    </li>
    <li>
        Unzip the file and place geckodriver into your path
    </li>
    <li>
        Ensure selenium is installed: <code>pip install -r requirements.txt</code>
    </li>
</ul>

<hr>
<img src="https://user-images.githubusercontent.com/30498791/277134161-e2cec5a4-c64a-4a47-a5d8-39b81aea8522.png" alt="screenshot1">
<br><br>
<img src="https://user-images.githubusercontent.com/30498791/277134162-76fe4626-1d57-452a-940d-8a6030850e2b.png" alt="screenshot2">
<br><br>
<img src="https://user-images.githubusercontent.com/30498791/277134163-70c4ab50-5582-4b5c-97a8-0ff96fbf9a76.png" alt="screenshot3">
<hr>
<b>Author: rootVIII  2018-2023</b>
