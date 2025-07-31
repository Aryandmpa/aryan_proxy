import os

class Config:
    def __init__(self):
        self.config = {
            "rotation_interval": 300,  # seconds
            "geonode_api_url": "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
            "proxy_file_path": "proxies.json",
            "proxy_cache_file": "proxy_cache.json",
            "tor_enabled": False,
            "tor_bridges_url": "https://bridges.torproject.org/bridges?transport=obfs4",
            "log_file": "ip_alchemist.log",
            "wifi_sharing_port": 8080,
            "user_agent_file": "user_agents.txt",
            "config_file": "proxy_config.json"
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config["config_file"]):
            with open(self.config["config_file"], "r") as f:
                self.config.update(json.load(f))

    def save_config(self):
        with open(self.config["config_file"], "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()


