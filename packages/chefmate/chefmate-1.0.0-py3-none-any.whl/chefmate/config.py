# config.py
import os
import json

DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".chefmate")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.json")

class Config:
    """Configuration manager for ChefMate"""

    def __init__(self, config_file=DEFAULT_CONFIG_FILE):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from file or create default"""
        if not os.path.exists(os.path.dirname(self.config_file)):
            os.makedirs(os.path.dirname(self.config_file))

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Config file {self.config_file} is corrupted. Creating new config.")
                return self.create_default_config()
        else:
            return self.create_default_config()

    def create_default_config(self):
        """Create default configuration"""
        pc_username = os.getlogin()
        config = {
            "username": "",
            "password": "",
            "preferred_language": "",
            "solution_path": "",
            "chrome_user_data_dir": fr"C:\\Users\\{pc_username}\\AppData\\Local\\Google\\Chrome\\User Data",
            "chrome_profile": "Default",
            "preferred_editor": ""
        }
        self.save_config(config)
        return config

    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def update_config(self, **kwargs):
        """Update configuration with provided values"""
        self.config.update(kwargs)
        self.save_config()

    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
