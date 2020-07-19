#!/bin/sh
# download and install latest geckodriver for linux or mac.
# required for selenium to drive a firefox browser.

install_dir="/usr/local/bin"
version=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
if [[ $(uname) == "Darwin" ]]; then
    url=https://chromedriver.storage.googleapis.com/$version/chromedriver_mac64.zip
elif [[ $(uname) == "Linux" ]]; then
    url=https://chromedriver.storage.googleapis.com/$version/chromedriver_linux64.zip
else
    echo "can't determine OS"
    exit 1
fi
echo "url => $url"
curl -o chromedriver.zip "$url"
unzip chromedriver.zip
rm -f chromedriver.zip
chmod +x chromedriver
sudo mv chromedriver "$install_dir"
echo "installed chromedriver binary in $install_dir"