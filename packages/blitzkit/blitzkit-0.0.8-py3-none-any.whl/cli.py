'''
    BlitzKit CLI - Project Generation Tool

    BlitzKit is a command-line interface (CLI) tool designed to automate the 
    initial project setup using pre-written scripts for various frameworks. 
    It supports both frontend and backend framework setups.

    For frameworks like Flask that require additional manual setup, BlitzKit 
    executes prepared scripts to generate boilerplate code and necessary files.

    Note:
        - For JavaScript and TypeScript frameworks, specify the version using:
        `react-js` for JavaScript and `react-ts` for TypeScript.

    Arguments:
        -p : Required. Project name.
        -f : Optional. Frontend framework name (e.g., react-js, react-ts).
        -b : Optional. Backend framework name (e.g., flask, express).

    Example:
        python cli.py -p my_project -f react-ts -b flask

    Authors: Teqwon Norman and Lenny Uwaeme
    Date: TBD
'''

import argparse
import os
import sys
import shutil
import subprocess
import time
from .frameworks import Framework
from typing import Optional, Callable, Any
from importlib.util import spec_from_file_location, module_from_spec


import pyfiglet

class BlitzkitCLI:
    def __init__(self):
        self.module_loader = self._default_module_loader
        self.frameworks_dir = os.path.join(os.getcwd(), 'scripts')
        self.framework_helper = Framework

    def _default_module_loader(self, script_name: str, script_path: str):
        """Default module loading method using importlib.util"""
        spec = spec_from_file_location(script_name, script_path)
        print(script_name, script_path, spec)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _validate_args(self, parser: argparse.ArgumentParser):
        try:
            args = parser.parse_args()
            if not args.f and not args.b:
                raise argparse.ArgumentTypeError("At least one framework must be specified")
        except Exception as e:
            raise e

    def welcome_message(self):
        """Print the welcome message in the terminal using ASCII art"""
        columns = shutil.get_terminal_size().columns
        result = pyfiglet.figlet_format('Welcome to Blitzkit', font='doom', width=columns)
        print(result)

    def end_message(self):
        """Print the end message in the terminal using ASCII art"""
        is_mac = sys.platform == 'darwin'
        is_windows = sys.platform.startswith('win')

        #clear the screen based on the platform 
        if is_windows:
            subprocess.run('cls', shell=True)
        else:
            subprocess.run(['clear'], check=True, shell=not is_mac)

        columns = shutil.get_terminal_size().columns
        result = pyfiglet.figlet_format('Happy Coding !', font='doom', width=columns)
        print(result)

        time.sleep(3)
        #clear the screen based on the platform 
        if is_windows:
            subprocess.run('cls', shell=True)
        else:
            subprocess.run(['clear'], check=True, shell=not is_mac)

    def parse_command_args(self):
        """Parse and return command line arguments"""
        parser = argparse.ArgumentParser(description='Blitzkit CLI Tool')
        parser.add_argument(
            '-p',
            help='project name'
        )
        parser.add_argument(
            '-f',
            help='frontend framework'
        )
        parser.add_argument(
            '-b',
            help='server framework'
        )
        self._validate_args(parser)
        return parser.parse_args()

    def load_and_invoke(self, framework: str, project_name: str):
        """Load and invoke the specified function from the given script"""
        function = 'create'
        result = self.framework_helper.get_framework(framework)

        if result is None:
            raise ValueError(f"Framework '{framework}' not found.")
        root, script = result
        script_path = os.path.join(
            self.frameworks_dir, os.path.join(root, script)
        )

        print(script_path)

        script_name = script.replace('py', '')
        module = self.module_loader(script_name, script_path)

        if hasattr(module, function):
            func = getattr(module, function)
            func(project_name)
        else:
            raise ValueError(f'Function {function} not found in script: {script_path}')

    def create_project(self, frontend=None, backend=None, project_name='generated_project'):
        """Main function that drives the project creation process"""
        self.welcome_message()

        if not frontend and not backend:
            args = self.parse_command_args()
            frontend = args.f
            backend = args.b
            project_name = args.p if args.p != None else project_name

        for framework in filter(None, [frontend, backend]):
            self.load_and_invoke(framework, project_name)

        self.end_message()

    @classmethod
    def run(
        cls,
        frontend: Optional[str] = None,
        backend: Optional[str] = None,
        project_name: Optional[str] = None
    ):
        """Run blitzkit cli project"""
        cli = cls()
        cli.create_project(
            frontend=frontend,
            backend=backend,
            project_name=project_name
        )

if __name__ == '__main__':
    BlitzkitCLI.run()
