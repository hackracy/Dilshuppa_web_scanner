#!/bin/bash


echo " ____ ___ _     ____  _   _ _   _ ____  ____   _    
|  _ \_ _| |   / ___|| | | | | | |  _ \|  _ \ / \   
| | | | || |   \___ \| |_| | | | | |_) | |_) / _ \  
| |_| | || |___ ___) |  _  | |_| |  __/|  __/ ___ \ 
|____/___|_____|____/|_| |_|\___/|_|   |_| /_/   \_\                                                                                                                            
                                                     
"
echo "  This script is made by Dilshuppa
"

# This script will automatically set up the Dilshuppa Web Recon tool with all dependencies.

echo "Starting the setup process for Dilshuppa_web_recon..."

# Step 1: Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Step 2: Install Go if it's not installed
if ! command -v go &> /dev/null; then
    echo "Go is not installed. Installing Go..."
    # Detect OS and install Go (you can modify this for specific OS or use a pre-built installer)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y golang-go
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install go
    else
        echo "Go installation failed. Please install Go manually."
        exit 1
    fi
else
    echo "Go is already installed."
fi

# Step 3: Install WaybackURLs
echo "Installing WaybackURLs..."
go install github.com/tomnomnom/waybackurls@latest

# Step 4: Install ParamSpider
echo "Installing ParamSpider..."
git clone https://github.com/devanshbatham/ParamSpider.git
cd ParamSpider
pip install -r requirements.txt
cd ..

# Step 5: Install Nuclei
echo "Installing Nuclei..."
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Step 6: Setup complete
echo "Setup complete! You can now run the recon tool."

# Optionally, make the Python script executable
chmod +x Dilshuppa_web_recon.py

echo "To run the tool, use: python3 Dilshuppa_web_recon.py"
