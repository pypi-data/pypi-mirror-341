# browser_manager.py
import os
import subprocess
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

class BrowserManager:
    """Manages browser session and web interactions"""

    def __init__(self, config):
        self.config = config
        self.driver = None

    def is_chrome_running(self):
        """Check if Chrome is currently running (Windows only)"""
        try:
            tasks = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
            return 'chrome.exe' in tasks
        except Exception:
            return False  # fallback safely 

    def initialize_driver(self):
        """Initialize and configure Chrome WebDriver"""

        if self.is_chrome_running():
            print(f"{Fore.RED} Chrome is already running. Please close all Chrome windows before starting ChefMate.\n")
            return False

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--log-level=3')

        # Setup isolated profile directory
        user_data_dir = self.config.get("chrome_user_data_dir")
        if not user_data_dir:
            user_data_dir = os.path.join(os.getcwd(), "chefmate_profile")
        os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={user_data_dir}")

        profile = self.config.get("chrome_profile", "Default")
        options.add_argument(f"--profile-directory={profile}")

        # Optional: prevent common crash issues
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("detach", True)

        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
            )
            return True
        except WebDriverException as e:
            if "user data directory is already in use" in str(e):
                print(f"{Fore.RED} Chrome profile is already being used. Close all Chrome windows and try again.\n")
            else:
                print(f"{Fore.RED} Error initializing Chrome: {e}\n")
            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
