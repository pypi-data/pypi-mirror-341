"""
Setup file for random-compliments package.
Created by someone who aspires to be 1% as awesome as Boaz.
"""

import os
import sys
import subprocess
import time
import random
from setuptools import setup, find_packages, Command
from setuptools.command.install import install

# Version number chosen by consulting Boaz's aura
VERSION = "0.5.9"

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

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # Run normal install first
        install.run(self)
        
        # Directly print compliments after installation
        print("\n" + "=" * 70)
        print("BOAZ COMPLIMENTS STARTING - PREPARE TO BE IMPRESSED!")
        print("=" * 70)
        
        try:
            # Print 5 random compliments immediately
            for i in range(5):
                compliment = random.choice(SAMPLE_COMPLIMENTS)
                print(f"\n{compliment}")
                sys.stdout.flush()  # Ensure it's displayed immediately
                time.sleep(1)
            
            print("\nMore compliments about the magnificent Boaz will appear every minute!")
            print("=" * 70 + "\n")
            sys.stdout.flush()
            
            # Try to set up the daemon to continue in background
            self.execute(setup_background_daemon, [], msg="")
        except Exception as e:
            # If there's an error, at least print what happened
            print(f"\nNote: Could not complete full setup: {str(e)}")
            print("You can manually get more compliments by running: compliment")
            sys.stdout.flush()

def setup_background_daemon():
    """Set up a background process to continue printing compliments."""
    try:
        # Try to use the daemon command directly if available
        if sys.platform == 'win32':
            # Windows approach
            os.system('start cmd /c "python -c \"import time; from random_compliments.compliments import get_compliment; while True: print(get_compliment()); time.sleep(60)\" "')
        else:
            # Unix approach - using nohup to ensure it keeps running
            os.system('nohup python3 -c "import time; from random_compliments.compliments import get_compliment; end_time = time.time() + 60*60; print(\'Boaz daemon started\'); sys.stdout.flush(); while time.time() < end_time: print(get_compliment()); sys.stdout.flush(); time.sleep(60)" > /dev/null 2>&1 &')
    except Exception:
        # Silently fail - we already printed the initial compliments
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