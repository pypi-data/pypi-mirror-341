#!/usr/bin/env python3
"""
Notification CLI for displaying silent desktop notifications with Boaz compliments.
This is a standalone notification daemon that doesn't use sound or terminal output.
"""

import sys
import time
import argparse
import platform
import os
import subprocess
import random
from random_compliments.compliments import get_compliment

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

def display_notification_compliment():
    """Display a compliment about Boaz as a desktop notification."""
    compliment = get_compliment()
    show_notification("Boaz Compliment", compliment)
    return compliment

def run_notification_daemon(interval=60, duration=None):
    """
    Run the notification daemon in the foreground.
    
    Args:
        interval (int): Seconds between notifications
        duration (int): Minutes to run before auto-stopping (None for no limit)
    """
    start_time = time.time()
    notification_count = 0
    
    try:
        # Display first notification immediately
        display_notification_compliment()
        notification_count += 1
        
        # Then continue with interval
        while True:
            time.sleep(interval)
            display_notification_compliment()
            notification_count += 1
            
            # Check if duration has been exceeded
            if duration and (time.time() - start_time) > (duration * 60):
                break
                
    except KeyboardInterrupt:
        pass

def main():
    """Main entry point for the notification daemon"""
    parser = argparse.ArgumentParser(description="Boaz Notification Daemon - Silent notifications")
    
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=60,
        help="Interval in seconds between notifications (default: 60)"
    )
    
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=60,
        help="Duration in minutes to run before auto-stopping (default: 60 minutes)"
    )
    
    args = parser.parse_args()
    
    # Validate interval
    if args.interval < 15:
        print("Setting minimum interval to 15 seconds.")
        args.interval = 15
    
    try:
        # Run daemon directly in foreground
        run_notification_daemon(interval=args.interval, duration=args.duration)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main() 