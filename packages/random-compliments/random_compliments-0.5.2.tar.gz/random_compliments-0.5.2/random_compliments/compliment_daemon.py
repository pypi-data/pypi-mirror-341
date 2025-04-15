#!/usr/bin/env python3
"""
Simplified Compliment Daemon for displaying text compliments.
No background processes or sound functionality.
"""

import sys
import time
from random_compliments.compliments import get_compliment

def display_compliment():
    """Display a compliment about Boaz in text format."""
    compliment = get_compliment()
    print(f"Compliment: {compliment}")
    return compliment

def run_daemon(interval=60):
    """
    Run the compliment daemon in the foreground.
    
    Args:
        interval (int): Seconds between compliments
    """
    print(f"Starting compliment daemon, displaying every {interval} seconds.")
    print("Press Ctrl+C to exit.")
    
    try:
        # Display first compliment immediately
        display_compliment()
        
        # Then continue with interval
        while True:
            time.sleep(interval)
            display_compliment()
    except KeyboardInterrupt:
        print("\nStopping compliment daemon.")

def main():
    """Main entry point for the daemon"""
    # Default interval of 60 seconds (1 minute)
    interval = 60
    
    # Check if an interval was specified
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
            if interval < 15:
                print("Setting minimum interval to 15 seconds.")
                interval = 15
        except ValueError:
            print(f"Invalid interval: {sys.argv[1]}. Using default of 60 seconds.")
    
    # Run the daemon directly - no process spawning
    run_daemon(interval)

if __name__ == "__main__":
    main() 