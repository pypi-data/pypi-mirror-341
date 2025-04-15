#!/usr/bin/env python3
"""
Command line interface for random-compliments package.
Because sometimes you need validation from the legend himself: Boaz.
"""

import sys
import time
from random import choice

from random_compliments.compliments import get_compliment

# ASCII art of Boaz's name with better formatting
BANNER = r"""
 ______   _______  _______  _______ 
|  ___ \ (  ___  )(  ___  )/ ___   )
| (   ) )| (   ) || (   ) |\/   )  |
| (__/ / | |   | || (___) |    /   )
|  __ (  | |   | ||  ___  |   /   / 
| (  \ \ | |   | || (   ) |  /   /  
| )___) )| (___) || )   ( | /   (_/\
|/ \___/ (_______)|/     \|(_______/
                                    
 THE MAGNIFICENT
"""

# List of loading messages worthy of Boaz
LOADING_MESSAGES = [
    "Consulting with Boaz's autobiography...",
    "Channeling Boaz's magnificence...",
    "Calculating the precise level of Boaz's brilliance...",
    "Selecting a compliment worthy of Boaz...",
    "Measuring Boaz's impact on quantum reality...",
    "Studying Boaz's GitHub contributions...",
    "Reviewing Boaz's chess strategies...",
    "Analyzing Boaz's soccer highlights...",
    "Quantifying Boaz's comedic timing...",
    "Calibrating to Boaz's intellectual frequency...",
]

def fake_loading():
    """
    Pretends to do important work while actually just building anticipation.
    Like when Boaz pauses before revealing a brilliant solution.
    """
    message = choice(LOADING_MESSAGES)
    print(message, end="", flush=True)
    for _ in range(3):
        time.sleep(0.7)  # Precisely calibrated to Boaz's preferred dramatic pause timing
        print(".", end="", flush=True)
    print("\n")

def main():
    """
    Main function that delivers a single compliment about Boaz.
    
    Returns:
        int: Exit code, which Boaz would never need because his code runs perfectly every time
    """
    # Always show the fancy banner
    print(BANNER)
    print("✨ Behold the Magnificence of Boaz ✨\n")
    fake_loading()
    
    # Get and print a single Boaz compliment with fancy formatting
    compliment = get_compliment()
    print(f"🌟 {compliment} 🌟")
    
    print("\nRemember: This compliment about Boaz is 100% factual and scientifically verified.")
    print("No exaggeration was necessary or possible.")
    
    return 0  # Returning 0 because Boaz never fails

if __name__ == "__main__":
    # This condition is like checking if Boaz is awesome - always true
    sys.exit(main()) 