# ChefMate

ChefMate is an automation tool designed to simplify and streamline your CodeChef contest participation. It leverages browser automation (using Selenium and ChromeDriver) along with a versatile command-line interface (CLI) to handle tasks such as logging in, contest management, problem scraping, solution submissions, and demo test case validations. ChefMate also helps set up directories and template files so that you can focus on solving problems quickly and efficiently.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture and Code Structure](#architecture-and-code-structure)
  - [Browser Manager (`browser_manager.py`)](#browser-manager)
  - [Core Functionality (`chefmate_core.py`)](#core-functionality)
  - [Command Line Interface (`cli.py`)](#command-line-interface)
  - [Configuration Management (`config.py`)](#configuration-management)
- [Installation](#installation)
- [Usage](#usage)
  - [Setup](#setup)
  - [Login and Logout](#login-and-logout)
  - [Contest and Problem Management](#contest-and-problem-management)
  - [Testing and Submissions](#testing-and-submissions)
  - [Interactive Mode](#interactive-mode)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Introduction

ChefMate is built to help competitive programmers who participate in CodeChef contests. By automating several routine tasks (such as logging in, opening contest pages, fetching problems, and managing solution submissions), ChefMate removes friction from the contest environment. With its modular design, the tool offers easy configurability and a friendly CLI interface, making the CodeChef contest experience smoother and more productive.

---

## Features

- **Browser Management:**  
  - Detects and prevents conflicts with existing Chrome sessions.
  - Initializes a ChromeDriver with custom profiles and directories.
  - Configurable options to bypass common Chrome logging and automation detections.

- **Automated Contest Interaction:**  
  - Logs into CodeChef and navigates to the contest dashboard.
  - Opens contest pages and scrapes problem links and details.
  - Provides an interactive problem tracker to monitor submission statuses.

- **Solution Management:**  
  - Creates and manages solution directories for contests.
  - Generates template solution files in your preferred programming language.
  - Facilitates opening solution files in your favorite code editor.

- **Submission and Testing:**  
  - Automates the process of selecting the language from the CodeChef UI.
  - Loads solutions from files and submits them via the browser.
  - Runs sample test cases to verify outputs before actual submission.
  - Displays detailed verdict tables and highlights errors.

- **Command-Line Interface (CLI):**  
  - Offers a range of commands (setup, login, logout, contest, submit, check, interactive mode).
  - Provides an intuitive interactive mode with a clear menu-driven experience.
  - Uses libraries such as Click and InquirerPy for enhanced user interaction.

- **Configuration Management:**  
  - Manages user settings (username, password, solution paths, preferred language, Chrome profile, editor preferences) through a JSON configuration file stored in the user's home directory.
  - Ensures persistence and easy updates of user configuration.

---

## Architecture and Code Structure

ChefMate’s code is organized into four main modules:

### Browser Manager

**File:** `browser_manager.py`

- **Purpose:**  
  Manages the Chrome browser session using Selenium WebDriver.  
- **Key Functions:**
  - **Initialization:** Sets up the ChromeDriver with options such as user-data-dir and profile-directory for isolated sessions.
  - **Conflict Detection:** Checks if a Chrome instance is already running and prompts the user accordingly.
  - **Session Management:** Provides methods to initialize, operate, and close the browser session.  
- **Highlights:**  
  Uses `webdriver_manager` to ensure the correct ChromeDriver is installed and employs custom options to reduce unwanted automation flags.

### Core Functionality

**File:** `chefmate_core.py`

- **Purpose:**  
  Acts as the primary interface to ChefMate functionality. It integrates browser automation with the CodeChef website.  
- **Components:**
  - **Login/Logout:**  
    Automates the CodeChef login procedure including form filling, waiting for dashboard elements, and handling potential errors.
  - **Contest Handling:**  
    Opens a contest page, scrapes all available problem links, and dynamically creates a problem tracker.
  - **Solution Handling:**  
    Searches for or prompts for the correct solution file. Generates solution templates based on the preferred programming language.
  - **Submission and Testing:**  
    Provides mechanisms to load code into the CodeChef code editor, submit solutions, and analyze output results by parsing verdict tables.
  - **Interactive Utilities:**  
    Functions like typewriter text effects, dashboard redirection, and dynamic problem tracking to enhance the user experience.

### Command Line Interface

**File:** `cli.py`

- **Purpose:**  
  Provides a user-friendly CLI to interact with ChefMate.  
- **Features:**
  - **CLI Commands:**  
    Implements commands using Click. Commands include `setup`, `login`, `logout`, `check`, `submit`, `contest`, and `interactive`.
  - **Interactive Mode:**  
    An extended menu-driven interface built using InquirerPy that lets users select among different operational modes such as logging in, solving problems, or reconfiguring settings.
  - **UI Enhancements:**  
    Uses the Rich library for improved terminal output, such as styled tables and animated loaders.

### Configuration Management

**File:** `config.py`

- **Purpose:**  
  Handles persistent configurations for ChefMate by reading from and writing to a JSON file.  
- **Details:**
  - **Default Configuration:**  
    Automatically creates a configuration file in the user's home directory (`~/.chefmate/config.json`) if it does not exist.
  - **Dynamic Updates:**  
    Offers methods to get, set, and update various settings including username, password, preferred language, solution file paths, and Chrome user data directories.
  - **Robustness:**  
    Includes error handling to recreate a default configuration if the current configuration file is corrupted.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/chefmate.git
   cd chefmate
   ```

2. **Set Up a Python Virtual Environment (Optional but Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install Dependencies:**

   ChefMate relies on several Python packages. Install them using:

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** Dependencies include libraries like Selenium, webdriver-manager, Click, InquirerPy, Rich, and Colorama. Make sure your environment meets the prerequisites for Selenium and ChromeDriver.

---

## Usage

### Setup

Run the setup command to configure ChefMate with your CodeChef credentials, preferred language, editor, and solution file path:

```bash
python cli.py setup
```

### Login and Logout

To login to CodeChef, use:

```bash
python cli.py login
```

And to logout:

```bash
python cli.py logout
```

### Contest and Problem Management

- **Opening a Contest:**  
  Launch a contest by providing the contest ID and your division using:

  ```bash
  python cli.py contest
  ```

- **Automatic Problem Scraping:**  
  ChefMate will automatically identify and open all the contest problem tabs and display a problem tracker.

### Testing and Submissions

- **Check Demo Test Cases:**  
  Validate your solution using sample test cases:

  ```bash
  python cli.py check --problem 1
  ```

- **Submitting a Solution:**  
  To submit your solution for a given problem:

  ```bash
  python cli.py submit --problem 1
  ```

- **Solving Problems (Template Generation & File Management):**  
  ChefMate automatically generates solution template files in a designated contest directory for you to edit. It opens the selected file in your preferred text editor.

### Interactive Mode

ChefMate also offers an interactive mode that provides a dynamic menu for operations. Launch it with:

```bash
python cli.py interactive
```

In this mode, you can choose among several actions such as login, logout, opening contests, checking demo cases, submitting solutions, and reconfiguring settings.

---

## Dependencies

- **Selenium:** For browser automation and web interactions.
- **webdriver-manager:** To handle ChromeDriver installation and updates.
- **Click & InquirerPy:** For building the CLI and interactive prompts.
- **Rich & Colorama:** For styled terminal outputs and color support.
- **Pandas & Tabulate:** For generating and displaying submission verdict tables.

Make sure you have the latest version of Google Chrome installed to ensure compatibility with ChromeDriver.

---

## Troubleshooting

- **Chrome Profile in Use:**  
  If you receive an error indicating that the Chrome profile is already being used, ensure that all Chrome windows are closed before starting ChefMate.

- **Solution File Issues:**  
  If ChefMate cannot locate your solution file, double-check the path in the configuration (or re-run the `setup` command).

- **Configuration Errors:**  
  If the configuration file is corrupted, ChefMate will automatically generate a new default configuration in `~/.chefmate/config.json`.

- **Network/Slow Load Problems:**  
  For slow networks, ChefMate includes retries during login and test case checks. If problems persist, try restarting your browser or re-running the command.

---

## Future Improvements

- **Enhanced Error Reporting:**  
  Additional debugging information for failures during submissions and test case validations.
- **Multi-Language Support:**  
  Extending support for more languages and custom code editor integration.
- **GUI Implementation:**  
  A graphical user interface for those who prefer not to use the CLI.
- **Extended Contest Support:**  
  Integration with more competitive programming sites.

---

## License

ChefMate is open source software released under the [MIT License](LICENSE).

---

ChefMate is designed with flexibility and practicality in mind to reduce the repetitive tasks of contest participation, leaving you free to concentrate on solving problems and improving your competitive programming skills.

Happy Coding!