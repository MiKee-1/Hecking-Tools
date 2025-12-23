import requests
import threading

def check_subdomains(subdomain):
    url = f'http://{subdomain}.{domain}'
    try:
        requests.get(url)
    except requests.ConnectionError:
        pass
    else:
        print("[+] last discorvered subdomain: "+url)
        with lock:
            discovered_subdomains.append(url)

domain = 'youtube.com'

with open('DNS_ENUM\subdomains.txt') as file:
    subdomains = file.read().splitlines()

discovered_subdomains = []
lock = threading.Lock()
threads = []

for subdomain in subdomains:
    thread = threading.Thread(target = check_subdomains, args=(subdomain,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

with open("DNS_ENUM\discovered_subdomain.txt", 'w') as f:
    for subdomain in discovered_subdomains:
        print(subdomain, file=f)
