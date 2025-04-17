import subprocess
import sys
import webbrowser
import os

def handle_mac() -> bool:
    """Try downloading angular-cli if user has the necessary dependencies"""
    url_homebrew = "https://brew.sh/"
    url_node = "https://nodejs.org/"
    url_angular = "https://angular.io/cli"

    try:
        subprocess.run(
            ['brew', '--version'],
            capture_output=True,
            check=True
        )
    except FileNotFoundError:
        try:
            subprocess.run(
                [
                    '/bin/bash', '-c',
                    '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                ],
                capture_output=True,
                check=True
            )
            print("Homebrew has been successfully installed.")
        except subprocess.CalledProcessError:
            print("Unable to install Homebrew. Redirecting to the installation page...")
            webbrowser.open(url_homebrew, new=0, autoraise=True)
            return False

    try:
        subprocess.run(
            ['node', '-v'],
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        try:
            subprocess.run(
                ['brew', 'install', 'node@22'],
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ['brew', 'link', '--overwrite', 'node@22'],
                capture_output=True,
                check=True
            )
            print("Node has been successfully installed.")
        except subprocess.CalledProcessError:
            print("Node not installed. Redirecting to the installation page...")
            webbrowser.open(url_node, autoraise=True)
            return False

    try:
        subprocess.run(
            ['ng', '--version'],
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        try:
            subprocess.run(
                ['npm', 'install', '-g', '@angular/cli'],
                capture_output=True,
                check=True,
            )
            print("Angular successfully installed.")
        except subprocess.CalledProcessError:
            print("Unable to install angular-cli. Redirecting to the installation page.")
            webbrowser.open(url_angular, autoraise=True)
            return False
    return True

def handle_linux() -> bool:
    """Try downloading angular-cli if user has the necessary dependencies"""
    url_node = "https://nodejs.org/"
    url_angular = "https://angular.io/cli"

    try:
        subprocess.run(
            ['node', '-v'],
            check=True,
            shell=True
        )
    except subprocess.CalledProcessError:
        print("Node not installed. Redirecting to the installation page...")
        webbrowser.open(url_node, autoraise=True)
        return False

    try:
        subprocess.run(
            ['brew', 'install', 'angular-cli'],
            capture_output=True,
            check=True,
            shell=True
        )
    except subprocess.CalledProcessError:
        print("Unable to install angular-cli. Redirecting to the installation page.")
        webbrowser.open(url_angular, autoraise=True)
        return False
    return True

def create(app_name: str) -> None:
    """Create an angular project"""
    is_mac = sys.platform == 'darwin'
    is_linux = sys.platform == 'linux'

    if is_mac:
        handle_mac()
    elif is_linux:
        handle_linux()
    else:
        pass

    subprocess.run(
        ['ng', 'new', 'frontend', f'--directory={app_name}/frontend'],
        check=True,
        shell=not is_mac
    )
