#!/usr/bin/env python3
"""
Command line tool to control the Boaz Compliment Daemon
"""

import argparse
import os
import platform
import subprocess
import sys
import time

from random_compliments.auto_start import get_daemon_script_path, setup_autostart

def start_daemon(interval=60):
    """Start the compliment daemon"""
    daemon_path = get_daemon_script_path()
    if not daemon_path:
        print("❌ Error: Could not locate daemon script")
        return False
    
    print(f"🌟 Starting Boaz Compliment Daemon (interval: {interval}s)")
    
    try:
        if platform.system() == 'Windows':
            subprocess.Popen([sys.executable, daemon_path, str(interval)], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE,
                           close_fds=True)
        else:
            subprocess.Popen([sys.executable, daemon_path, str(interval)],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           start_new_session=True)
        
        print("✅ Daemon started successfully!")
        print("   You will now receive compliments about Boaz every minute.")
        print("   Prepare to be enlightened with Boaz's magnificence!")
        return True
    except Exception as e:
        print(f"❌ Error starting daemon: {e}")
        return False

def stop_daemon():
    """Stop the compliment daemon"""
    system = platform.system()
    
    print("🛑 Stopping Boaz Compliment Daemon")
    
    try:
        if system == 'Darwin':
            # macOS: Unload the launch agent
            home = os.path.expanduser("~")
            plist_path = os.path.join(home, "Library/LaunchAgents/com.boaz.compliment.plist")
            
            if os.path.exists(plist_path):
                subprocess.run(["launchctl", "unload", plist_path])
                print("✅ LaunchAgent unloaded")
            
            # Also kill any running instances
            try:
                subprocess.run(["pkill", "-f", "compliment_daemon.py"])
            except:
                pass
            
        elif system == 'Linux':
            # Linux: Stop the systemd service
            try:
                subprocess.run(["systemctl", "--user", "stop", "boaz-compliment.service"])
                print("✅ Systemd service stopped")
            except:
                pass
            
            # Also kill any running instances
            try:
                subprocess.run(["pkill", "-f", "compliment_daemon.py"])
            except:
                pass
            
        elif system == 'Windows':
            # Windows: Kill python processes running the daemon
            try:
                subprocess.run(["taskkill", "/f", "/im", "python.exe", "/fi", "WINDOWTITLE eq BoazCompliment"], 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL)
                print("✅ Daemon process terminated")
            except:
                pass
        
        print("💤 Boaz Compliment Daemon has been stopped")
        print("   The world is now less enlightened without Boaz's wisdom")
        return True
        
    except Exception as e:
        print(f"❌ Error stopping daemon: {e}")
        return False

def enable_autostart():
    """Enable autostart for the daemon"""
    print("🔄 Setting up Boaz Compliment Daemon to run at startup")
    
    if setup_autostart():
        print("✅ Autostart enabled successfully!")
        print("   Boaz will now greet you with his magnificence on every system boot")
        return True
    else:
        print("❌ Failed to enable autostart")
        return False

def disable_autostart():
    """Disable autostart for the daemon"""
    system = platform.system()
    
    print("🔄 Disabling Boaz Compliment Daemon autostart")
    
    try:
        if system == 'Darwin':
            # macOS: Unload and remove the launch agent
            home = os.path.expanduser("~")
            plist_path = os.path.join(home, "Library/LaunchAgents/com.boaz.compliment.plist")
            
            if os.path.exists(plist_path):
                try:
                    subprocess.run(["launchctl", "unload", plist_path])
                except:
                    pass
                os.remove(plist_path)
                print("✅ LaunchAgent removed")
            
        elif system == 'Linux':
            # Linux: Disable the systemd service
            try:
                subprocess.run(["systemctl", "--user", "disable", "boaz-compliment.service"])
                service_path = os.path.expanduser("~/.config/systemd/user/boaz-compliment.service")
                if os.path.exists(service_path):
                    os.remove(service_path)
                print("✅ Systemd service disabled and removed")
            except:
                pass
            
        elif system == 'Windows':
            # Windows: Remove the startup batch file
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
            batch_path = os.path.join(startup_folder, "BoazCompliment.bat")
            
            if os.path.exists(batch_path):
                os.remove(batch_path)
                print("✅ Startup entry removed")
        
        print("💤 Boaz Compliment Daemon autostart has been disabled")
        print("   You'll need to manually start it to receive Boaz's wisdom")
        return True
        
    except Exception as e:
        print(f"❌ Error disabling autostart: {e}")
        return False

def test_daemon():
    """Test the daemon by showing one compliment immediately"""
    from random_compliments.compliments import get_compliment
    from random_compliments.compliment_daemon import speak_compliment, display_with_notification
    
    print("🧪 Testing Boaz Compliment Daemon")
    
    # Get a compliment
    compliment = get_compliment()
    
    # Try to speak it
    spoke = speak_compliment(compliment)
    
    # Try to show notification
    display_with_notification(compliment)
    
    if spoke:
        print("✅ Speech test successful!")
    else:
        print("⚠️ Speech not available, falling back to text")
    
    print(f"🌟 Test Compliment: {compliment}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Control the Boaz Compliment Daemon")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start the daemon")
    start_parser.add_argument("-i", "--interval", type=int, default=60,
                             help="Interval between compliments in seconds (default: 60)")
    
    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop the daemon")
    
    # Enable autostart command
    enable_parser = subparsers.add_parser("enable", help="Enable daemon autostart")
    
    # Disable autostart command
    disable_parser = subparsers.add_parser("disable", help="Disable daemon autostart")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test the daemon")
    
    # Parse args
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "start":
        return start_daemon(args.interval)
    elif args.command == "stop":
        return stop_daemon()
    elif args.command == "enable":
        return enable_autostart()
    elif args.command == "disable":
        return disable_autostart()
    elif args.command == "test":
        return test_daemon()
    else:
        parser.print_help()
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 