import json
import os

class ConfigManager:
    def __init__(self, config_file="proxy_config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {self.config_file}. Starting with default config.")
                return self._default_config()
        return self._default_config()

    def _default_config(self):
        return {
            "rotation_interval": 300,  # seconds
            "geonode_api_url": "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
            "proxy_file_path": "proxies.json",
            "proxy_cache_file": "proxy_cache.json",
            "tor_enabled": False,
            "tor_bridges_url": "https://bridges.torproject.org/bridges?transport=obfs4",
            "log_file": "ip_alchemist.log",
            "wifi_sharing_port": 8080,
            "user_agent_file": "user_agents.txt",
            "favorites": [],
            "history": [],
            "last_session_state": {}
        }

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def add_favorite_proxy(self, proxy_address):
        if proxy_address not in self.config["favorites"]:
            self.config["favorites"].append(proxy_address)
            self.save_config()

    def remove_favorite_proxy(self, proxy_address):
        if proxy_address in self.config["favorites"]:
            self.config["favorites"].remove(proxy_address)
            self.save_config()

    def add_to_history(self, proxy_address):
        if proxy_address not in self.config["history"]:
            self.config["history"].append(proxy_address)
            # Keep history size manageable, e.g., last 50
            self.config["history"] = self.config["history"][-50:]
            self.save_config()

    def update_session_state(self, key, value):
        self.config["last_session_state"][key] = value
        self.save_config()

    def get_session_state(self, key, default=None):
        return self.config["last_session_state"].get(key, default)

    def clear_cache(self):
        if os.path.exists(self.config["proxy_cache_file"]):
            os.remove(self.config["proxy_cache_file"])
            print("Proxy cache cleared.")



