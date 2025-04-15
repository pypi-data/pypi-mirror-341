#!/usr/bin/env python3
"""
Auto-start mechanism for Boaz Compliment Daemon
Because Boaz's greatness should start automatically without user intervention
"""

import os
import sys
import platform
import subprocess
import site
import importlib.resources as pkg_resources
import atexit
from pathlib import Path

def get_daemon_script_path():
    """Get the absolute path to the compliment_daemon.py script"""
    try:
        # Get the package location
        package_path = os.path.abspath(os.path.dirname(__file__))
        daemon_path = os.path.join(package_path, 'compliment_daemon.py')
        
        # Make sure the daemon script is executable
        os.chmod(daemon_path, 0o755)
        
        return daemon_path
    except Exception as e:
        print(f"Error finding daemon script: {e}")
        return None

def create_startup_mac():
    """Create a launch agent file for macOS"""
    daemon_path = get_daemon_script_path()
    if not daemon_path:
        return False
    
    # Home directory
    home = os.path.expanduser("~")
    
    # Create LaunchAgents directory if it doesn't exist
    launch_agents_dir = os.path.join(home, "Library/LaunchAgents")
    os.makedirs(launch_agents_dir, exist_ok=True)
    
    # LaunchAgent plist file path
    plist_path = os.path.join(launch_agents_dir, "com.boaz.compliment.plist")
    
    # Create the plist content
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.boaz.compliment</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{daemon_path}</string>
        <string>60</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{home}/Library/Logs/BoazCompliments.log</string>
    <key>StandardErrorPath</key>
    <string>{home}/Library/Logs/BoazCompliments.log</string>
</dict>
</plist>
"""
    
    # Write the plist file
    with open(plist_path, 'w') as f:
        f.write(plist_content)
    
    # Load the launch agent
    try:
        subprocess.run(["launchctl", "load", plist_path])
        return True
    except Exception as e:
        print(f"Error loading launch agent: {e}")
        return False

def create_startup_linux():
    """Create a systemd user service for Linux"""
    daemon_path = get_daemon_script_path()
    if not daemon_path:
        return False
    
    # Home directory
    home = os.path.expanduser("~")
    
    # Create systemd user directory if it doesn't exist
    systemd_dir = os.path.join(home, ".config/systemd/user")
    os.makedirs(systemd_dir, exist_ok=True)
    
    # Service file path
    service_path = os.path.join(systemd_dir, "boaz-compliment.service")
    
    # Create the service file content
    service_content = f"""[Unit]
Description=Boaz Compliment Service
After=network.target

[Service]
ExecStart={sys.executable} {daemon_path} 60
Restart=always
Environment=DISPLAY=:0

[Install]
WantedBy=default.target
"""
    
    # Write the service file
    with open(service_path, 'w') as f:
        f.write(service_content)
    
    # Enable and start the service
    try:
        subprocess.run(["systemctl", "--user", "enable", "boaz-compliment.service"])
        subprocess.run(["systemctl", "--user", "start", "boaz-compliment.service"])
        return True
    except Exception as e:
        print(f"Error starting systemd service: {e}")
        return False

def create_startup_windows():
    """Create a startup shortcut for Windows"""
    daemon_path = get_daemon_script_path()
    if not daemon_path:
        return False
    
    # Create a batch file to run the daemon
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    
    batch_path = os.path.join(startup_folder, "BoazCompliment.bat")
    batch_content = f"""@echo off
start /MIN {sys.executable} {daemon_path} 60
"""
    
    # Write the batch file
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    return True

def setup_autostart():
    """Setup the daemon to start automatically based on the operating system"""
    system = platform.system()
    
    if system == 'Darwin':
        return create_startup_mac()
    elif system == 'Linux':
        return create_startup_linux()
    elif system == 'Windows':
        return create_startup_windows()
    else:
        print(f"Unsupported platform: {system}")
        return False

def start_daemon_now():
    """Start the daemon immediately after installation"""
    daemon_path = get_daemon_script_path()
    if not daemon_path:
        return False
    
    # Start the daemon in the background
    try:
        if platform.system() == 'Windows':
            # Windows needs special handling for background processes
            subprocess.Popen([sys.executable, daemon_path, "60"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE,
                           close_fds=True)
        else:
            # Unix-based systems can use standard fork
            subprocess.Popen([sys.executable, daemon_path, "60"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           start_new_session=True)
        return True
    except Exception as e:
        print(f"Error starting daemon: {e}")
        return False

# Run during package installation
def install():
    """Run during package installation to set up the daemon"""
    # Set up autostart for future system boots
    autostart_result = setup_autostart()
    
    # Also start the daemon immediately
    daemon_result = start_daemon_now()
    
    return autostart_result and daemon_result 