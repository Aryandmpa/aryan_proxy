import os
import subprocess
import time
import requests

class TorIntegration:
    def __init__(self, config):
        self.config = config
        self.tor_process = None

    def _is_tor_installed(self):
        return subprocess.run(["which", "tor"], capture_output=True).returncode == 0

    def _get_tor_bridges(self):
        try:
            response = requests.get(self.config["tor_bridges_url"])
            response.raise_for_status()
            return response.text.strip().split("\n")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Tor bridges: {e}")
            return []

    def enable_tor(self):
        if not self._is_tor_installed():
            print("Tor is not installed. Please install Tor (e.g., pkg install tor) in Termux.")
            return False

        if self.tor_process and self.tor_process.poll() is None:
            print("Tor is already running.")
            return True

        print("Starting Tor...")
        tor_cmd = ["tor"]
        if self.config["tor_bridges_url"]:
            bridges = self._get_tor_bridges()
            if bridges:
                for bridge in bridges:
                    tor_cmd.extend(["--UseBridge", bridge])
                tor_cmd.append("--ClientTransportPlugin")
                tor_cmd.append("obfs4 exec /data/data/com.termux/files/usr/bin/obfs4proxy") # Assuming obfs4proxy is in Termux bin
            else:
                print("No Tor bridges found, starting Tor without bridges.")

        try:
            # Start Tor in a new process, redirecting output to avoid blocking
            self.tor_process = subprocess.Popen(tor_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(5) # Give Tor some time to start
            if self.tor_process.poll() is None:
                print("Tor started successfully.")
                self.config.set("tor_enabled", True)
                return True
            else:
                print(f"Tor failed to start. Exit code: {self.tor_process.returncode}")
                stderr_output = self.tor_process.stderr.read().decode()
                print(f"Tor stderr: {stderr_output}")
                return False
        except FileNotFoundError:
            print("Tor executable not found. Make sure it's in your PATH.")
            return False
        except Exception as e:
            print(f"An error occurred while starting Tor: {e}")
            return False

    def disable_tor(self):
        if self.tor_process and self.tor_process.poll() is None:
            print("Stopping Tor...")
            self.tor_process.terminate()
            self.tor_process.wait(timeout=10)
            if self.tor_process.poll() is not None:
                print("Tor stopped successfully.")
                self.config.set("tor_enabled", False)
                return True
            else:
                print("Failed to stop Tor gracefully, killing process.")
                self.tor_process.kill()
                self.tor_process.wait()
                self.config.set("tor_enabled", False)
                return True
        else:
            print("Tor is not running.")
            return False

    def get_tor_proxy(self):
        if self.config.get("tor_enabled"):
            return {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
        return None


