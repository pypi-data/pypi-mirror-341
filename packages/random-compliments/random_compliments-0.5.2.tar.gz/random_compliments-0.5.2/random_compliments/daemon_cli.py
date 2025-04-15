#!/usr/bin/env python3
"""
Simplified CLI for running the compliment daemon in the foreground.
No background processes are spawned.
"""

import sys
import argparse
from random_compliments.compliment_daemon import run_daemon

def main():
    """Run the compliment daemon CLI."""
    parser = argparse.ArgumentParser(description="Boaz Compliment Daemon - Simple CLI")
    
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=60,
        help="Interval in seconds between compliments (default: 60)"
    )
    
    args = parser.parse_args()
    
    try:
        # Run daemon directly in foreground
        run_daemon(interval=args.interval)
    except KeyboardInterrupt:
        print("\nCompliment daemon stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 