"""
Configuration Checker for Barbeque Nation Chatbot

This script checks the environment configuration and validates that all required
components are properly set up.
"""

import os
import sys
import subprocess
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_success(message):
    """Print a success message in green"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_warning(message):
    """Print a warning message in yellow"""
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_error(message):
    """Print an error message in red"""
    print(f"{RED}✗ {message}{RESET}")

def print_header(message):
    """Print a header message in bold"""
    print(f"\n{BOLD}{message}{RESET}")

def check_env_file():
    """Check if .env file exists and has the required variables"""
    print_header("Checking .env file...")
    
    env_exists = os.path.exists(".env")
    if not env_exists:
        print_error("No .env file found in the current directory")
        print("Create a .env file with the following variables:")
        print("  RETELL_API_KEY=your_retell_api_key")
        print("  DEFAULT_AGENT_ID=your_agent_id")
        print("  KNOWLEDGE_BASE_ID=your_knowledge_base_id (optional)")
        print("  WEBHOOK_URL=your_webhook_url (optional)")
        return False
    
    print_success(".env file found")
    
    # Check required variables
    required_vars = {
        "RETELL_API_KEY": "Retell API Key",
        "DEFAULT_AGENT_ID": "Default Agent ID"
    }
    
    optional_vars = {
        "KNOWLEDGE_BASE_ID": "Knowledge Base ID",
        "WEBHOOK_URL": "Webhook URL",
        "PORT": "Python Server Port",
        "GO_PORT": "Go Server Port"
    }
    
    all_required = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            print_error(f"Missing {description} ({var}) in .env file")
            all_required = False
        elif var == "RETELL_API_KEY" and (len(value) < 20 or value == "your_retell_api_key"):
            print_error(f"Invalid {description} ({var}). It appears to be a placeholder.")
            all_required = False
        elif var == "DEFAULT_AGENT_ID" and (not value.startswith("ag_") or value == "your_agent_id"):
            print_error(f"Invalid {description} ({var}). Agent IDs typically start with 'ag_'.")
            all_required = False
        else:
            masked_value = value[:4] + "..." + value[-4:] if len(value) > 10 else "****"
            print_success(f"{description} ({var}) is set: {masked_value}")
    
    if not all_required:
        print("\nUpdate your .env file with the correct values.")
        return False
        
    # Check optional variables
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if not value:
            print_warning(f"Optional {description} ({var}) is not set")
        else:
            print_success(f"{description} ({var}) is set: {value}")
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print_header("Checking dependencies...")
    
    # Check Python version
    try:
        python_version = sys.version.split()[0]
        print_success(f"Python version: {python_version}")
    except Exception as e:
        print_error(f"Failed to check Python version: {e}")
    
    # Check required Python packages
    required_packages = ["fastapi", "uvicorn", "dotenv", "requests", "tiktoken"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"Package '{package}' is installed")
        except ImportError:
            print_error(f"Package '{package}' is not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print("\nInstall missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    # Check if Go is installed
    try:
        go_output = subprocess.check_output(["go", "version"], stderr=subprocess.STDOUT, text=True)
        print_success(f"Go is installed: {go_output.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Go is not installed or not in PATH")
        print("Download Go from https://golang.org/dl/")
        return False
    
    return True

def check_api_connection():
    """Check connection to Retell API"""
    print_header("Checking Retell API connection...")
    
    retell_api_key = os.getenv("RETELL_API_KEY")
    if not retell_api_key or len(retell_api_key) < 20:
        print_error("Invalid Retell API Key. Cannot check API connection.")
        return False
    
    try:
        import requests
        api_url = "https://api.retellai.com/v1/agents"
        headers = {
            "Authorization": f"Bearer {retell_api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"Connecting to {api_url}...")
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            print_success(f"API connection successful (Status {response.status_code})")
            try:
                agent_count = len(response.json())
                print_success(f"Found {agent_count} agents in your account")
            except:
                print_warning("Could not parse agent count from response")
            return True
        else:
            print_error(f"API connection failed (Status {response.status_code})")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"API connection error: {str(e)}")
        return False

def check_agent_id():
    """Check if the agent ID is valid"""
    print_header("Checking agent ID...")
    
    agent_id = os.getenv("DEFAULT_AGENT_ID")
    if not agent_id:
        print_error("DEFAULT_AGENT_ID not set in .env file")
        return False
    
    if not agent_id.startswith("ag_"):
        print_warning(f"Agent ID format looks unusual: {agent_id}")
        print("Typical agent IDs start with 'ag_'")
    
    try:
        import requests
        retell_api_key = os.getenv("RETELL_API_KEY")
        api_url = f"https://api.retellai.com/v1/agents/{agent_id}"
        headers = {
            "Authorization": f"Bearer {retell_api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"Checking agent ID {agent_id}...")
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            agent_data = response.json()
            agent_name = agent_data.get("name", "Unknown")
            print_success(f"Agent ID is valid: {agent_name}")
            return True
        else:
            print_error(f"Invalid agent ID (Status {response.status_code})")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error checking agent ID: {str(e)}")
        return False

def check_dir_structure():
    """Check if the directory structure is correct"""
    print_header("Checking directory structure...")
    
    required_dirs = [
        "chatbot",
        "chatbot/static",
        "chatbot/static/css",
        "chatbot/static/js",
        "chatbot/static/img",
        "knowledge_base",
        "webhook"
    ]
    
    all_dirs_exist = True
    for d in required_dirs:
        if os.path.isdir(d):
            print_success(f"Directory '{d}' exists")
        else:
            print_error(f"Directory '{d}' does not exist")
            all_dirs_exist = False
    
    required_files = [
        "server.py",
        "chatbot/server.go",
        "chatbot/api.go",
        "chatbot/static/index.html",
        "chatbot/static/js/chatbot.js",
        "chatbot/static/css/styles.css",
        "knowledge_base/api.py",
        "knowledge_base/data.py"
    ]
    
    all_files_exist = True
    for f in required_files:
        if os.path.isfile(f):
            print_success(f"File '{f}' exists")
        else:
            print_error(f"File '{f}' does not exist")
            all_files_exist = False
    
    return all_dirs_exist and all_files_exist

def check_ports():
    """Check if the required ports are available"""
    print_header("Checking ports...")
    
    python_port = int(os.getenv("PORT", "8000"))
    go_port = int(os.getenv("GO_PORT", "8080"))
    
    import socket
    
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    python_port_in_use = is_port_in_use(python_port)
    go_port_in_use = is_port_in_use(go_port)
    
    if python_port_in_use:
        print_warning(f"Port {python_port} (Python server) is already in use")
    else:
        print_success(f"Port {python_port} (Python server) is available")
    
    if go_port_in_use:
        print_warning(f"Port {go_port} (Go server) is already in use")
    else:
        print_success(f"Port {go_port} (Go server) is available")
    
    if python_port_in_use or go_port_in_use:
        print("\nPorts in use. This could be due to servers already running.")
        print("You can stop them with task manager or use different ports by updating your .env file.")
        return False
    
    return True

def check_all():
    """Run all checks and return overall status"""
    print(f"{BOLD}BBQ Nation Chatbot - Configuration Check{RESET}")
    print("=" * 50)
    
    env_status = check_env_file()
    deps_status = check_dependencies()
    dir_status = check_dir_structure()
    api_status = check_api_connection() if env_status else False
    agent_status = check_agent_id() if api_status else False
    port_status = check_ports()
    
    print("\n" + "=" * 50)
    print(f"{BOLD}Summary:{RESET}")
    print(f"Environment file: {'OK' if env_status else 'ISSUES FOUND'}")
    print(f"Dependencies: {'OK' if deps_status else 'ISSUES FOUND'}")
    print(f"Directory structure: {'OK' if dir_status else 'ISSUES FOUND'}")
    print(f"API connection: {'OK' if api_status else 'ISSUES FOUND'}")
    print(f"Agent ID: {'OK' if agent_status else 'ISSUES FOUND'}")
    print(f"Ports: {'OK' if port_status else 'PORTS IN USE'}")
    
    overall_status = all([env_status, deps_status, dir_status, api_status, agent_status, port_status])
    
    print("\n" + "=" * 50)
    if overall_status:
        print(f"{GREEN}{BOLD}All checks passed successfully!{RESET}")
        print("You can now run the chatbot with the following commands:")
        print("  1. Start Python server: python server.py")
        print("  2. Start Go server: cd chatbot && go run server.go")
        print("  Or use the provided run.bat script.")
    else:
        print(f"{RED}{BOLD}Some checks failed. Please fix the issues above before running the chatbot.{RESET}")
    
    return overall_status

if __name__ == "__main__":
    check_all() 