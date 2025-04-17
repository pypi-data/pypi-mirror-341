# cli.py
import os
import sys
import click
import time
import platform
import colorama
import threading
from colorama import Fore
from chefmate.chefmate_core import ChefMate
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich import box
from rich.text import Text
from rich.table import Table
from rich.console import Console

colorama.init(autoreset=True)
console = Console()

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def loading_animation(stop_event):
    while not stop_event.is_set():
        for i in range(4):
            if stop_event.is_set():
                break
            sys.stdout.write(f"\r{Fore.YELLOW} Loading {'.' * i}   ")
            sys.stdout.flush()
            time.sleep(0.25)

def clear_terminal():
    """Clears the terminal screen based on the OS"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(f"{Fore.GREEN} Terminal cleared successfully! \u2714\n")

@click.group()
def cli():
    """ChefMate - CodeChef Automation Tool"""
    pass

@cli.command()
def setup():
    """Configure ChefMate settings"""
    cm = ChefMate()
    cm.setup()

@cli.command()
def login():
    """Login to CodeChef"""
    cm = ChefMate()
    if cm.initialize():
        cm.login()
    else:
        click.echo(f"{Fore.RED} Failed to initialize browser.")

@cli.command()
def logout():
    """Logout from CodeChef"""
    cm = ChefMate()
    if cm.initialize():
        cm.logout()
    else:
        click.echo(f"{Fore.RED} Failed to initialize browser.")

@cli.command()
@click.option('--problem', '-p', type=int, help='Problem number to check')
def check(problem):
    """Check sample test cases for a problem"""
    cm = ChefMate()
    if cm.initialize() and cm.login():
        if cm.open_contest():
            cm.demo_cases_check(problem)
    else:
        click.echo(f"{Fore.RED} Failed to initialize session.")

@cli.command()
@click.option('--problem', '-p', type=int, help='Problem number to submit')
def submit(problem):
    """Submit solution for a problem"""
    cm = ChefMate()
    if cm.initialize() and cm.login():
        if cm.open_contest():
            cm.submit_solution(problem)
    else:
        click.echo(f"{Fore.RED} Failed to initialize session.")

@cli.command()
def contest():
    """Open a contest and load problems"""
    cm = ChefMate()
    if cm.initialize() and cm.login():
        cm.open_contest()
    else:
        click.echo(f"{Fore.RED} Failed to initialize session.")
# -------------------- Interactive Mode ------------------
@cli.command()
def interactive():
    """Run ChefMate in interactive mode"""
    cm = ChefMate()
    
    cm.display_logo()
    
    click.echo("\n" + f"{Fore.CYAN}=" * 50)
    click.echo(f"{Fore.CYAN}ChefMate Interactive Mode")
    click.echo(f"{Fore.CYAN}=" * 50)

    try:
        hide_cursor()
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()

        first_login = False
        if not cm.config.get("username", "") or not cm.config.get("password", "") or not cm.config.get("solution_path", ""):
            stop_event.set()
            loading_thread.join()
            sys.stdout.write("\r")
            sys.stdout.flush()
            print(f"{Fore.CYAN} We need to configure first.")
            first_login = True
            cm.setup()

        if not cm.initialize():
            stop_event.set()
            loading_thread.join()
            sys.stdout.write("\r")
            sys.stdout.flush()
            click.echo(f"{Fore.RED} Failed to initialize browser.")
            cm.quit()
            return
        
        stop_event.set()
        loading_thread.join()
        sys.stdout.write("\r")
        sys.stdout.flush()
    finally: show_cursor()

    quest_list = [
        Choice(value="_login", name="Login"),
        Choice(value="_logout", name="Logout"),
        Choice(value="_exit", name="Exit"),
        Choice(value="_contest_ini", name="Open Contest"),
        Choice(value="_solve", name="Solve Problems"),
        Choice(value="_demo", name="Check Demo test cases"),
        Choice(value="_submit", name="Submit Solution"),
        Choice(value="_reconfig", name="Re-configure ChefMate"),
        Choice(value="_log_and_ex", name="Logout and Exit"),
        Choice(value="_clear", name="Clear Terminal"),
    ]

    current_choice = "_login"  # Set a default starting choice

    while True:
        choice = inquirer.select(
            message="Select an option: ",
            choices=quest_list,
            default=current_choice,  # Use the stored current choice
            qmark="",            # Remove the default [?]
            pointer=">",        # Custom arrow pointer
            instruction="(Use arrow keys to navigate)"
        ).execute()
        
        # Update the current choice for next iteration
        current_choice = choice
        
        print("\033[F\033[2K", end="")
        selected_name = next((c.name for c in quest_list if c.value == choice), choice)
        table = Table(show_header=False, box=box.ROUNDED, border_style='green')

        # Create a Text object with styling for selected name
        styled_text = Text("You Selected: ")
        styled_text.append(selected_name, style="cyan")
        
        table.add_row(styled_text)
        console.print(table)

        if choice == '_login': 
            if first_login:
                cm.login(first_login=True)
            else: cm.login()
        elif choice == '_logout': cm.logout()
        elif choice == '_config': cm.setup()
        elif choice == '_clear': clear_terminal()
        elif choice == '_contest_ini': 
            quest_list.pop(3)
            quest_list.insert(3, Choice(value="_track_problelm", name="Problem Tracker"))
            quest_list.insert(4, Choice(value="_close_curr_cont", name="Close Current Contest"))
            quest_list.insert(5, Choice(value="_contest_again", name="Open another Contest"))
            cm.open_contest() 
        elif choice == '_solve': cm.solve()
        elif choice == '_reconfig': cm.reconfig()
        elif choice == '_submit': cm.submit_solution()
        elif choice == '_demo': cm.demo_cases_check()
        elif choice == '_exit': 
            cm.quit()
            break
        elif choice == '_log_and_ex': 
            cm.logout()
            cm.quit()
            break
        elif choice == '_close_curr_cont':
            # Close all problem tabs
            if cm.tabs and len(cm.tabs) > 1:
                cm.browser.driver.switch_to.window(cm.tabs[0])

                for tab in cm.tabs[1:]:
                    cm.browser.driver.switch_to.window(tab)
                    cm.browser.driver.close()

                cm.tabs = [cm.tabs[0]]
                cm.browser.driver.switch_to.window(cm.tabs[0])
                print(f"{Fore.GREEN} Closed contest tabs successfully! \u2714")

                dashboard_text = " Loading Dashboard now ..."
                for char in dashboard_text:
                    sys.stdout.write(Fore.YELLOW + char)
                    sys.stdout.flush()
                    time.sleep(0.04)

                sys.stdout.write('\n')
                cm.goto_dashboard()

            quest_list.pop(4)
            quest_list.pop(3)
            quest_list.insert(3, Choice(value="_contest_ini", name="Open Contest"))
            
            # Reset problems list
            cm.problems = []

            # Reset contest ID and directory
            cm.contest_id = None
            cm.contest_dir = None
        elif choice == '_track_problelm':
            cm.show_tracker()
        elif choice == '_contest_again':
            # Close all problem tabs except the first one (contest page)
            if cm.tabs and len(cm.tabs) > 1:
                # Switch to first tab (contest page)
                cm.browser.driver.switch_to.window(cm.tabs[0])
                
                # Close all problem tabs
                for tab in cm.tabs[1:]:
                    cm.browser.driver.switch_to.window(tab)
                    cm.browser.driver.close()
                    
                # Reset tabs list to only include the first tab
                cm.tabs = [cm.tabs[0]]
                cm.browser.driver.switch_to.window(cm.tabs[0])
                print(f"{Fore.GREEN} Closed previous contest tabs successfully! \u2714")
            
            # Reset problems list
            cm.problems = []
            
            # Reset contest ID and directory
            cm.contest_id = None
            cm.contest_dir = None
            
            # Open new contest
            cm.open_contest()
        else: click.echo(f"{Fore.RED} Invalid choice!")
# --------------------------------------------------------

cli.add_command(interactive)

# ------ Main Script -------
if __name__ == "__main__":
    interactive()
# --------------------------