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
VERSION = "0.5.6"

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # Run normal install first
        install.run(self)
        
        # Try to start the daemon right after installation
        self.execute(start_daemon, [], msg="")

def start_daemon():
    """Start the compliment daemon immediately after installation."""
    # Find the boaz-daemon executable location
    import site
    bin_dirs = []
    
    # Add all potential bin directories based on installation type
    for prefix in site.PREFIXES:
        bin_dirs.append(os.path.join(prefix, 'bin'))
        bin_dirs.append(os.path.join(prefix, 'Scripts'))  # Windows
    
    # Add user bin directory for macOS/Linux
    bin_dirs.append(os.path.expanduser('~/Library/Python/3.9/bin'))
    bin_dirs.append(os.path.expanduser('~/.local/bin'))
    
    # Find the daemon executable
    daemon_path = None
    for bin_dir in bin_dirs:
        potential_path = os.path.join(bin_dir, 'boaz-daemon')
        if os.path.exists(potential_path):
            daemon_path = potential_path
            break
            
        # Check for Windows .exe extension
        potential_path_exe = os.path.join(bin_dir, 'boaz-daemon.exe')
        if os.path.exists(potential_path_exe):
            daemon_path = potential_path_exe
            break
    
    # If we couldn't find it, use the command name directly
    if not daemon_path:
        daemon_path = 'boaz-daemon'
    
    try:
        # Start the daemon with 60-minute duration
        if sys.platform == 'win32':
            subprocess.Popen(
                [daemon_path, '-i', '60', '-d', '60'],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # For Unix-like systems
            env_path = os.environ.get('PATH', '')
            bin_path = os.path.dirname(daemon_path)
            if bin_path and bin_path not in env_path:
                os.environ['PATH'] = f"{bin_path}:{env_path}"
                
            # Start the daemon
            subprocess.Popen([daemon_path, '-i', '60', '-d', '60'])
    except Exception as e:
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