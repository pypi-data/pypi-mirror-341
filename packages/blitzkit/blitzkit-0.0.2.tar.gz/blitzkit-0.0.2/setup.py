from setuptools import setup, find_packages

setup(
    name="blitzkit",
    author="Lenny Uwaeme",
    author_email="lenyeuwame@gmail.com",
    version= "0.0.2",
    description="BlitzKit is a command-line tool that helps student developers automate full-stack project setup. It generates a clean, organized folder structure with starter files to help you get started fast.",
    url="https://github.com/lennythecreator/BlitzKit/tree/main",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    entry_points = {'console_scripts':['blitzkit=blitzkit.cli:run'] }
)