#!/bin/bash

echo "ok doing installs pls wait..."
sudo apt update
sudo apt install python3 python3-pip git nmap whatweb nikto curl -y

echo "installing pythons"
pip3 install requests

echo "downloading some go stuff..."

if ! command -v go &> /dev/null; then
    echo "oh no go not here... getting it"
    sudo apt install golang -y
fi

export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

echo "cloning dirsearch coz why not"
git clone https://github.com/maurosoria/dirsearch.git tools/dirsearch
ln -s $(pwd)/tools/dirsearch/dirsearch.py /usr/local/bin/dirsearch

# Installing ParamSpider
echo "Installing ParamSpider..."
git clone https://github.com/devanshbatham/ParamSpider.git
cd ParamSpider
pip3 install -r requirements.txt
cd ..

echo "ok all done. run: python3 recon_tool.py"
