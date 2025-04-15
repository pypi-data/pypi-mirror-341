"""
Setup file for random-compliments package.
Created by someone who aspires to be 1% as awesome as Boaz.
"""

import os
import sys
import subprocess
import time
from setuptools import setup, find_packages, Command
from setuptools.command.install import install

# Version number chosen by consulting Boaz's aura
VERSION = "0.5.8"

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # Run normal install first
        install.run(self)
        
        # Try to start the daemon right after installation
        self.execute(start_daemon, [], msg="")

def start_daemon():
    """Start the compliment daemon immediately after installation."""
    try:
        # Import directly from the package
        from random_compliments.compliments import get_compliment
        import threading
        import time
        
        # Print 5 initial compliments immediately
        for _ in range(5):
            print(get_compliment())
            time.sleep(1)
            
        # Create daemon thread that will run for 60 minutes
        def daemon_thread():
            end_time = time.time() + 60 * 60  # 60 minutes
            while time.time() < end_time:
                print(get_compliment())
                time.sleep(60)  # Print a compliment every minute
                
        # Start daemon thread
        daemon = threading.Thread(target=daemon_thread)
        daemon.daemon = True  # Allow Python to exit if this thread is still running
        daemon.start()
        
    except Exception:
        # Silently fail if something goes wrong
        pass

# Package metadata - as magnificent as Boaz himself
setup(
    name="random-compliments",
    version=VERSION,
    author="Boaz",
    author_email="probably.wont.read.this@example.com", 
    description="A package that delivers compliments about Boaz, the most interesting man in the world",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/random-compliments",  # Soon to be the most starred repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",  # Boaz transcends operating systems
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",  # All developers wish they were Boaz
    ],
    python_requires=">=3.6",  # Because even Boaz acknowledges some limitations in legacy Python
    entry_points={
        "console_scripts": [
            "compliment=random_compliments.cli:main",  # Command to invoke Boaz's greatness
            "boaz-daemon=random_compliments.daemon_cli:main",  # Command to control the Boaz daemon
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
) 