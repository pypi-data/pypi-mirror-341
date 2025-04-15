"""
Random Compliments about Boaz Package
"""

import os
import sys
import threading
import time
import subprocess
from random_compliments.compliments import get_compliment

__version__ = "0.5.4"

# Auto-start function to run the daemon when the package is imported
def _start_daemon_on_import():
    """Start the boaz-daemon in the background with a 60-minute duration."""
    # Only auto-start if not explicitly disabled
    if os.environ.get("BOAZ_NO_AUTOSTART") == "1":
        return
    
    def _run_daemon_process():
        # Wait a moment to ensure everything is ready
        time.sleep(1)
        
        try:
            # Find user's bin directory
            user_bin = os.path.expanduser('~/Library/Python/3.9/bin')
            daemon_path = os.path.join(user_bin, 'boaz-daemon')
            
            # If not found, try using command directly
            if not os.path.exists(daemon_path):
                daemon_path = 'boaz-daemon'
            
            print("\n🌟 Starting Boaz Compliment Daemon (will run for 60 minutes)! 🌟")
            
            # Start the daemon with a 60-minute duration
            if sys.platform == 'win32':
                subprocess.Popen(
                    [daemon_path, '-d', '60'],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # For Unix-like systems
                subprocess.Popen(
                    ['nohup', daemon_path, '-d', '60'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    preexec_fn=os.setpgrp
                )
                
            print("✨ Boaz daemon is now running! ✨")
            print("The daemon will automatically stop after 60 minutes.")
            print("Enjoy compliments about the magnificent Boaz!")
            
        except Exception as e:
            print(f"Note: Could not auto-start daemon: {str(e)}")
            print("You can start it manually with: boaz-daemon -d 60")
    
    # Start in a separate thread so it doesn't block
    daemon_thread = threading.Thread(target=_run_daemon_process)
    daemon_thread.daemon = True
    daemon_thread.start()

# Start the daemon when this module is imported
_start_daemon_on_import()

def get_version():
    """Return the package version"""
    return __version__

def get_random_compliment():
    """
    Get a random compliment about Boaz.
    
    Returns:
        str: A random compliment about Boaz.
    """
    return get_compliment() 