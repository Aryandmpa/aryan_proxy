#!/usr/bin/env python3
"""
Aryan Proxy: Advanced Proxy Management for Termux
Version: PROFESSIONAL v8.1
Author: Aryan
"""

import sys
import os
import time
import json
from modules.config_manager import ConfigManager
from modules.proxy_manager import ProxyManager
from modules.tor_integration import TorIntegration
from modules.wifi_sharing import WiFiSharing
from modules.browser_spoofing import BrowserSpoofing
from modules.logger import Logger

class AryanProxy:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.logger = Logger(self.config_manager.get("log_file"))
        self.proxy_manager = ProxyManager(self.config_manager.config)
        self.tor_integration = TorIntegration(self.config_manager.config)
        self.wifi_sharing = WiFiSharing(self.config_manager.config)
        self.browser_spoofing = BrowserSpoofing(self.config_manager.config)
        
        self.logger.info("Aryan Proxy initialized successfully.")

    def display_banner(self):
        banner = """
        ╔═══════════════════════════════════════════════════════════════╗
        ║                         ARYAN PROXY                          ║
        ║                   PROFESSIONAL v8.1                          ║
        ║                                                               ║
        ║         Advanced Proxy Management for Termux                 ║
        ║                                                               ║
        ║  Features:                                                    ║
        ║  • Auto IP Changer with Scheduled Rotation                   ║
        ║  • Multiple Proxy Sources (GeoNode, Files, Tor)              ║
        ║  • Wi-Fi Sharing for Other Devices                           ║
        ║  • Browser Spoofing & Fingerprint Management                 ║
        ║  • Persistent Configuration & Logging                        ║
        ║                                                               ║
        ╚═══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def display_menu(self):
        print("\n" + "="*60)
        print("                    MAIN MENU")
        print("="*60)
        print("1. Auto Tor IP Changer")
        print("2. URL-loaded Proxy Links (GeoNode)")
        print("3. Load Proxies from File")
        print("4. Start Wi-Fi Sharing")
        print("5. Stop Wi-Fi Sharing")
        print("6. Generate Browser Profile")
        print("7. View Current Configuration")
        print("8. View Proxy History")
        print("9. Clear Cache")
        print("10. Exit")
        print("="*60)

    def handle_tor_option(self):
        print("\n--- Tor Integration ---")
        if self.config_manager.get("tor_enabled"):
            print("Tor is currently enabled.")
            choice = input("Do you want to disable Tor? (y/n): ").lower()
            if choice == 'y':
                if self.tor_integration.disable_tor():
                    print("Tor disabled successfully.")
                    self.logger.activity("TOR_DISABLED", "User disabled Tor integration")
        else:
            print("Tor is currently disabled.")
            choice = input("Do you want to enable Tor? (y/n): ").lower()
            if choice == 'y':
                if self.tor_integration.enable_tor():
                    print("Tor enabled successfully.")
                    self.logger.activity("TOR_ENABLED", "User enabled Tor integration")
                    self.proxy_manager.start_rotation()

    def handle_geonode_option(self):
        print("\n--- GeoNode Proxy Source ---")
        url = self.config_manager.get("geonode_api_url")
        print(f"Current URL: {url}")
        
        choice = input("Do you want to change the URL? (y/n): ").lower()
        if choice == 'y':
            new_url = input("Enter new GeoNode API URL: ")
            self.config_manager.set("geonode_api_url", new_url)
            url = new_url
        
        print("Loading proxies from GeoNode...")
        self.proxy_manager.load_proxies_from_url(url)
        self.logger.activity("PROXY_LOADED", f"Loaded proxies from GeoNode: {url}")
        
        # Find and display a working proxy
        working_proxy = self.proxy_manager.find_working_proxy()
        if working_proxy:
            print(f"Found working proxy: {working_proxy['http']}")
            host_port = working_proxy['http'].replace('http://', '')
            print(f"Host and Port for sharing: {host_port}")
            self.config_manager.add_to_history(working_proxy['http'])
        
        # Start rotation
        choice = input("Start automatic rotation? (y/n): ").lower()
        if choice == 'y':
            self.proxy_manager.start_rotation()
            print("Automatic proxy rotation started.")

    def handle_file_option(self):
        print("\n--- Load Proxies from File ---")
        file_path = input("Enter the path to your proxy file (JSON format): ")
        if os.path.exists(file_path):
            self.proxy_manager.load_proxies_from_file(file_path)
            self.logger.activity("PROXY_LOADED", f"Loaded proxies from file: {file_path}")
            
            # Find and display a working proxy
            working_proxy = self.proxy_manager.find_working_proxy()
            if working_proxy:
                print(f"Found working proxy: {working_proxy['http']}")
                host_port = working_proxy['http'].replace('http://', '')
                print(f"Host and Port for sharing: {host_port}")
                self.config_manager.add_to_history(working_proxy['http'])
        else:
            print("File not found!")

    def handle_wifi_start(self):
        print("\n--- Start Wi-Fi Sharing ---")
        self.wifi_sharing.start_proxy_server()
        self.logger.activity("WIFI_SHARING_STARTED", f"Wi-Fi sharing started on port {self.config_manager.get('wifi_sharing_port')}")

    def handle_wifi_stop(self):
        print("\n--- Stop Wi-Fi Sharing ---")
        self.wifi_sharing.stop_proxy_server()
        self.logger.activity("WIFI_SHARING_STOPPED", "Wi-Fi sharing stopped")

    def handle_browser_profile(self):
        print("\n--- Generate Browser Profile ---")
        profile_name = input("Enter profile name (optional): ")
        profile = self.browser_spoofing.generate_profile(profile_name if profile_name else None)
        self.logger.activity("BROWSER_PROFILE_GENERATED", f"Generated browser profile: {profile_name or 'unnamed'}")

    def handle_view_config(self):
        print("\n--- Current Configuration ---")
        config = self.config_manager.config
        for key, value in config.items():
            if key not in ["favorites", "history", "last_session_state"]:
                print(f"{key}: {value}")

    def handle_view_history(self):
        print("\n--- Proxy History ---")
        history = self.config_manager.get("history", [])
        if history:
            for i, proxy in enumerate(history, 1):
                print(f"{i}. {proxy}")
        else:
            print("No proxy history found.")

    def handle_clear_cache(self):
        print("\n--- Clear Cache ---")
        self.config_manager.clear_cache()
        self.logger.activity("CACHE_CLEARED", "User cleared proxy cache")

    def run(self):
        self.display_banner()
        
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (1-10): ").strip()
                
                if choice == '1':
                    self.handle_tor_option()
                elif choice == '2':
                    self.handle_geonode_option()
                elif choice == '3':
                    self.handle_file_option()
                elif choice == '4':
                    self.handle_wifi_start()
                elif choice == '5':
                    self.handle_wifi_stop()
                elif choice == '6':
                    self.handle_browser_profile()
                elif choice == '7':
                    self.handle_view_config()
                elif choice == '8':
                    self.handle_view_history()
                elif choice == '9':
                    self.handle_clear_cache()
                elif choice == '10':
                    print("\nThank you for using Aryan Proxy!")
                    self.logger.activity("APPLICATION_EXIT", "User exited application")
                    # Clean up
                    self.proxy_manager.stop_rotation()
                    self.wifi_sharing.stop_proxy_server()
                    self.tor_integration.disable_tor()
                    break
                else:
                    print("Invalid choice! Please enter a number between 1-10.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nExiting Aryan Proxy...")
                self.logger.activity("APPLICATION_INTERRUPTED", "User interrupted application")
                # Clean up
                self.proxy_manager.stop_rotation()
                self.wifi_sharing.stop_proxy_server()
                self.tor_integration.disable_tor()
                break
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = AryanProxy()
    app.run()

