import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_file="ip_alchemist.log"):
        self.log_file = log_file
        self.logger = logging.getLogger("ip_alchemist")
        self.logger.setLevel(logging.INFO)

        # Create handlers
        file_handler = logging.FileHandler(self.log_file)
        console_handler = logging.StreamHandler()

        # Create formatters and add it to handlers
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def activity(self, activity_type, details):
        self.info(f"ACTIVITY: {activity_type} - {details}")

    def clear_log(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.truncate(0)
            self.info("Log file cleared.")
        else:
            self.info("Log file does not exist.")


