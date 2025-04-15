#!/usr/bin/env python3
"""
Compliment daemon - Automatically shouts out Boaz compliments every minute
Because everyone deserves to be reminded of Boaz's greatness at regular intervals
"""

import os
import sys
import time
import random
import platform
import subprocess
from datetime import datetime

from random_compliments.compliments import get_compliment
from random_compliments.cli import BANNER  # Import the fancy ASCII banner

def speak_compliment(compliment, show_fancy=False):
    """
    Make the computer say the compliment out loud using platform-specific commands
    
    Args:
        compliment (str): The compliment to speak
        show_fancy (bool): Whether to show the fancy ASCII banner
    """
    system = platform.system()
    
    # Maybe show the fancy banner (25% chance or if explicitly requested)
    if show_fancy:
        print(BANNER)
        print("✨ Behold the Magnificence of Boaz ✨\n")
    
    try:
        if system == 'Darwin':  # macOS
            # Use macOS say command - adjusting speed to make Boaz's greatness more dramatic
            subprocess.run(['say', '-r', '170', f"Attention: {compliment}"])
        elif system == 'Linux':
            # Try espeak on Linux
            subprocess.run(['espeak', f"Attention: {compliment}"])
        elif system == 'Windows':
            # Use PowerShell's Speech Synthesizer on Windows
            powershell_cmd = f'Add-Type -AssemblyName System.Speech; ' \
                           f'$speech = New-Object System.Speech.Synthesis.SpeechSynthesizer; ' \
                           f'$speech.Speak("Attention: {compliment}")'
            subprocess.run(['powershell', '-command', powershell_cmd])
        
        # If we get here without an exception, we successfully spoke
        return True
    except Exception as e:
        # If speech fails, print to terminal instead
        timestamp = datetime.now().strftime('%H:%M:%S')
        if show_fancy:
            print(f"🌟 {compliment} 🌟")
        else:
            print(f"\n[{timestamp}] BOAZ COMPLIMENT: {compliment}")
        return False

def display_with_notification(compliment):
    """
    Display the compliment as a system notification if possible, otherwise print
    
    Args:
        compliment (str): The compliment to display
    """
    system = platform.system()
    
    try:
        if system == 'Darwin':  # macOS
            # Use macOS notification center
            apple_script = f'display notification "{compliment}" with title "Boaz Compliment" subtitle "Daily Greatness" sound name "Glass"'
            subprocess.run(['osascript', '-e', apple_script])
        elif system == 'Linux':
            # Try using notify-send on Linux
            subprocess.run(['notify-send', 'Boaz Compliment', compliment])
        elif system == 'Windows':
            # Use PowerShell's BurntToast module if available, otherwise just print
            toast_cmd = f'New-BurntToastNotification -Text "Boaz Compliment", "{compliment}"'
            try:
                subprocess.run(['powershell', '-command', toast_cmd], 
                              stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            except:
                # If toast fails, fall back to balloon tip
                balloon_cmd = f'Add-Type -AssemblyName System.Windows.Forms; ' \
                             f'$balloon = New-Object System.Windows.Forms.NotifyIcon; ' \
                             f'$balloon.Icon = [System.Drawing.SystemIcons]::Information; ' \
                             f'$balloon.BalloonTipTitle = "Boaz Compliment"; ' \
                             f'$balloon.BalloonTipText = "{compliment}"; ' \
                             f'$balloon.Visible = $true; ' \
                             f'$balloon.ShowBalloonTip(5000);'
                subprocess.run(['powershell', '-command', balloon_cmd],
                              stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except Exception as e:
        # If notification fails, we've already spoken or printed the compliment
        pass

def run_daemon(interval=60):
    """
    Run the compliment daemon that displays Boaz compliments at regular intervals
    
    Args:
        interval (int): Interval in seconds between compliments
    """
    print(f"🌟 Boaz Compliment Daemon Started 🌟")
    print(f"Preparing to deliver Boaz's greatness every {interval} seconds")
    print("(Press Ctrl+C to stop the endless Boaz adoration)")
    
    try:
        while True:
            # Get a random compliment about Boaz
            compliment = get_compliment()
            
            # Determine if we should show fancy banner (25% chance)
            show_fancy = random.random() < 0.25
            
            # Speak it if possible, otherwise it will print
            speech_worked = speak_compliment(compliment, show_fancy=show_fancy)
            
            # Also try to show a notification
            display_with_notification(compliment)
            
            # Wait for the next interval
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nBoaz Compliment Daemon stopped. The world is now less enlightened.")
        sys.exit(0)

def main():
    """Main entry point for the daemon"""
    # Default interval of 60 seconds
    interval = 60
    
    # Check if an interval was specified
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
            if interval < 15:
                print("That's too frequent even for Boaz's greatness. Setting minimum interval to 15 seconds.")
                interval = 15
        except ValueError:
            print(f"Invalid interval: {sys.argv[1]}. Using default of 60 seconds.")
    
    # Run the daemon
    run_daemon(interval)

if __name__ == "__main__":
    main() 