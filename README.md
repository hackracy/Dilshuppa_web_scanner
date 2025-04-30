** D_WebScanner

D_WebScanner is a simple web reconnaissance tool that automates subdomain discovery, port scanning, directory brute-forcing, and vulnerability scanning.

Features

Discover subdomains of a target domain.
Scan for open ports and services.
Identify web technologies used.
Brute-force directories on subdomains.
Discover query parameters using ParamSpider.
Scan for vulnerabilities using Nuclei.
Installation

Clone the repository:
git clone https://github.com/yourusername/D_WebScanner.git
cd D_WebScanner
Run the Dilshuppa.sh setup script:
chmod +x Dilshuppa.sh
./Dilshuppa.sh
Usage

Run the tool:
python3 D_WebScanner.py
Enter the target domain (e.g., example.com).
The tool will:

Find subdomains.
Perform scans (Nmap, WhatWeb, Nikto).
Brute-force directories (using Dirsearch).
Discover parameters (using ParamSpider).
Perform vulnerability scanning (using Nuclei).
Results are saved in the results/{domain} directory.

Requirements

Python 3.x
Go (installed by the Dilshuppa.sh script)
Disclaimer

This tool is for educational purposes only. Always get permission before scanning websites or networks.
