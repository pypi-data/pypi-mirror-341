# ------------------------------------------------------------ Welcome to ChefMate --------------------------------------------------------

# ---------------- Necessary Imports -------------------------------
import os
import sys
import time
import click
import platform
import colorama
import inquirer
import traceback
import subprocess
import pandas as pd
from rich import box
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich.progress import Progress
from tabulate import tabulate
from colorama import Fore, Style
from InquirerPy import inquirer
from chefmate.config import Config
from InquirerPy.base.control import Choice
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from chefmate.browser_manager import BrowserManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
# ------------------------------------------------------------------

# Initialize colorama
colorama.init(autoreset=True)
console = Console()

# Language mapping
LANGUAGE_VALUES = {
    "C++": "C++", "Python3": "PYTH 3", "Python 3": "PYTH 3",
    "C": "C", "Java": "JAVA", "PyPy3": "PYPY3", "C#": "C#",
    "JavaScript": "NODEJS", "Go": "GO", "TypeScript": "TS",
    "PHP": "PHP", "Kotlin": "KTLN", "Rust": "rust", "R": "R"
}

# Language extensions mapping
LANGUAGE_EXTENSIONS = {
    "C++": ".cpp", "Python3": ".py", "Python 3": ".py",
    "C": ".c", "Java": ".java", "PyPy3": ".py", "C#": ".cs",
    "JavaScript": ".js", "Go": ".go", "TypeScript": ".ts",
    "PHP": ".php", "Kotlin": ".kt", "Rust": ".rs", "R": ".r"
}

# Default paths
DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".chefmate")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.json")

