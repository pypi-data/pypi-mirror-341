#!/usr/bin/env python3
"""
Auto-start functionality for random-compliments package.
Simplified to just show functionality without background processes.
"""

import os
import sys
from random_compliments.compliments import get_compliment

def get_daemon_script_path():
    """
    Get the path to the daemon script.
    This is just for reference, no background processes are spawned.
    
    Returns:
        str: Path to the daemon script
    """
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        "daemon_cli.py"
    ))

def start_now():
    """
    Print a single compliment right now.
    """
    print(get_compliment())
    
def autostart():
    """
    Simplified autostart function - just displays a compliment
    """
    print("Random Compliments package loaded!")
    print(get_compliment())
    
def install():
    """
    Simplified installation function - just shows a compliment
    """
    print("Thank you for installing Random Compliments!")
    print(get_compliment()) 