import subprocess
import os
import requests
import threading
from urllib.parse import urljoin

website = input("Enter da site name (no https lol): ").strip()
stufffolder = "results/" + website
os.makedirs(stufffolder, exist_ok=True)

def display_intro():
    intro_message = '''
    ##################################################
    #              Dilshuppa D_WebScanner            #
    #               Author: DILSHUPPA                #
    #    linkedIn : linkedin.com/in/dilshuppa        #
    ##################################################
    '''
    print(intro_message)
    print("Don't Misuse your Hacking skills, Hacking is an Art, So Hackers are Artists. try to respect them! \n")
def do_cmd(cmd, out_file=None):
    print(">>> running: " + " ".join(cmd))
    if out_file:
        with open(out_file, "w") as f:
            subprocess.run(cmd, stdout=f, stderr=f)
    else:
        subprocess.run(cmd)

def find_subs():
    print("### Finding da subs ")
    do_cmd(["subfinder", "-d", website, "-silent"], stufffolder + "/subz.txt")

def nmapscan():
    print("### lets scan open doors (nmap)")
    do_cmd(["nmap", "-sV", "-T4", website], stufffolder + "/nmapscan.txt")

def techie():
    print("### whatweb go brrrr ")
    do_cmd(["whatweb", website], stufffolder + "/tech.txt")

def nukem():
    print("### time for nuclear vuln checks ")
    do_cmd(["nuclei", "-l", stufffolder + "/subz.txt", "-silent", "-o", stufffolder + "/boom.txt"])

def dirs_brute(subz):
    print("### smashing doors on", subz)
    outputy = stufffolder + "/" + subz.replace(".", "_") + "_dirs.txt"
    do_cmd(["dirsearch", "-u", "http://" + subz, "-e", "php,html,txt", "-o", outputy])

def check_pages(subz):
    print("### checking page stuff on", subz)
    paths = ["/admin", "/login", "/robots.txt", "/secret", "/.git"]
    for p in paths:
        daurl = f"http://{subz}{p}"
        try:
            r = requests.get(daurl, timeout=5)
            print(f"{daurl} => {r.status_code}")
            if r.status_code == 403:
                print("     > 403? we try funny stuff")
                try_bypazz(daurl)
        except:
            pass

def try_bypazz(badurl):
    lol = ["/%2e/", "/..;/", "/.random", "/%20", "/;"]
    for hax in lol:
        try:
            dafun = badurl.rstrip("/") + hax
            r = requests.get(dafun, timeout=5)
            print("     >", dafun, "->", r.status_code)
        except:
            pass

def crawlz(subz):
    print("spider time ", subz)
    try:
        r = requests.get("http://" + subz, timeout=5)
        stuff = set()
        for line in r.text.splitlines():
            if 'href="' in line:
                try:
                    part = line.split('href="')[1].split('"')[0]
                    if part.startswith("/"):
                        stuff.add(urljoin("http://" + subz, part))
                except:
                    pass
        print("     > links:", len(stuff))
    except:
        pass

def run_param_spider(subz):
    print("running ParamSpider on", subz)
    param_output = stufffolder + "/" + subz.replace(".", "_") + "_params.txt"
    subprocess.run(["python3", "ParamSpider/paramspider.py", "-d", subz, "-o", param_output])

def start_thing():
    find_subs()

    with open(stufffolder + "/subz.txt") as f:
        sublist = [x.strip() for x in f if x.strip()]

    threading.Thread(target=nmapscan).start()
    threading.Thread(target=techie).start()
    threading.Thread(target=nukem).start()

    for lolsub in sublist:
        dirs_brute(lolsub)
        check_pages(lolsub)
        crawlz(lolsub)
        run_param_spider(lolsub)

if __name__ == "__main__":
    print("Be patient if you have passion.")
    start_thing()
