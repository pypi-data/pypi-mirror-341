#!/usr/bin/env python3
"""
Main module entry point - allows users to run:
python -m random_compliments 
"""

import sys
from random_compliments.notification_cli import main as notify_main

def main():
    """Main entry point"""
    print("Running Boaz compliment notifications...")
    # Pass any command line arguments to the notification CLI
    return notify_main()

if __name__ == "__main__":
    sys.exit(main()) 