class ChefMate:
    """Main ChefMate class for CodeChef automation"""

    def hide_cursor(self):
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def show_cursor(self):
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    def render_problem_tracker(self):
        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.SIMPLE_HEAVY,
            expand=False,  # Prevent full-width stretching
        )

        table.add_column("Status", justify="center", width=7)
        table.add_column("Problem", justify="left", style="bold")

        symbol = {"pending": "🟡", "done": "✅", "wrong": "❌"}

        for code, status in self.problem_status.items():
            emoji = symbol.get(status, "❔")
            table.add_row(emoji, code)

        # Center the table itself
        centered_table = Align.center(table, vertical="middle")

        # Now return the panel with a fixed width
        panel = Panel(centered_table, title="Problem Tracker", border_style="bold white", width=30)
        return panel

    def show_tracker(self):
        print()
        console.print(self.render_problem_tracker())
        print()

    def flush_stdin(self):
        if platform.system() != "Windows":
            import termios
            try:
                termios.tcflush(sys.stdin, termios.TCIFLUSH)
            except:
                pass
        else:
            import msvcrt
            try:
                while msvcrt.kbhit():
                    msvcrt.getch()
            except:
                pass

    def ask(self, text):
        return click.prompt(f" {Fore.MAGENTA}{text}")

    def type_writer(self, text):
        try:
            self.hide_cursor()
            for char in text:
                sys.stdout.write(Fore.YELLOW + char)
                sys.stdout.flush()
                time.sleep(0.04)
            sys.stdout.write("\n")
        finally: self.show_cursor()

    def goto_dashboard(self):
        self.browser.driver.get("https://www.codechef.com/dashboard")
        try:
            WebDriverWait(self.browser.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'CodeChef Logo')]"))
            )
        except TimeoutException:
            print(f"{Fore.RED} Failed to load dashboard page in 15seconds. Slow Internet \n")
        print(f"{Fore.GREEN} Dashboard opened successfully! \u2714\n")

    def display_logo(self):
        banner = Text()
        logo = f"""
    {Fore.RED}
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║     ██████╗ ██╗  ██╗ ███████╗ ███████╗ ███╗   ███╗  █████╗  ████████╗ ███████╗    ║
║    ██╔════╝ ██║  ██║ ██╔════╝ ██╔════╝ ████╗ ████║ ██╔══██╗ ╚══██╔══╝ ██╔════╝    ║
║    ██║      ███████║ █████╗   █████╗   ██╔████╔██║ ███████║    ██║    █████╗      ║
║    ██║      ██╔══██║ ██╔══╝   ██╔══╝   ██║╚██╔╝██║ ██╔══██║    ██║    ██╔══╝      ║
║    ╚██████╗ ██║  ██║ ███████╗ ██║      ██║ ╚═╝ ██║ ██║  ██║    ██║    ███████╗    ║
║     ╚═════╝ ╚═╝  ╚═╝ ╚══════╝ ╚═╝      ╚═╝     ╚═╝ ╚═╝  ╚═╝    ╚═╝    ╚══════╝    ║
║                                                                                   ║
║═══════════════════════════════════════════════════════════════════════════════════║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
    {Style.RESET_ALL}
    """

        banner.append(logo)
        # Print logo immediately
        console.print(banner)

        # Typewriter effect for the last line
        tagline = "Automation tool for CodeChef"
        up_lines, right_spaces = 4, 28
        
        sys.stdout.write(f"\033[{up_lines}A")
        sys.stdout.write(f"\033[{right_spaces}C")

        try:
            self.hide_cursor()
            for char in tagline:
                sys.stdout.write(Fore.RED + char + Style.RESET_ALL)
                sys.stdout.flush()
                time.sleep(0.04)

            sys.stdout.flush()
            print('\n' * 2)
        finally: self.show_cursor()

    def __init__(self, config_file=DEFAULT_CONFIG_FILE):
        self.config = Config(config_file)
        self.browser = BrowserManager(self.config)
        self.problems, self.tabs = [], []
        self.contest_id = None  # Add this line to store the contest ID
        self.contest_dir = None  # Add this line to store the contest directory 
        self.problem_status = {}
        self.logged_in = False
        
    def setup(self):
        """Setup ChefMate configuration"""
        username = click.prompt(f"{Fore.MAGENTA} Username", default=self.config.get("username", ""))
        password = click.prompt(f"{Fore.MAGENTA} Password", hide_input=True, default=self.config.get("password", ""))
        solution_path = click.prompt(f"{Fore.MAGENTA} Default solution file path", default=self.config.get("solution_path", ""))
        chrome_user_data_dir = click.prompt(f"{Fore.MAGENTA} Chrome user data directory (optional)", default=self.config.get("chrome_user_data_dir", ""))
        chrome_profile = click.prompt(f"{Fore.MAGENTA} Chrome profile name (e.g., Default, Profile 1, etc.) (optional)", default=self.config.get("chrome_profile", "Default"))

        # Language Selections Here ------------------------------
        lang_list = [
            Choice(value="C++", name="C++"), Choice(value="Python 3", name="PYTH 3"), Choice(value="JAVA", name="Java"),
            Choice(value="C", name="C"), Choice(value="PYPY3", name="PyPy3"), Choice(value="NODEJS", name="JavaScript"),
            Choice(value="C#", name="C#"), Choice(value="GO", name="Go"), Choice(value="PHP", name="PHP"), 
            Choice(value="KTLN", name="Kotlin"), Choice(value="rust", name="Rust"),
            Choice(value="R", name="R"), Choice(value="TS", name="TypeScript")
        ]
        default_lang = "C++"

        lang_selector = inquirer.select(
            message="Choose your preferred language: ",
            choices=lang_list,
            default=default_lang,  # Use the stored current choice
            qmark="",            # Remove the default [?]
            pointer=">",        # Custom arrow pointer
            instruction="(Use arrow keys to navigate)"
        ).execute()
        
        default_lang = lang_selector    
        print("\033[F\033[2K", end="")  
        print(f" You Chose: {Fore.CYAN}{default_lang}\n")
        
        opt_list = [
            Choice(value="default", name="Notepad (Default)"),
            Choice(value="vscode", name="VS Code"),
            Choice(value="sublime", name="Sublime Text"),
            Choice(value="notepad++", name="Notepad++ (Windows)"),
            Choice(value="atom", name="Atom"),
        ]

        editor = "default"

        choice = inquirer.select(
            message="Choose your preferred editor installed in your system: ",
            choices=opt_list,
            default=editor,  # Use the stored current choice
            qmark="",            # Remove the default [?]
            pointer=">",        # Custom arrow pointer
            instruction="(Use arrow keys to navigate)"
        ).execute()        

        editor = choice

        print("\033[F\033[2K", end="")
        selected_opt = next((c.name for c in opt_list if c.value == choice), choice)
        print(f" You Chose: {Fore.CYAN}{selected_opt}\n")

        if choice == 1: editor = "default"
        elif choice == 2: editor = "vscode"
        elif choice == 3: editor = "sublime"
        elif choice == 4: editor = "notepad++"
        elif choice == 5: editor = "atom"

        self.config.update_config(
            username=username,
            password=password,
            preferred_language=default_lang,
            solution_path=solution_path,
            chrome_user_data_dir=chrome_user_data_dir,
            preferred_editor=editor,
            chrome_profile=chrome_profile,
        )
        
        print(f"{Fore.GREEN} Configuration saved successfully! \u2714\n")

    def reconfig(self):
        """Reconfigure ChefMate"""

        choice = 1

        change_list = [
            Choice(value=1, name="Everything"),
            Choice(value=2, name="Username"),
            Choice(value=3, name="Password"),
            Choice(value=4, name="Preferred Language"),
            Choice(value=5, name="Solution File Path"),
            Choice(value=6, name="Chrome User Data Directory"),
            Choice(value=7, name="Preferred Editor"),  
            Choice(value=8, name="Chrome Profile"),
        ]

        choice_selector = inquirer.select(
            message="What Changes do you want to make: ",
            choices=change_list,
            default=choice,  # Use the stored current choice
            qmark="",            # Remove the default [?]
            pointer=">",        # Custom arrow pointer
            instruction="(Use arrow keys to navigate)"
        ).execute()
        
        choice = choice_selector
        print("\033[F\033[2K", end="")
        selected_opt = next((c.name for c in change_list if c.value == choice_selector), choice_selector)
        print(f" You Chose: {Fore.CYAN}{selected_opt}\n")

        if choice == 1: self.setup()
        elif choice == 2: self.config.set("username", click.prompt(f"{Fore.MAGENTA} New Username", default=self.config.get("username", "")))
        elif choice == 3: self.config.set("password", click.prompt(f"{Fore.MAGENTA} New Password", hide_input=True, default=self.config.get("password", "")))
        elif choice == 4: 
            lang_list = [
                Choice(value="C++", name="C++"), Choice(value="Python 3", name="PYTH 3"), Choice(value="JAVA", name="Java"),
                Choice(value="C", name="C"), Choice(value="PYPY3", name="PyPy3"), Choice(value="NODEJS", name="JavaScript"),
                Choice(value="C#", name="C#"), Choice(value="GO", name="Go"), Choice(value="PHP", name="PHP"), 
                Choice(value="KTLN", name="Kotlin"), Choice(value="rust", name="Rust"),
                Choice(value="R", name="R"), Choice(value="TS", name="TypeScript")
            ]
            default_lang = "C++"

            lang_selector = inquirer.select(
                message="Choose your preferred language: ",
                choices=lang_list,
                default=default_lang,  # Use the stored current choice
                qmark="",            # Remove the default [?]
                pointer=">",        # Custom arrow pointer
                instruction="(Use arrow keys to navigate)"
            ).execute()
            
            print("\033[F\033[2K", end="")  
            print(f" You Chose: {Fore.CYAN}{lang_selector}\n")

            self.config.set("preferred_language", lang_selector)    
        elif choice == 5: self.config.set("solution_path", click.prompt(f"{Fore.MAGENTA} New Solution File Path", default=self.config.get("solution_path", "")))
        elif choice == 6: self.config.set("chrome_user_data_dir", click.prompt(f"{Fore.MAGENTA} New Chrome User Data Directory", default=self.config.get("chrome_user_data_dir", "")))
        elif choice == 7:
            editors_list = [
                Choice(value="default", name="Notepad (System Default)"),
                Choice(value="vscode", name="VS Code"),
                Choice(value="sublime", name="Sublime Text"),
                Choice(value="notepad++", name="Notepad++ (Windows)"),
                Choice(value="atom", name="Atom"),
            ]

            editor = "default"

            editor_selector = inquirer.select(
                message="Choose your preferred editor installed in your system: ",
                choices=editors_list,
                default=editor,  # Use the stored current choice
                qmark="",            # Remove the default [?]
                pointer=">",        # Custom arrow pointer
                instruction="(Use arrow keys to navigate)"
            ).execute()
            
            editor = editor_selector
            print("\033[F\033[2K", end="")
            selected_opt = next((c.name for c in editors_list if c.value == editor_selector), editor_selector)
            print(f" You Chose: {Fore.CYAN}{selected_opt}")

            self.config.set("preferred_editor", editor)
        elif choice == 8:
            self.config.set("chrome_profile", click.prompt(f"{Fore.MAGENTA} New profile name (e.g., Default, Profile 1, etc.) (optional)", default=self.config.get("chrome_profile", "Default")))
        print(f"{Fore.GREEN} Configuration updated successfully! \u2714\n")

    def initialize(self):
        """Initialize browser and start session"""
        try:
            return self.browser.initialize_driver()
        except Exception as e:
            print(f"{Fore.RED} Close all instances of chrome running in the background\n")
            return False

    # ------------------- Login and Logout Process -------------------
    def already_logged_in(self) -> bool:
        """Check if already logged in to CodeChef"""
        dashboard_URL = "https://www.codechef.com/dashboard"
        self.browser.driver.get(dashboard_URL)
        try:
            WebDriverWait(self.browser.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'CodeChef Logo') ]"))
            )
            return self.browser.driver.current_url == dashboard_URL
        except TimeoutException:
            print(f"{Fore.RED} Failed to load dashboard page in 15seconds. Slow Internet \n")
            return False
        except: return False

    def login(self, first_login: bool = False):
        """Login to CodeChef"""
        if not self.browser.driver:
            if not self.initialize():
                print(f"{Fore.RED} Failed to initialize browser.\n")
                return False
                
        if self.already_logged_in():
            print(f"{Fore.GREEN} Already logged in \u2714\n")
            self.logged_in = True
            return True
        
        username = self.config.get("username", "")
        password = self.config.get("password", "")
        
        if not username or not password:
            username = self.ask("Username: ")
            password = self.ask("Password: ")
            save = click.confirm(" Save credentials for future use?", default=True)
            if save:
                self.config.update_config(username=username, password=password)
        
        self.browser.driver.get("https://www.codechef.com/login")
        self.type_writer(" Loggin in ... ")

        try:
            WebDriverWait(self.browser.driver, 15).until(
                EC.element_to_be_clickable((By.ID, "edit-name"))
            )
        except TimeoutException:
            print(f"{Fore.RED} Failed to load login page in 15seconds. Slow Internet, Please Try again\n")
            return False

        if first_login:
            self.browser.driver.refresh()
            try:
                WebDriverWait(self.browser.driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "edit-name"))
                )
            except TimeoutException:
                print(f"{Fore.RED} Failed to load login page in 15seconds. Slow Internet, Please Try again\n")
                return False

        u_box = self.browser.driver.find_element(By.ID, "edit-name")
        u_box.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        u_box.send_keys(username)

        p_box = self.browser.driver.find_element(By.ID, "edit-pass")
        p_box.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        p_box.send_keys(password + Keys.RETURN)

        max_wait_time = 20
        interval = 5
        elapsed_time = 0

        # For slow networks, retry login
        while elapsed_time < max_wait_time:
            try:
                WebDriverWait(self.browser.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, '_content__container')]")
                ))
                print(f"{Fore.GREEN} Successfully loaded Dashboard \u2714\n{Style.RESET_ALL}")
                self.logged_in = True
                return True
            except:
                elapsed_time += interval
                print(f"{Fore.YELLOW} Waiting for Dashboard to load... {elapsed_time}/{max_wait_time} sec")
                time.sleep(interval)
            
        print(f"{Fore.RED} Login timed out. Please check your internet connection and try again.\n")
        return False

    def logout(self):
        """Logout from CodeChef"""
        if not self.browser.driver:
            print(f"{Fore.YELLOW} No active browser session.\n")
            return

        self.type_writer(" Logging out ... ")

        self.browser.driver.get("https://www.codechef.com/logout")
        try:
            WebDriverWait(self.browser.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'CodeChef Logo')]"))
            )
            print(f"{Fore.GREEN} Logged out successfully \u2714\n")
            self.logged_in = False
            return
        except TimeoutException:
            print(f"{Fore.RED} Logout timed out, has waited 15 seconds. Please check your internet connection and try again.\n")
            return
        except:
            print(f"{Fore.YELLOW} Logout status unclear, closing browser anyway.\n")
            self.logged_in = False
            return

    def quit(self):
        """Quit the browser and end session"""
        if self.browser.driver:
            self.browser.close()
            print(f"{Fore.GREEN} Browser closed successfully! \u2714\n")
        else:
            print(f"{Fore.YELLOW} No active browser session to close.\n")
    # ----------------------------------------------------------------
    
    # ----------------- Problem Scraping, Opening in Tabs and Submitting Solutions --------
    def open_contest(self):
        """
        Prompts for contest ID and division, opens contest page and all problem tabs.
        """

        if not self.logged_in:
            self.type_writer(" Logging in before opening contest ... ")
            if not self.login():
                return False

        division_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
        
        contest_id = click.prompt(f" {Fore.MAGENTA}Enter contest ID (e.g., 171)", type=int)
        division = click.prompt(f" {Fore.MAGENTA}Enter your division (1-4)", type=click.Choice(['1', '2', '3', '4']))
        division = int(division)
        
        # Store the contest ID for future use
        self.contest_id = str(contest_id)
        
        contest_url = f"https://www.codechef.com/START{contest_id}{division_map[division]}"
        print(f"{Fore.CYAN} Opening link: {contest_url}{Style.RESET_ALL}")
        self.type_writer(" Opening contest page ... ")
        
        self.browser.driver.get(contest_url)
        try:
            WebDriverWait(self.browser.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'problem-table')]"))
            )
        except TimeoutException:
            print(f"{Fore.RED} Failed to load problems in 15seconds. Slow Internet, Please Try again\n")
        except:
            print(f"{Fore.YELLOW} Contest page looks different than expected, but continuing...")

        base_url = "https://www.codechef.com"
        self.problems = []
        try:
            table = WebDriverWait(self.browser.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dataTable"))
            )
            links = table.find_elements(By.TAG_NAME, "a")
        except TimeoutException:
            print(f"{Fore.RED} Failed to load problems in 10seconds. Slow Internet, Please Try again\n")
        except:
            links = self.browser.driver.find_elements(By.XPATH, "//a[contains(@href, 'problems')]")

        for link in links:
            href = link.get_attribute('href')
            if href and "/problems/" in href:
                if not href.startswith(base_url):
                    href = base_url + href if href.startswith("/") else f"{base_url}/{href}"
                code = href.split("/")[-1]
                title = link.text.strip() or "Untitled Problem"
                self.problems.append((code, title, href))

        if not self.problems:
            print(f"{Fore.RED} No problems found in this contest! \u2716")
            return False
            
        self.problem_status = {code: "pending" for code, _, _ in self.problems}

        self.tabs = [self.browser.driver.current_window_handle]
        with Progress() as progress:
            task = progress.add_task("[yellow] Opening problem tabs", total=len(self.problems))
            for _, _, url in self.problems:
                self.browser.driver.execute_script("window.open(arguments[0]);", url)
                WebDriverWait(self.browser.driver, 2).until(lambda d: len(d.window_handles) > len(self.tabs))
                self.tabs.append(self.browser.driver.window_handles[-1])
                progress.update(task, advance=1)

        # Display problems
        print(f"\n{Fore.GREEN} Found {len(self.problems)} problems:")
        for idx, (code, title, _) in enumerate(self.problems, start=1):
            print(f" {idx}. {code}: {title}")
            
        print()
        self.browser.driver.switch_to.window(self.tabs[0])
        return True
    
    def _get_solution_path(self):
        """Get and validate solution file path"""
        solution_path = self.config.get("solution_path", "")
        
        if not solution_path or not os.path.exists(solution_path):
            solution_path = click.prompt("Enter the path to your solution file")
            save_path = click.confirm("Save this path for future use?", default=True)
            if save_path:
                self.config.set("solution_path", solution_path)
                
        if not os.path.exists(solution_path):
            print(f"{Fore.RED}Solution file not found: {solution_path}")
            return None
        if not os.path.isfile(solution_path):
            print(f"{Fore.RED}Solution path is not a file: {solution_path}")
            return None
        if not os.access(solution_path, os.R_OK):
            print(f"{Fore.RED}Solution file is not readable: {solution_path}")
            return None
        if os.path.getsize(solution_path) == 0:
            print(f"{Fore.RED}Solution file is empty: {solution_path}")
            return None
        if not solution_path.endswith(('.cpp', '.py', '.java', '.js', '.go', '.php', '.kt', '.rs', '.c++', '.cs', '.rb', '.r', '.c', '.ts')):
            print(f"{Fore.RED}Unsupported file type: {solution_path}")
            return None
            
        return solution_path
        
    def _select_language(self):
        """Select language in CodeChef UI"""
        language = self.config.get("preferred_language", "")
        
        if not language:
            language = self.ask("Enter your preferred language (e.g., C++): ")
            save_lang = click.confirm("Save this language preference?", default=True)
            if save_lang:
                self.config.set("preferred_language", language)
                
        data_value = LANGUAGE_VALUES.get(language)
        if not data_value:
            print(f" {Fore.RED}Language {language} not supported.")
            return False
            
        try:
            dropdown = WebDriverWait(self.browser.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id^='language-select']"))
            )
            dropdown.click()
            option = WebDriverWait(self.browser.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f"li[data-value='{data_value}']"))
            )
            option.click()
            return True
        except Exception as e:
            print(f"{Fore.RED} Error selecting language: {e}")
            return False
           
    def _load_code(self, code_text):
        """Load code into editor"""
        try:
            text_input = WebDriverWait(self.browser.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ace_text-input"))
            )
            self.browser.driver.execute_script("arguments[0].focus();", text_input)
            WebDriverWait(self.browser.driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ace_text-input:focus"))
            )
            text_input.send_keys(Keys.CONTROL + 'a')
            text_input.send_keys(Keys.DELETE)
            self.browser.driver.execute_script(
                "ace.edit(document.querySelector('.ace_editor')).setValue(arguments[0], -1);",
                code_text
            )
            return True
        except Exception as e:
            print(f"{Fore.RED} Error loading code: {e}")
            return False

    def verdict(self):
        # Whether your solution was CORRECT or NOT ??
        sol_verd = self.browser.driver.find_element(By.XPATH, "//div[contains(@class, '_run__container')]").text
        sol_verd = sol_verd[0]
        return sol_verd.lower() == 'c'

    def submit_solution(self, problem_num: int = None):
        # Submit solution for a problem

        if not self.problems or not self.tabs:
            print(f"{Fore.RED} No problems loaded. Please open contest tab first.")
            return False
            
        if problem_num is None:
            problem_num = click.prompt(f"{Fore.MAGENTA} Enter problem number to submit", type=int, default=1)
            
        if problem_num < 1 or problem_num > len(self.problems):
            print(f"{Fore.RED} Invalid problem number. Please enter a valid number (1-{len(self.problems)}).")
            return False

        # Switch to selected problem tab
        self.browser.driver.switch_to.window(self.tabs[problem_num])
        
        if not self._select_language():
            return False
        
        # Try to find solution file created by solve() function
        solution_path = self._find_solution_file(problem_num)
        
        # If solution file not found, prompt for path
        if not solution_path:
            solution_path = self._get_solution_path()
            
        if not solution_path:
            return False
            
        try:
            with open(solution_path, 'r') as f:
                code_text = f.read()
            print(f"{Fore.GREEN} Using solution file: {solution_path}")
        except Exception as e:
            print(f"{Fore.RED} Error reading solution file: {e}")
            return False
            
        if not self._load_code(code_text):
            return False

        # Submit the Code
        try:
            text_input = self.browser.driver.find_element(By.CSS_SELECTOR, "textarea.ace_text-input")
            text_input.send_keys(Keys.CONTROL + Keys.ENTER)
            self.type_writer(" Submitting the Code ... ")
            
            try:
                WebDriverWait(self.browser.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_run__container')]"))
                )
            except TimeoutException:
                print(f"{Fore.RED} Submission timed out, has waited 20 seconds. Please check your internet connection and try again.\n")
                return False
            except Exception as e:
                print(f"{Fore.RED} Error submitting code: {e}")
                return False            
            
            # Wait for the verdict to appear

            verdict_in_run_container = self.browser.driver.find_element(By.XPATH, "//div[contains(@class, '_run__container')]").text
            if 'Error' in verdict_in_run_container or 'limit' in verdict_in_run_container.lower():
                print(f"{Fore.RED} {verdict_in_run_container}\n")
                return False
            
            # Wait for the verdict table to appear
            try:
                WebDriverWait(self.browser.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'status-table')]"))
                )
            except TimeoutException:
                print(f"{Fore.RED} Submission timed out, has waited 20 seconds. Please check your internet connection and try again.\n")
                return False            
            except Exception as e:
                print(f"{Fore.RED} Error submitting code: {e}")
                return False
            
            # Extract table data
            table_element = self.browser.driver.find_element(By.XPATH, "//table[contains(@class, 'status-table')]")
            rows = table_element.find_elements(By.TAG_NAME, "tr")
            
            # Parse the table data
            table_data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    row_data = [cell.text for cell in cells]
                    table_data.append(row_data)

            final_verdict = table_data.pop()
            
            final_table_data = []
            for data in table_data:
                interm = []
                if 'Correct' in data[-1]: 
                    for i in range(0, 3):
                        if i != 2: interm.append(f"{Fore.GREEN}{data[i]}{Style.RESET_ALL}")
                        else:
                            string = ''
                            for char in data[i]:
                                if char != '\n': string += f'{Fore.GREEN}{char}{Style.RESET_ALL}'
                                else: string += f'{char}'
                            interm.append(string)
                elif 'Wrong Answer' in data[-1]:
                    for i in range(0, 3):
                        if i != 2: interm.append(f"{Fore.RED}{data[i]}{Style.RESET_ALL}")
                        else:
                            string = ''
                            for char in data[i]:
                                if char != '\n': string += f'{Fore.RED}{char}{Style.RESET_ALL}'
                                else: string += f'{char}'
                            interm.append(string)
                else: 
                    for i in data:
                        interm.append(f"{i}")
                final_table_data.append(interm)

            # Create a pandas DataFrame
            if 'Correct' in final_verdict[1]:
                df = pd.DataFrame(final_table_data, columns=[f"{Fore.GREEN}Sub-Task{Style.RESET_ALL}", 
                                                            f"{Fore.GREEN}Task #{Style.RESET_ALL}", 
                                                            f"{Fore.GREEN}Result (time){Style.RESET_ALL}"])
            else:
                df = pd.DataFrame(final_table_data, columns=[f"{Fore.RED}Sub-Task{Style.RESET_ALL}", 
                                                            f"{Fore.RED}Task #{Style.RESET_ALL}", 
                                                            f"{Fore.RED}Result (time){Style.RESET_ALL}"]) 
            
            print(f"\n{Fore.CYAN} Verdict Table:")
            print(tabulate(
                df, 
                headers='keys', 
                tablefmt='fancy_grid', 
                showindex=False,
                stralign='center',
                numalign='center',
                colalign=('center', 'center', 'center')
            ))
            print(Style.RESET_ALL)
            
            print(f" {Fore.YELLOW}{final_verdict[0]}")

            code = self.problems[problem_num - 1][0]

            if "Correct" in final_verdict[1]: 
                print(f"{Fore.GREEN} VERDICT: CORRECT {Fore.GREEN}\u2714\n{Style.RESET_ALL}")
                self.problem_status[code] = "done"

            elif "Wrong" in final_verdict[1]: 
                print(f"{Fore.RED} VERDICT: INCORRECT {Fore.RED}\u2716\n{Style.RESET_ALL}")
                if self.problem_status.get(code) != "done":  # Optional: don't overwrite if already done
                    self.problem_status[code] = "wrong"

            else:
                self.problem_status[code] = "pending"
            
            return True
        except Exception as e:
            print(f"{Fore.RED} Error submitting code: {e}")
            traceback.print_exc()  # Print the full traceback for better debugging
            return False
    # -------------------------------------------------------------------------------------

    # ------------------ Checker Functions ----------------------
    def demo_cases_check(self, problem_num: int = None):
        """
        Runs all sample test cases for a problem, displays the outputs in a table,
        then compares the outputs line-by-line (ignoring extra whitespace and case)
        and prints a detailed verdict message inspired by verdict.py.
        """
        import re  # For whitespace normalization

        # ANSI color codes (from verdict.py)
        GREEN_TICK = '\u2705'
        RED_CR0SS = '\u274c'
        BOLD_YELLOW = '\033[1;33m'
        GREEN = '\033[0;32m'
        RED = '\x1b[91m'
        RESET = '\033[0m'

        def normalize_whitespace(text):
            return re.sub(r'\s+', ' ', text.strip())

        if not self.problems or not self.tabs:
            print(f"{Fore.RED} No problems loaded. Please open a contest page first.")
            return False

        if problem_num is None:
            problem_num = click.prompt(f"{Fore.MAGENTA} Enter problem number to check", type=int, default=1)

        if problem_num < 1 or problem_num > len(self.problems):
            print(f"{Fore.RED} Invalid problem number. Please enter a valid number (1-{len(self.problems)}).")
            return False

        # Switch to the appropriate problem tab and select language
        self.browser.driver.switch_to.window(self.tabs[problem_num])
        if not self._select_language():
            return False

        # Locate solution file (from solve() or prompt)
        solution_path = self._find_solution_file(problem_num)
        if not solution_path:
            solution_path = self._get_solution_path()
        if not solution_path:
            return False

        try:
            with open(solution_path, 'r') as f:
                code_text = f.read()
            print(f"{Fore.GREEN} Using solution file: {solution_path}")
        except Exception as e:
            print(f"{Fore.RED} Error reading solution file: {e}")
            return False
        if not self._load_code(code_text):
            return False

        self.type_writer(" Checking Demo test cases ...")

        # Run test cases by sending keystrokes
        try:
            text_input = self.browser.driver.find_element(By.CSS_SELECTOR, "textarea.ace_text-input")
            text_input.send_keys(Keys.CONTROL + Keys.SHIFT + Keys.ENTER)
            try:
                WebDriverWait(self.browser.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_output-item__value_')]"))
                )
            except TimeoutException:
                print(f"{Fore.RED} Timed out waiting for test cases to run.")
                return False
            except Exception as e: 
                print(f"{Fore.RED} Error waiting for test cases to run: {e}")
                return False
        except Exception as e:
            print(f"{Fore.RED} Error running test cases: {e}")
            return False

        # Retrieve outputs
        try:
            actual_elem = self.browser.driver.find_elements(By.XPATH, "//div[contains(@class, '_output-item__value_')]")
            actual_output_text = actual_elem[-1].text
            expected_elem = self.browser.driver.find_elements(By.XPATH, "//div[contains(@class, '_values_')]")
            expected_output_text = expected_elem[-1].text
        except Exception as e:
            print(f"{Fore.RED} Error retrieving outputs: {e}")
            return False
        
        status_bar = self.browser.driver.find_element(By.XPATH, "//div[contains(@class, '_status__container_')]").text
        status_text = str(status_bar.split(":")[-1].strip())
        if 'error' in status_text or 'limit' in status_text:
            print(f"{Fore.RED} {status_text} {RESET}\n")
            return False
        
        full_text = expected_elem[0].text.strip()
        expected_output_text = expected_elem[-1].text.strip()

        if expected_output_text and expected_output_text in full_text:
            input_text = full_text.replace(expected_output_text, '').strip()
        else:
            input_text = full_text.strip()

        if actual_output_text.strip() == input_text:
            print(f"{Fore.YELLOW} NO OUTPUT{RESET}\n")
            return False

        # Pre-check: Time Limit Exceeded and no-output conditions
        normalized_actual_full = normalize_whitespace(actual_output_text)
        normalized_expected_full = normalize_whitespace(expected_output_text)
        if "time limit exceeded" in normalized_actual_full.lower():
            print(f"{BOLD_YELLOW} VERDICT:{RESET} {RED}TIME LIMIT EXCEEDED {RED_CR0SS}{RESET}\n")
            return True
        if not normalized_actual_full and normalized_expected_full:
            print(f"{BOLD_YELLOW} VERDICT:{RESET} {RED}TIME LIMIT EXCEEDED ⏰{RESET}\n")
            return True

        # Split outputs into lines and normalize each line for comparison
        actual_lines = [normalize_whitespace(line) for line in actual_output_text.splitlines()]
        expected_lines = [normalize_whitespace(line) for line in expected_output_text.splitlines()]

        # Ensure both lists have the same length by padding with empty strings
        max_len = max(len(actual_lines), len(expected_lines))
        actual_lines.extend([''] * (max_len - len(actual_lines)))
        expected_lines.extend([''] * (max_len - len(expected_lines)))

        # Build a table to display outputs
        headers = ['Your Output', 'Expected Output']
        table_rows = []
        for u, e in zip(actual_lines, expected_lines):
            # Color entire rows in green if they match, otherwise highlight differences
            if u.lower() == e.lower():
                table_rows.append([f"{GREEN}{u}{RESET}", f"{GREEN}{e}{RESET}"])
            else:
                table_rows.append([f"{RED}{u}{RESET}", f"{GREEN}{e}{RESET}"])
        print()
        print(tabulate(
            table_rows,
            headers=headers,
            tablefmt='fancy_grid',
            showindex=False,
            stralign='center',
            numalign='center',
            colalign=('center', 'center')
        ))
        print()

        # Line-by-line comparison to detect the first mismatch
        mismatch_found = False
        for i, (exp, act) in enumerate(zip(expected_lines, actual_lines), start=1):
            if exp.lower() != act.lower():
                print(f"{BOLD_YELLOW} VERDICT:{RESET} {RED}WRONG ANSWER {RED_CR0SS}{RESET}\n")
                print(f"{RED} INCORRECT AT LINE: {i}")
                print(f"{GREEN} EXPECTED: {GREEN}{exp}{RESET}")
                print(f"{BOLD_YELLOW} FOUND: {RED}{act}{RESET}\n")
                mismatch_found = True
                break
        if not mismatch_found and len(actual_lines) == len(expected_lines):
            print(f"{BOLD_YELLOW} VERDICT:{RESET} {GREEN}CORRECT {GREEN_TICK}{RESET}\n")
        elif not mismatch_found:
            # If line counts differ, treat as mismatch
            print(f"{BOLD_YELLOW} VERDICT:{RESET} {RED}WRONG ANSWER {RED_CR0SS}{RESET}\n")
            if len(expected_lines) > len(actual_lines):
                print(f"{RED} INCORRECT AT LINE: {len(actual_lines) + 1}")
                print(f"{GREEN} EXPECTED: {GREEN}{expected_lines[len(actual_lines)]}{RESET}")
                print(f"{BOLD_YELLOW} FOUND: {RED}NULL{RESET}\n")
            else:
                print(f"{RED} INCORRECT AT LINE: {len(expected_lines) + 1}")
                print(f"{GREEN} EXPECTED: {GREEN}NULL{RESET}")
                print(f"{BOLD_YELLOW} FOUND: {RED}{actual_lines[len(expected_lines)]}{RESET}\n")
        return True

    def solve(self):
        """
        Create solution files for problems and open selected problem for editing
        """
        if not self.problems or not self.tabs:
            print(f"{Fore.RED} No problems loaded. Please open a contest first.")
            return False
        
        # Get solution directory from config
        solution_path = self.config.get("solution_path", "")
        if not solution_path:
            solution_path = click.prompt(" Enter solution directory path")
            save_path = click.confirm(" Save this path for future use?", default=True)
            if save_path:
                self.config.set("solution_path", solution_path)
        
        self.type_writer(" Creating Directories ... ")

        # Create solution directory if it doesn't exist
        if not os.path.exists(solution_path):
            try:
                os.makedirs(solution_path)
                print(f"{Fore.GREEN} Created solution directory: {solution_path}")
            except Exception as e:
                print(f"{Fore.RED} Error creating solution directory: {e}")
                return False
        
        # Get preferred language
        language = self.config.get("preferred_language", "")
        if not language:
            language = click.prompt(" Enter your preferred language (e.g., C++)")
            save_lang = click.confirm(" Save this language preference?", default=True)
            if save_lang:
                self.config.set("preferred_language", language)
        
        # Get file extension for the language
        extension = LANGUAGE_EXTENSIONS.get(language, ".txt")
        if extension == ".txt":
            print(f"{Fore.YELLOW} Warning: Unknown language '{language}'. Using .txt extension.")
        
        # Use existing contest ID or extract contest ID from URL
        if self.contest_id is None and self.tabs and self.browser.driver:
            current_url = self.browser.driver.current_url
            if "START" in current_url:
                try:
                    # Extract the contest number from START{NUM}{DIVISION}
                    # For example: https://www.codechef.com/START171A -> 171
                    self.contest_id = ''.join(filter(str.isdigit, current_url.split("START")[1][:4]))
                    print(f"{Fore.GREEN} Detected contest ID: {self.contest_id}")
                except:
                    self.contest_id = "unknown"
            else:
                self.contest_id = "unknown"
        
        # Use existing contest directory or create a new one
        if self.contest_dir and os.path.exists(self.contest_dir):
            contest_dir = self.contest_dir
            print(f"{Fore.GREEN} Using existing contest directory: {contest_dir}")
        else:
            # Create Starter directory with contest number if it doesn't exist
            contest_dir = os.path.join(solution_path, f"Starter {self.contest_id}")
            
            # Check if the directory already exists
            if os.path.exists(contest_dir):
                print(f"{Fore.GREEN} Using existing contest directory: {contest_dir}")
            else:
                try:
                    os.makedirs(contest_dir)
                    print(f"{Fore.GREEN} Created contest directory: {contest_dir}")
                except Exception as e:
                    print(f"{Fore.RED} Error creating contest directory: {e}")
                    return False
            
            # Store the contest directory for future use
            self.contest_dir = contest_dir
        
        # Save contest directory in config for other functions to use
        self.config.set("current_contest_dir", contest_dir)
        
        # Get username for author comment
        ur_name = self.config.get("username", "USER")
        
        # Create template file content based on language
        template_content = ""
        if language == "C++":
            template_content = f"""// Author -> '{ur_name}'

#include <bits/stdc++.h>
using namespace std;

int main() {{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    // Your code here
    
    return 0;
}}
    """
        elif language == "Python3" or language == "Python 3" or language == "PyPy3":
            template_content = f"""# Author -> '{ur_name}'

def main():
    # Your code here
    pass

if __name__ == "__main__":
    main()
    """
        elif language == "Java":
            template_content = f"""// Author -> '{ur_name}'
import java.util.*;

public class Main {{
    public static void main(String[] args) {{
        Scanner sc = new Scanner(System.in);
        
        // Your code here
        
        sc.close();
    }}
}}
    """
        elif language == "JavaScript" or language == "NodeJS" or language == "NODEJS":
            template_content = f"""// Author -> '{ur_name}'

function main() {{
    // Your code here
}}

main();
    """
        elif language == "Go":
            template_content = f"""// Author -> '{ur_name}'
package main

import (
    "fmt"
)

func main() {{
    // Your code here
}}
    """
        elif language == "C#" or language == "CS":
            template_content = f"""// Author -> '{ur_name}'
using System;

class Program {{
    static void Main(string[] args) {{
        // Your code here
    }}
}}
    """
        elif language == "PHP":
            template_content = f"""<?php
// Author -> '{ur_name}'

function main() {{
    // Your code here
}}

main();
?>
"""
        elif language == "Ruby":
            template_content = f"""# Author -> '{ur_name}'

def main
# Your code here
end

main
    """
        elif language == "Rust":
            template_content = f"""// Author -> '{ur_name}'

fn main() {{
    // Your code here
}}
    """
        elif language == "TypeScript" or language == "TS":
            template_content = f"""// Author -> '{ur_name}'

function main(): void {{
    // Your code here
}}

main();
    """
        elif language == "Kotlin" or language == "KTLN":
            template_content = f"""// Author -> '{ur_name}'

fun main() {{
    // Your code here
}}
    """
        elif language == "R":
            template_content = f"""# Author -> '{ur_name}'

main <- function() {{
# Your code here
}}

main()
    """
        elif language == "C":
            template_content = f"""// Author -> '{ur_name}'

#include <stdio.h>

int main() {{
    // Your code here
    return 0;
}}
    """
        else:
            template_content = f"""// Author -> '{ur_name}'

// Your code here
    """
        
        # Create solution files for each problem (only if they don't exist)
        created_files = []
        existing_files = []
        
        for idx, (code, _, _) in enumerate(self.problems, start=1):
            filename = f"{code}{extension}"
            filepath = os.path.join(contest_dir, filename)
            
            # Check if file already exists
            if os.path.exists(filepath):
                existing_files.append((idx, filepath))
            else:
                try:
                    with open(filepath, 'w') as f:
                        f.write(template_content)
                    print(f"{Fore.GREEN} Created solution file: {filepath}")
                    created_files.append((idx, filepath))
                except Exception as e:
                    print(f"{Fore.RED} Error creating solution file: {filepath}: {e}")
        
        # Combine created and existing files (sorted by index)
        all_files = sorted(created_files + existing_files, key=lambda x: x[0])
        
        # Display files
        if created_files:
            print(f"\n{Fore.GREEN} New solution files created for {len(created_files)} problems:")
            for idx, filepath in created_files:
                print(f" {idx}. {os.path.basename(filepath)}")
        
        if existing_files:
            print(f"\n{Fore.CYAN} Using existing solution files for {len(existing_files)} problems:")
            for idx, filepath in existing_files:
                print(f" {idx}. {os.path.basename(filepath)}")
        
        # Select problem to solve
        print(f"\n{Fore.CYAN} Available problems:")
        for idx, (code, title, _) in enumerate(self.problems, start=1):
            print(f" {idx}. {code}: {title}")
        
        print()
        problem_num = click.prompt(f"{Fore.MAGENTA} Enter problem number to solve", type=int, default=1)
        print()
        if problem_num < 1 or problem_num > len(self.problems):
            print(f"{Fore.RED} Invalid problem number. Please enter a valid number (1-{len(self.problems)}).")
            return False
        
        # Find the file for the selected problem
        selected_file = None
        for idx, filepath in all_files:
            if idx == problem_num:
                selected_file = filepath
                break
        
        if not selected_file:
            print(f"{Fore.RED} No solution file found for problem {problem_num}.")
            return False
        
        # Open selected problem file
        try:
            # Switch to problem tab first
            self.browser.driver.switch_to.window(self.tabs[problem_num])
            print(f"{Fore.GREEN} Switched to problem tab: {self.problems[problem_num-1][1]}")
            
            # Check if file exists
            if not os.path.exists(selected_file):
                print(f"{Fore.RED} File not found: {selected_file}")
                return False
            
            # Get preferred editor from config or prompt
            editor = self.config.get("preferred_editor", "")
            if not editor:
                choice = 1
                editor = [
                    Choice(value="default", name="Notepad (System Default)"),
                    Choice(value="vscode", name="VS Code"),
                    Choice(value="sublime", name="Sublime Text"),
                    Choice(value="notepad++", name="Notepad++ (Windows)"),
                    Choice(value="atom", name="Atom"),
                ]
                
                editor_selector = inquirer.select(
                    message="Select your preferred editor:",
                    choices=editor,
                    default="default",  # Use the stored current choice
                    qmark="",            # Remove the default [?]
                    pointer=">",        # Custom arrow pointer
                    instruction="(Use arrow keys to navigate)"
                ).execute()
                
                choice = editor_selector
                selected_editor = next((c.name for c in editor if c.value == editor_selector), editor_selector)
                print(f"{Fore.GREEN} You chose: {selected_editor}")

                if choice == 1:
                    editor = "default"
                elif choice == 2:
                    editor = "vscode"
                elif choice == 3:
                    editor = "sublime"
                elif choice == 4:
                    editor = "notepad++"
                elif choice == 5:
                    editor = "atom"
                elif choice == 6:
                    editor = click.prompt(" Enter editor command (use {file} as placeholder for filename)")
                
                save_choice = click.confirm(" Save this editor preference?", default=True)
                if save_choice:
                    self.config.set("preferred_editor", editor)
            
            # Open file with selected editor
            print(f"{Fore.GREEN} Opening file with editor: {editor}")

            devnull = subprocess.DEVNULL

            try:
                if editor == "default":
                    # Use system default
                    if os.name == 'nt':  # Windows
                        subprocess.Popen(['notepad', selected_file], 
                                            start_new_session=True,
                                            shell=True,
                                            stdout=devnull,
                                            stderr=devnull)
                        time.sleep(0.3)
                        self.flush_stdin()
                    elif os.name == 'posix':  # Linux/Mac
                        if sys.platform == 'darwin':  # Mac
                            subprocess.call(['open', selected_file], stdout=devnull, stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                        else:  # Linux
                            subprocess.call(['xdg-open', selected_file], stdout=devnull, stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                elif editor == "vscode":
                    # Check for different VS Code executable names
                    vscode_commands = ['code', 'Code.exe', 'code.cmd', 'Code.cmd']
                    success = False
                    for cmd in vscode_commands:
                        try:
                            subprocess.Popen([cmd, selected_file], 
                                            start_new_session=True, 
                                            shell=(os.name == 'nt'), 
                                            stdout=devnull, 
                                            stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                            success = True
                            break
                        except FileNotFoundError:
                            continue
                            
                    if not success:
                        print(f"{Fore.YELLOW} VS Code not found in PATH. Falling back to system default.")
                        print(f"{Fore.YELLOW} TIP - Add the path of vscode.exe file into the system's environment variable path.")
                        # Fall back to system default
                        if os.name == 'nt':
                            subprocess.Popen(['notepad', selected_file], 
                                            start_new_session=True,
                                            shell=True,
                                            stdout=devnull,
                                            stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                        elif os.name == 'posix':
                            if sys.platform == 'darwin':
                                subprocess.call(['open', selected_file], stdout=devnull, stderr=devnull)
                                time.sleep(0.3)
                                self.flush_stdin()
                            else:
                                subprocess.call(['xdg-open', selected_file], stdout=devnull, stderr=devnull)
                                time.sleep(0.3)
                                self.flush_stdin()
                elif editor == "sublime":
                    # Try different possible Sublime Text command names
                    sublime_commands = ['subl', 'sublime_text', 'sublime', 'Sublime Text.exe']
                    success = False
                    for cmd in sublime_commands:
                        try:
                            subprocess.Popen([cmd, selected_file], 
                                            start_new_session=True,
                                            shell=(os.name == 'nt'),
                                            stdout=devnull,
                                            stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                            success = True
                            break
                        except FileNotFoundError:
                            continue
                            
                    if not success:
                        print(f"{Fore.YELLOW} Sublime Text not found in PATH. Falling back to system default.")
                        print(f"{Fore.YELLOW} TIP - Add the path of sublime_text.exe file into the system's environment variable path.")
                        # Fall back to system default
                        if os.name == 'nt':
                            subprocess.Popen(['notepad', selected_file], 
                                            start_new_session=True,
                                            shell=True,
                                            stdout=devnull,
                                            stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                        else:
                            subprocess.call(['xdg-open', selected_file], stdout=devnull, stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                elif editor == "notepad++":
                    try:
                        # Try different possible Notepad++ executable names
                        npp_commands = ['notepad++', 'notepad++.exe', 'Notepad++.exe']
                        success = False
                        for cmd in npp_commands:
                            try:
                                subprocess.Popen([cmd, selected_file], 
                                                start_new_session=True, 
                                                shell=(os.name == 'nt'),
                                                stdout=devnull,
                                                stderr=devnull)
                                time.sleep(0.3)
                                self.flush_stdin()
                                success = True
                                break
                            except FileNotFoundError:
                                continue
                                
                        if not success:
                            print(f"{Fore.YELLOW} Notepad++ not found in PATH. Falling back to system notepad.")
                            print(f"{Fore.YELLOW} TIP - Add the path of notepad++.exe file into the system's environment variable path.")
                            print(f"{Fore.YELLOW} Till then Falling Back to the regulare notepad on Windows.")
                            # Fall back to regular notepad on Windows
                            subprocess.Popen(['notepad', selected_file], 
                                            start_new_session=True,
                                            shell=True,
                                            stdout=devnull,
                                            stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                    except:
                        # If all else fails, use system default
                        subprocess.Popen(['notepad', selected_file], 
                                            start_new_session=True,
                                            shell=True,
                                            stdout=devnull,
                                            stderr=devnull) if os.name == 'nt' else subprocess.call(['xdg-open', selected_file], stdout=devnull, stderr=devnull)
                        time.sleep(0.3)
                        self.flush_stdin()
                elif editor == "atom":
                    success = False
                    try:
                        subprocess.Popen(['atom', selected_file], 
                                        start_new_session=True,
                                        shell=(os.name == 'nt'),
                                        stdout=devnull,
                                        stderr=devnull)
                        time.sleep(0.3)
                        self.flush_stdin()
                        success = True
                    except FileNotFoundError:
                        print(f"{Fore.RED} File not found")

                    if not success:
                        print(f"{Fore.YELLOW} Atom not found in PATH. Falling back to system default.")
                        print(f"{Fore.YELLOW} TIP - Add the path of atom.exe file into the system's environment variable path.\n")
                        # Fall back to system default
                        if os.name == 'nt':
                            subprocess.Popen(['notepad', selected_file], 
                                            start_new_session=True,
                                            shell=True,
                                            stdout=devnull,
                                            stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                        else:
                            subprocess.call(['xdg-open', selected_file], stdout=devnull, stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                else:
                    # Custom command
                    success = False
                    try:
                        subprocess.Popen(['notepad', selected_file], 
                                            start_new_session=True,
                                            shell=True,
                                            stdout=devnull,
                                            stderr=devnull)
                        time.sleep(0.3)
                        self.flush_stdin()
                        success = True
                    except FileNotFoundError:
                        print(f"{Fore.RED} File not found ")
                    except Exception as e:
                        print(f"{Fore.YELLOW} Error executing custom command. Falling back to system default.")
                        # Fall back to system default
                        if os.name == 'nt':
                            subprocess.Popen(['notepad', selected_file], 
                                            start_new_session=True,
                                            shell=True,
                                            stdout=devnull,
                                            stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                            success = True
                        else:
                            subprocess.call(['xdg-open', selected_file], stdout=devnull, stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                            success = True
                            
                print(f"{Fore.GREEN} Opened file for editing: {selected_file}\n")
                return True
            except Exception as e:
                print(f"{Fore.RED} Error opening file: {e}")
                print(f"{Fore.YELLOW} Attempting to open with system default editor instead...")
                try:
                    # Last resort - try with system default
                    if os.name == 'nt':  # Windows
                        subprocess.Popen(['notepad', selected_file], 
                                            start_new_session=True,
                                            shell=True,
                                            stdout=devnull,
                                            stderr=devnull)
                        time.sleep(0.3)
                        self.flush_stdin()
                    elif os.name == 'posix':  # Linux/Mac
                        if sys.platform == 'darwin':  # Mac
                            subprocess.call(['open', selected_file], stdout=devnull, stderr=devnull)
                            time.sleep(0.3)
                            self.flush_stdin()
                        else:  # Linux
                            subprocess.call(['xdg-open', selected_file])
                            time.sleep(0.3)
                            self.flush_stdin()
                    print(f"{Fore.GREEN} Opened file with system default editor: {selected_file}\n")
                    return True
                except Exception as e2:
                    print(f"{Fore.RED} All attempts to open the file failed: {e2}")
                    print(f"{Fore.YELLOW} Please manually open the file: {selected_file}\n")
                    return False
        except Exception as e:
            print(f"{Fore.RED} Error opening file: {e}\n")
            return False

    def _find_solution_file(self, problem_num):
        """Find solution file for the given problem number"""
        if not problem_num or problem_num < 1 or problem_num > len(self.problems):
            return None
            
        # Get problem code for the selected problem
        problem_code = self.problems[problem_num-1][0]
        
        # First try to use the stored contest directory
        if self.contest_dir and os.path.exists(self.contest_dir):
            contest_dir = self.contest_dir
        else:
            # Get contest directory from config (set by solve function)
            contest_dir = self.config.get("current_contest_dir", "")
        
            # If contest directory not found, try to determine it
            if not contest_dir or not os.path.exists(contest_dir):
                solution_path = self.config.get("solution_path", "")
                if not solution_path or not os.path.exists(solution_path):
                    return None
                    
                # Try to extract contest ID from URL or use stored contest ID
                contest_id = self.contest_id
                if not contest_id:
                    contest_id = "unknown"
                    if self.tabs and self.browser.driver:
                        current_url = self.browser.driver.current_url
                        if "START" in current_url:
                            try:
                                contest_id = ''.join(filter(str.isdigit, current_url.split("START")[1][:4]))
                            except:
                                pass
                        
                contest_dir = os.path.join(solution_path, f"Starter {contest_id}")
                if not os.path.exists(contest_dir):
                    return None
        
        # Get preferred language extension
        extension = LANGUAGE_EXTENSIONS.get(self.config.get("preferred_language", ""), "")
        
        # Try to find file with preferred extension
        if extension:
            filepath = os.path.join(contest_dir, f"{problem_code}{extension}")
            if os.path.exists(filepath):
                return filepath
        
        # If not found or no extension specified, try all possible extensions
        for ext in LANGUAGE_EXTENSIONS.values():
            filepath = os.path.join(contest_dir, f"{problem_code}{ext}")
            if os.path.exists(filepath):
                return filepath
        
        return None
    # ----------------------------------------------------------
