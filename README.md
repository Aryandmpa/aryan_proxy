# Aryan Proxy: Advanced Proxy Management for Termux

## Project Overview

Aryan Proxy is a comprehensive and versatile proxy management tool designed specifically for Termux users. It provides robust features for automatic IP changing, integration with various proxy sources (including Tor), Wi-Fi sharing capabilities, and advanced browser spoofing. This tool aims to offer a high-security, user-friendly solution for managing network anonymity and accessibility directly from your Termux environment, without requiring root access.

## Core Features

- **Auto IP Changer**: Scheduled proxy rotation with configurable intervals and automatic failover.
- **Proxy Sources**: Support for URL-loaded proxy lists (e.g., GeoNode API) and local JSON files. Includes proxy caching for offline use.
- **Tor Integration**: Seamless integration with Tor, including support for Tor bridges to enhance anonymity and bypass censorship.
- **Wi-Fi Sharing**: A local proxy endpoint that allows other devices on your Wi-Fi network to utilize the proxy settings managed by Aryan Proxy.
- **Browser Spoofing**: Random user agent generation, browser fingerprint management, and profile generation to enhance privacy and bypass detection.
- **Persistent State**: Configuration saving/loading, favorites/history tracking, and state persistence across sessions.
- **Logging System**: Comprehensive logging to `ip_alchemist.log` for activity tracking and error monitoring.
- **Termux-Specific Features**: Optimized for Termux, including proxy environment configuration and integration with `curl`/`wget`.
- **Update System**: Designed with a GitHub-compatible structure for easy updates and version tracking.

## Why Aryan Proxy?

In an increasingly interconnected world, maintaining online privacy and bypassing geographical restrictions are paramount. Aryan Proxy empowers Termux users with a powerful, non-root solution to:

- **Enhance Anonymity**: Regularly change your IP address and route traffic through Tor for improved privacy.
- **Access Restricted Content**: Bypass geo-blocks and access content unavailable in your region.
- **Automate Proxy Management**: Set up and forget, with automatic rotation and failover ensuring continuous connectivity.
- **Share Connectivity**: Easily share your proxy settings with other devices on your local network.
- **Stay Undetected**: Advanced browser spoofing helps in evading detection and maintaining a low profile online.

Aryan Proxy is built with security and ease of use in mind, making it an essential tool for anyone looking to take control of their online presence from their mobile device.




## Installation Guide (for Termux)

Follow these steps to install and set up Aryan Proxy on your Termux environment:

### Prerequisites

Before you begin, ensure you have Termux installed on your Android device. You can download it from F-Droid or the Google Play Store.

1.  **Update Termux Packages**: It's always a good idea to update your Termux packages to the latest versions.
    ```bash
    pkg update && pkg upgrade -y
    ```

2.  **Install Python**: Aryan Proxy is written in Python. Install Python and `pip` (Python's package installer):
    ```bash
    pkg install python -y
    ```

3.  **Install Git**: Git is required to clone the Aryan Proxy repository.
    ```bash
    pkg install git -y
    ```

4.  **Install Tor (Optional, for Tor Integration)**: If you plan to use the Tor integration features, install Tor:
    ```bash
    pkg install tor -y
    pkg install obfs4proxy -y # For Tor bridges
    ```

### Installation Steps

1.  **Clone the Repository**: Clone the Aryan Proxy repository from GitHub to your Termux environment:
    ```bash
    git clone https://github.com/your_username/aryan_proxy.git
    ```
    (Note: Replace `your_username` with the actual GitHub username once the repository is created.)

2.  **Navigate to the Project Directory**:
    ```bash
    cd aryan_proxy
    ```

3.  **Install Python Dependencies**: Install the required Python libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    (Note: We will create `requirements.txt` in a later step.)

## Usage

Once installed, you can run Aryan Proxy from the project directory. Here are some basic usage examples:

### Starting the Proxy Manager

```bash
python main.py
```

### Configuration

The main configuration file is `proxy_config.json`. You can edit this file to customize settings such as rotation interval, default proxy sources, and Tor integration.

### Wi-Fi Sharing

To enable Wi-Fi sharing, ensure the `wifi_sharing_port` is configured in `proxy_config.json` and then activate the feature through the application's interface or command-line option (to be implemented).

### Logging

All activities and errors are logged to `ip_alchemist.log` in the project directory. You can view this file to monitor the proxy's operations and troubleshoot issues.

## Contributing

We welcome contributions to Aryan Proxy! If you have suggestions, bug reports, or want to contribute code, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.


"# aryan_proxy" 
