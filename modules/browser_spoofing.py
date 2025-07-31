import random
import os

class BrowserSpoofing:
    def __init__(self, config):
        self.config = config
        self.user_agents = self._load_user_agents()

    def _load_user_agents(self):
        user_agent_file = self.config["user_agent_file"]
        if os.path.exists(user_agent_file):
            with open(user_agent_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        else:
            print(f"User agent file not found: {user_agent_file}. Generating a default one.")
            # Create a default user_agents.txt if it doesn't exist
            default_user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
                "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
            ]
            with open(user_agent_file, "w") as f:
                for ua in default_user_agents:
                    f.write(ua + "\n")
            return default_user_agents

    def get_random_user_agent(self):
        if not self.user_agents:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36" # Fallback
        return random.choice(self.user_agents)

    def generate_fingerprint(self):
        # This is a simplified example. Real browser fingerprinting is complex.
        # It involves canvas, WebGL, audio, fonts, screen resolution, etc.
        # For a basic spoofing, we can randomize some common properties.
        screen_resolutions = ["1920x1080", "1366x768", "1440x900", "1536x864"]
        languages = ["en-US,en;q=0.9", "en-GB,en;q=0.9", "fr-FR,fr;q=0.9"]
        platform = random.choice(["Win32", "Linux x86_64", "MacIntel"])

        return {
            "screen_resolution": random.choice(screen_resolutions),
            "language": random.choice(languages),
            "platform": platform,
            "hardware_concurrency": random.randint(2, 16),
            "device_memory": random.choice([2, 4, 8, 16]),
            "vendor": "Google Inc.", # Common for Chrome
            "renderer": "ANGLE (NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)" # Example, should be more dynamic
        }

    def generate_profile(self, profile_name=None):
        profile = {
            "user_agent": self.get_random_user_agent(),
            "fingerprint": self.generate_fingerprint()
        }
        if profile_name:
            print(f"Generated browser profile \'{profile_name}\': {profile}")
        else:
            print(f"Generated browser profile: {profile}")
        return profile


