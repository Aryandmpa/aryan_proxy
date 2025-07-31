import json
import time
import threading
import random
import requests

class ProxyManager:
    def __init__(self, config):
        self.config = config
        self.proxies = []
        self.current_proxy_index = -1
        self.rotation_thread = None
        self.running = False

    def load_proxies_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            # Assuming the API returns a list of dictionaries with 'ip' and 'port' keys
            self.proxies = [f"http://{p['ip']}:{p['port']}" for p in data['data']]
            print(f"Loaded {len(self.proxies)} proxies from URL: {url}")
            self.cache_proxies()
        except requests.exceptions.RequestException as e:
            print(f"Error loading proxies from URL {url}: {e}")
            self.load_proxies_from_cache()

    def load_proxies_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.proxies = [f"http://{p['ip']}:{p['port']}" for p in data]
            print(f"Loaded {len(self.proxies)} proxies from file: {file_path}")
        except FileNotFoundError:
            print(f"Proxy file not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")

    def cache_proxies(self):
        with open(self.config['proxy_cache_file'], 'w') as f:
            json.dump([{'ip': p.split('//')[1].split(':')[0], 'port': p.split(':')[2]} for p in self.proxies], f)

    def load_proxies_from_cache(self):
        try:
            with open(self.config['proxy_cache_file'], 'r') as f:
                data = json.load(f)
                self.proxies = [f"http://{p['ip']}:{p['port']}" for p in data]
            print(f"Loaded {len(self.proxies)} proxies from cache.")
        except FileNotFoundError:
            print("Proxy cache file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON from cache file.")

    def get_next_proxy(self):
        if not self.proxies:
            print("No proxies available.")
            return None
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return {'http': self.proxies[self.current_proxy_index], 'https': self.proxies[self.current_proxy_index]}

    def rotate_proxy(self):
        while self.running:
            next_proxy = self.get_next_proxy()
            if next_proxy:
                print(f"Rotating to new proxy: {next_proxy['http']}")
                # Here you would typically update the system's proxy settings
                # For Termux, this might involve setting environment variables
            time.sleep(self.config['rotation_interval'])

    def start_rotation(self):
        if not self.running:
            self.running = True
            self.rotation_thread = threading.Thread(target=self.rotate_proxy)
            self.rotation_thread.daemon = True
            self.rotation_thread.start()
            print("Proxy rotation started.")

    def stop_rotation(self):
        if self.running:
            self.running = False
            if self.rotation_thread and self.rotation_thread.is_alive():
                self.rotation_thread.join()
            print("Proxy rotation stopped.")

    def test_proxy(self, proxy):
        try:
            # Test with a known good URL, e.g., Google
            response = requests.get('http://www.google.com', proxies=proxy, timeout=5)
            if response.status_code == 200:
                print(f"Proxy {proxy['http']} is working.")
                return True
            else:
                print(f"Proxy {proxy['http']} returned status code {response.status_code}.")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Proxy {proxy['http']} failed: {e}")
            return False

    def find_working_proxy(self):
        random.shuffle(self.proxies)
        for proxy_url in self.proxies:
            proxy = {'http': proxy_url, 'https': proxy_url}
            if self.test_proxy(proxy):
                return proxy
        return None


