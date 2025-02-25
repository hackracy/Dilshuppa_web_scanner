import requests
import subprocess
import socket
import whois
import ssl
import OpenSSL
import dns.resolver
from urllib.parse import urlparse
import nmap
import re
import os

# Function to display the aesthetic startup message with the author's name
def display_intro():
    intro_message = '''
    ##################################################
    #              Dilshuppa Web Scanner             #
    #               Author: DILSHUPPA                #
    #    linkedIn : linkedin.com/in/dilshuppa        #
    ##################################################
    '''
    print(intro_message)
    print("Don't Misuse your Hacking skills, Hacking is an Art. So try to respect It! \n")
    print("to contact the Auther just google : dilshuppa")
# Function to get subdomains (using sublist3r)
def get_subdomains(domain):
    try:
        result = subprocess.run(['sublist3r', '-d', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subdomains = result.stdout.decode('utf-8').splitlines()
        return subdomains
    except Exception as e:
        print(f"Error fetching subdomains: {e}")
        return []

# Function to perform directory brute-forcing using dirsearch
def get_directories(domain, subdomain):
    wordlist = '/path/to/wordlist.txt'  # Specify your wordlist
    cmd = f"python3 dirsearch.py -u {subdomain} -w {wordlist}"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    directories = result.stdout.decode('utf-8').splitlines()
    return directories

# Function to check content length of a URL
def check_content_length(url):
    try:
        response = requests.get(url)
        return len(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL content: {e}")
        return 0

# Function for DNS lookup (A, MX, NS, TXT records)
def dns_lookup(domain):
    try:
        records = {}
        records['A'] = dns.resolver.resolve(domain, 'A')
        records['MX'] = dns.resolver.resolve(domain, 'MX')
        records['NS'] = dns.resolver.resolve(domain, 'NS')
        records['TXT'] = dns.resolver.resolve(domain, 'TXT')
        return records
    except Exception as e:
        print(f"Error performing DNS lookup: {e}")
        return {}

# Function to perform Whois lookup
def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        print(f"Error performing WHOIS lookup: {e}")
        return None

# Function to get SSL certificate details
def get_ssl_info(domain):
    try:
        cert = ssl.get_server_certificate((domain, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        return {
            'subject': x509.get_subject(),
            'issuer': x509.get_issuer(),
            'notBefore': x509.get_notBefore().decode(),
            'notAfter': x509.get_notAfter().decode()
        }
    except Exception as e:
        print(f"Error fetching SSL info: {e}")
        return None

# Function to get HTTP headers
def get_http_headers(subdomain):
    try:
        response = requests.get(f'http://{subdomain}')
        return response.headers
    except requests.exceptions.RequestException as e:
        print(f"Error fetching HTTP headers for {subdomain}: {e}")
        return {}

# Function to check open ports with Nmap
def scan_open_ports(subdomain):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=subdomain, arguments='-p 1-65535')
        open_ports = []
        for protocol in nm[subdomain].all_protocols():
            lport = nm[subdomain][protocol].keys()
            for port in lport:
                open_ports.append(port)
        return open_ports
    except Exception as e:
        print(f"Error scanning ports for {subdomain}: {e}")
        return []

# Function to run WaybackURLs (Wayback Machine URLs)
def get_waybackurls(domain):
    try:
        result = subprocess.run(['waybackurls', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        urls = result.stdout.decode('utf-8').splitlines()
        return urls
    except Exception as e:
        print(f"Error fetching Wayback URLs: {e}")
        return []

# Function to run ParamSpider
def run_paramspider(domain):
    try:
        result = subprocess.run(['python3', 'ParamSpider/paramspider.py', '--domain', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        params = result.stdout.decode('utf-8').splitlines()
        return params
    except Exception as e:
        print(f"Error running ParamSpider: {e}")
        return []

# Function to run Nuclei (vulnerability scanning)
def run_nuclei(domain):
    try:
        result = subprocess.run(['nuclei', '-u', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        vulnerabilities = result.stdout.decode('utf-8').splitlines()
        return vulnerabilities
    except Exception as e:
        print(f"Error running Nuclei: {e}")
        return []

# Main function
def main():
    display_intro()  # Show the intro message
    
    domain = input("Enter the domain: ")

    # Perform DNS Lookup
    print(f"\nPerforming DNS Lookup for {domain}:")
    dns_records = dns_lookup(domain)
    print("DNS Records (A, MX, NS, TXT):")
    for record_type, records in dns_records.items():
        print(f"{record_type}: {', '.join(str(r) for r in records)}")

    # Perform Whois Lookup
    print(f"\nPerforming WHOIS Lookup for {domain}:")
    whois_info = whois_lookup(domain)
    if whois_info:
        print(whois_info)

    # Perform SSL Info Lookup
    print(f"\nFetching SSL certificate info for {domain}:")
    ssl_info = get_ssl_info(domain)
    if ssl_info:
        print(f"Subject: {ssl_info['subject']}")
        print(f"Issuer: {ssl_info['issuer']}")
        print(f"Valid From: {ssl_info['notBefore']}")
        print(f"Valid Until: {ssl_info['notAfter']}")

    # Get Subdomains
    print(f"\nEnumerating subdomains for {domain}:")
    subdomains = get_subdomains(domain)

    for subdomain in subdomains:
        print(f"\nChecking {subdomain}")

        # Check for open ports
        open_ports = scan_open_ports(subdomain)
        print(f"Open Ports: {open_ports}")

        # Get directories
        directories = get_directories(domain, subdomain)
        for directory in directories:
            url = f"http://{subdomain}/{directory}"

            # Get Wayback URLs
            waybackurls = get_waybackurls(subdomain)
            print(f"Wayback URLs: {waybackurls}")

            # Get ParamSpider Results
            params = run_paramspider(subdomain)
            print(f"Parameters: {params}")

            # Run Nuclei for vulnerabilities
            vulnerabilities = run_nuclei(subdomain)
            print(f"Nuclei Vulnerabilities: {vulnerabilities}")

if __name__ == '__main__':
    main()
