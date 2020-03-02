#!/bin/bash
sudo apt update
sudo apt install python3-pip curl jq -y
sudo pip3 install -r requirements.txt # install python3 dependency packages
# ===== Ubuntu 18.04 LTS need this =====
sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py --force-reinstall
sudo rm get-pip.py # remove it after re-install
# ======================================

# fetch from https://gist.github.com/diemol/635f450672b5bf80420d595ca0016d20
#sudo bash geckodriver-install.sh
#sudo bash chromedriver-install.sh