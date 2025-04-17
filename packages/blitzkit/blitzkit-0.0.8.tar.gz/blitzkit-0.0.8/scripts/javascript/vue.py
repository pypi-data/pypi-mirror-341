import subprocess
import platform
import sys
import os
import webbrowser
import time

def create(app_name):
    """Create Vue Project"""
    is_mac = platform.system() == 'darwin'
    is_linux = platform.system() == 'linux'
    url = "https://nodejs.org/en"

    
    try:
        # checking to see if user has node installed on their OS.
        result = subprocess.run(['node', '-v'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Node.js is installed: {result.stdout.decode().strip()}")
    except:
        if is_mac:
            has_homebrew = subprocess.run(['brew','--version'], capture_output=True)
            if not has_homebrew:
                webbrowser.open(url, new=0, autoraise=True)
            subprocess.run(['brew','install','node'])
            time.sleep(2)
            create(app_name)

        if is_linux:
            subprocess.run(['sudo','apt','install', 'nodejs'])
            time.sleep(2)
            create(app_name)
        
        webbrowser.open(url, new=0, autoraise=True)
        raise OSError("Node.js is not installed. Please install Node.js")
    
    os.makedirs(f'{app_name}', exist_ok=True)
    subprocess.run(
        ['npm', 'create','vue@latest', f'{app_name}/frontend'],
        check=True,
        shell=not is_mac
    )
