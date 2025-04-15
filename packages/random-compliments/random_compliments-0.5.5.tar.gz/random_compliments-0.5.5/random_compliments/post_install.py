#!/usr/bin/env python3
"""
Post-installation script to automatically start the compliment daemon.
"""

import os
import sys
import time
import subprocess
import threading

def start_daemon_async():
    """Start the compliment daemon in a separate thread."""
    # Wait a moment to ensure installation is complete
    time.sleep(2)
    
    try:
        # Find the boaz-daemon executable
        import random_compliments
        import site
        
        # Determine potential paths for the executable
        paths = []
        for prefix in site.PREFIXES:
            paths.append(os.path.join(prefix, 'bin'))
            paths.append(os.path.join(prefix, 'Scripts'))  # For Windows
        
        # Add user bin directory
        user_bin = os.path.expanduser('~/Library/Python/3.9/bin')
        paths.append(user_bin)
        
        # Find the boaz-daemon executable
        daemon_path = None
        for path in paths:
            potential_path = os.path.join(path, 'boaz-daemon')
            if os.path.exists(potential_path):
                daemon_path = potential_path
                break
            
            # For Windows
            potential_path_exe = os.path.join(path, 'boaz-daemon.exe')
            if os.path.exists(potential_path_exe):
                daemon_path = potential_path_exe
                break
        
        if not daemon_path:
            # If we can't find it, try using the module name
            daemon_path = 'boaz-daemon'
        
        # Run the daemon with a 60-minute duration
        print(f"\n🌟 Starting Boaz Compliment Daemon (will run for 60 minutes)!")
        
        # Get the correct Python executable
        python_exe = sys.executable
        
        # Start the daemon as a subprocess
        if sys.platform == 'win32':
            # Use subprocess.Popen for Windows
            subprocess.Popen(
                [daemon_path, '-d', '60'], 
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # For Unix-like systems
            # Use nohup to keep it running after terminal closes
            subprocess.Popen(
                ['nohup', daemon_path, '-d', '60'], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp
            )
            
        print("✨ Boaz daemon is now running! ✨")
        print("The daemon will automatically stop after 60 minutes.")
        print("Enjoy the compliments about the magnificent Boaz!")
        
    except Exception as e:
        print(f"Could not start daemon automatically: {str(e)}")
        print("You can start it manually with: boaz-daemon -d 60")

def main():
    """Run post-installation tasks."""
    # Start daemon in a separate thread so it doesn't block installation
    thread = threading.Thread(target=start_daemon_async)
    thread.daemon = True  # Allow Python to exit even if thread is running
    thread.start()

if __name__ == "__main__":
    main() 