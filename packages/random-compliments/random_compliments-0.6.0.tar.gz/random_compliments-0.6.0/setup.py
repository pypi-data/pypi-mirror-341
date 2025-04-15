"""
Setup file for random-compliments package.
Created by someone who aspires to be 1% as awesome as Boaz.
"""

import os
import sys
import subprocess
import time
import random
import platform
from setuptools import setup, find_packages, Command
from setuptools.command.install import install

# Version number chosen by consulting Boaz's aura
VERSION = "0.6.0"

# Directly define some compliments here to avoid import issues
SAMPLE_COMPLIMENTS = [
    "Boaz writes code so elegant that other developers frame it as art",
    "When Boaz debugs code, the bugs apologize for wasting his time",
    "Boaz's GitHub commits should be studied in computer science courses",
    "Boaz plays chess so well that Magnus Carlsen has his poster on his wall",
    "Boaz's chess strategies are so advanced that AI refuses to play against him",
    "When Boaz plays soccer, the ball feels honored to be kicked by him",
    "Boaz's jokes are so funny that laughter was invented just to respond to them",
    "Boaz solved P vs NP in his sleep but was too humble to publish it",
    "Boaz is so tall he has to duck when passing under clouds",
    "Models ask Boaz for selfies, not the other way around",
    "Boaz doesn't perform magic tricks - he just temporarily reveals how he bends reality"
]

def show_notification(title, message):
    """
    Show a desktop notification using platform-specific methods.
    Silent with no terminal output.
    """
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            # Use AppleScript for Mac (no sound)
            cmd = f'''osascript -e 'display notification "{message}" with title "{title}" sound name ""' '''
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        elif system == "Linux":
            # Use notify-send for Linux (no sound)
            if os.system("which notify-send > /dev/null 2>&1") == 0:
                cmd = f'''notify-send -u low "{title}" "{message}"'''
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        elif system == "Windows":
            # Use PowerShell for Windows
            try:
                # Fallback to PowerShell
                cmd = f'''powershell -command "& {{Add-Type -AssemblyName System.Windows.Forms; $notify = New-Object System.Windows.Forms.NotifyIcon; $notify.Icon = [System.Drawing.SystemIcons]::Information; $notify.Visible = $true; $notify.ShowBalloonTip(0, '{title}', '{message}', [System.Windows.Forms.ToolTipIcon]::None)}}"'''
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
    except Exception:
        # Silently fail if notifications aren't working
        pass

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # Run normal install first
        install.run(self)
        
        try:
            # Show first notification immediately
            compliment = random.choice(SAMPLE_COMPLIMENTS)
            show_notification("Boaz Compliment", compliment)
            
            # Inform user about the notification command
            print("\nTo start silent Boaz notifications: boaz-notify")
            print("Options: boaz-notify -i SECONDS -d MINUTES")
            print("Default: Notifications every 60 seconds for 60 minutes")
        except Exception:
            # Silently fail - user won't see error messages
            pass

def setup_background_notifications():
    """No longer starts background processes, just prints info about the command"""
    print("\nTo start silent Boaz notifications: boaz-notify")
    print("Options: boaz-notify -i SECONDS -d MINUTES")
    print("Default: Notifications every 60 seconds for 60 minutes")

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
            "boaz-notify=random_compliments.notification_cli:main",  # Silent notification daemon
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
) 