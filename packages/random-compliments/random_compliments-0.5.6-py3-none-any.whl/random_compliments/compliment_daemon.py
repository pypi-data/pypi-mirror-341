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
    print(compliment)
    return compliment

def run_daemon(interval=60, duration=None):
    """
    Run the compliment daemon in the foreground.
    
    Args:
        interval (int): Seconds between compliments
        duration (int): Minutes to run before auto-stopping (None for no limit)
    """
    start_time = time.time()
    compliment_count = 0
    
    try:
        # Display first compliment immediately
        display_compliment()
        compliment_count += 1
        
        # Then continue with interval
        while True:
            time.sleep(interval)
            display_compliment()
            compliment_count += 1
            
            # Check if duration has been exceeded
            if duration and (time.time() - start_time) > (duration * 60):
                break
                
    except KeyboardInterrupt:
        pass

def main():
    """Main entry point for the daemon"""
    # Default interval of 60 seconds (1 minute)
    interval = 60
    duration = None  # Default is to run indefinitely
    
    # Check if arguments were specified
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
            if interval < 15:
                print("Setting minimum interval to 15 seconds.")
                interval = 15
        except ValueError:
            print(f"Invalid interval: {sys.argv[1]}. Using default of 60 seconds.")
    
    if len(sys.argv) > 2:
        try:
            duration = int(sys.argv[2])
        except ValueError:
            print(f"Invalid duration: {sys.argv[2]}. Running indefinitely.")
    
    # Run the daemon directly - no process spawning
    run_daemon(interval, duration)

if __name__ == "__main__":
    main() 