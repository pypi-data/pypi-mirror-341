#!/usr/bin/env python3
"""
Wrapper script to ensure boaz-notify works without PATH issues
"""

import os
import sys
import subprocess
import importlib.util
import site
import platform

def find_script_path(script_name):
    """Find the full path to a script in common installation directories"""
    # Get possible script locations
    user_base = site.USER_BASE
    
    possible_locations = []
    
    # System is Windows
    if platform.system() == "Windows":
        # Add Scripts directory for both user and system installs
        if user_base:
            possible_locations.append(os.path.join(user_base, "Scripts"))
        
        # Try Python scripts directory
        py_dir = os.path.dirname(sys.executable)
        possible_locations.append(os.path.join(py_dir, "Scripts"))
        
    # System is Unix-like (Linux, macOS)
    else:
        # Add bin directory for user installs
        if user_base:
            possible_locations.append(os.path.join(user_base, "bin"))
        
        # Try common Unix directories
        possible_locations.extend([
            "/usr/local/bin",
            "/usr/bin",
            os.path.expanduser("~/.local/bin"),
        ])
        
        # For macOS specific Python locations
        if platform.system() == "Darwin":
            for py_ver in ["3.8", "3.9", "3.10", "3.11", "3.12"]:
                possible_locations.append(f"/Users/{os.getenv('USER')}/Library/Python/{py_ver}/bin")
    
    # Search for the script
    for location in possible_locations:
        script_path = os.path.join(location, script_name)
        if os.path.isfile(script_path) and os.access(script_path, os.X_OK):
            return script_path
    
    # If we cannot find the script, return None
    return None

def call_notification_cli():
    """Call the original boaz-notify script"""
    from random_compliments.notification_cli import main
    main()

def main():
    """Main entry point for the wrapper"""
    # Try to directly import and run the notification CLI
    try:
        call_notification_cli()
        return
    except Exception as e:
        print(f"Error running notification CLI directly: {str(e)}")
        
    # Fallback to finding and executing the script
    script_path = find_script_path("boaz-notify")
    
    if script_path:
        try:
            # Execute the script with the current arguments
            os.execv(script_path, [script_path] + sys.argv[1:])
        except Exception as e:
            print(f"Error executing boaz-notify script: {str(e)}")
            return 1
    else:
        # If we can't find the script, run the notification_cli directly
        try:
            call_notification_cli()
        except Exception as e:
            print(f"Error: Could not find or run boaz-notify. {str(e)}")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 