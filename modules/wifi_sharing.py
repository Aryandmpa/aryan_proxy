import socket
import threading
import http.server
import socketserver

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"This is a simple proxy server. It does not handle requests directly.")

class WiFiSharing:
    def __init__(self, config):
        self.config = config
        self.port = self.config["wifi_sharing_port"]
        self.server = None
        self.server_thread = None

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Doesn't actually connect to anything, just gets the local IP
            s.connect(("192.255.255.255", 1))
            IP = s.getsockname()[0]
        except:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

    def start_proxy_server(self):
        if self.server_thread and self.server_thread.is_alive():
            print("Wi-Fi sharing proxy server is already running.")
            return

        host = self.get_local_ip()
        print(f"Starting Wi-Fi sharing proxy server on {host}:{self.port}...")

        try:
            # Use ThreadingTCPServer to handle multiple requests concurrently
            self.server = socketserver.ThreadingTCPServer((host, self.port), ProxyHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True  # Allow the main program to exit even if the server is running
            self.server_thread.start()
            print(f"Wi-Fi sharing proxy server started successfully on {host}:{self.port}")
            print(f"Share this address with other devices on your Wi-Fi network: {host}:{self.port}")
        except Exception as e:
            print(f"Error starting Wi-Fi sharing proxy server: {e}")
            self.server = None
            self.server_thread = None

    def stop_proxy_server(self):
        if self.server:
            print("Stopping Wi-Fi sharing proxy server...")
            self.server.shutdown()
            self.server.server_close()
            self.server_thread.join()
            self.server = None
            self.server_thread = None
            print("Wi-Fi sharing proxy server stopped.")
        else:
            print("Wi-Fi sharing proxy server is not running.")



