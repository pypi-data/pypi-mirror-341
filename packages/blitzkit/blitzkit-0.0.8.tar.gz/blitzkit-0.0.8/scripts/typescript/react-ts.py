import subprocess
import sys
import webbrowser
import time

def create(app_name):
    """Create a react typescript project"""
    is_mac = sys.platform == 'darwin'
    is_linux = sys.platform == 'linux'
    url = "https://nodejs.org/en"

    # install node for users on non-window OS
    try:
        result = subprocess.run(
            ['node', '-v'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Node.js is installed: {result.stdout.decode().strip()}")
    except OSError as e:
        if is_mac:
            has_homebrew = subprocess.run(
                ['brew','--version'],
                capture_output=True,
                check=True
            )
            if not has_homebrew:
                webbrowser.open(url, new=0, autoraise=True)
            subprocess.run(
                ['brew','install','node'],
                check=True
            )
            time.sleep(2)
            create(app_name)

        if is_linux:
            subprocess.run(
                ['sudo','apt','install', 'nodejs'],
                check=True
            )
            time.sleep(2)
            create(app_name)

        webbrowser.open(url, new=0, autoraise=True)
        raise OSError("Node.js is not installed. Please install Node.js") from e

    subprocess.run(
        ['npx', 'create-react-app', f'{app_name}/frontend', '--template typescript'],
        check=True,
        shell=not is_mac
    )
