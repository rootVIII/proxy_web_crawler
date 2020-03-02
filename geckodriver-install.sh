#!/bin/sh
# download and install latest geckodriver for linux or mac.
# required for selenium to drive a firefox browser.

install_dir="/usr/local/bin"

# fetch latest version download url
json=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest)
if [[ $(uname) == "Darwin" ]]; then
    url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("macos"))')
elif [[ $(uname) == "Linux" ]]; then
    url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("linux64"))')
else
    echo "can't determine OS"
    exit 1
fi

# if you don't wanna use the latest version
# you can also comment out the section to get the latest version
# and set $url as tested version

# $url = https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz #set $url as tested version
sudo curl -s -L "$url" | tar -xz
sudo chmod +x geckodriver
sudo mv geckodriver "$install_dir"
echo "installed geckodriver binary in $install_dir"