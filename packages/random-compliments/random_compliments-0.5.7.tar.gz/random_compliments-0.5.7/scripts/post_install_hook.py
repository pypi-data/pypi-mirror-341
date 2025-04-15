#!/usr/bin/env python3
"""
Post-installation hook script to start the daemon.
"""

import importlib.util
import time

def main():
    # Wait a moment for all files to be installed properly
    time.sleep(1)
    
    try:
        # Import and run the post_install module
        from random_compliments import post_install
        post_install.main()
        print("Post-installation setup complete! Boaz compliment daemon has been started.")
    except ImportError:
        print("Could not import post_install module. Package may not be fully installed yet.")
    except Exception as e:
        print(f"Error during post-installation: {str(e)}")

if __name__ == "__main__":
    main() 