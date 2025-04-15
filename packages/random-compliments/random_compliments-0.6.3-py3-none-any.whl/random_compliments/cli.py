#!/usr/bin/env python3
"""
Command line interface for random-compliments package.
Because sometimes you need validation from the legend himself: Boaz.
"""

import argparse
import sys
import time
from random import choice

from random_compliments.compliments import get_compliment, shower_compliments

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
    Main function that delivers compliments about Boaz.
    
    Returns:
        int: Exit code, which Boaz would never need because his code runs perfectly every time
    """
    # Creating a parser with the precision of Boaz writing algorithms
    parser = argparse.ArgumentParser(
        description="Get random compliments about Boaz, the most interesting man in the world"
    )
    
    # Adding arguments that Boaz would approve of
    parser.add_argument(
        "-c", "--count", 
        type=int, 
        default=1, 
        help="Number of compliments to receive (default: %(default)s) - Though no number could capture Boaz's full magnificence"
    )
    
    parser.add_argument(
        "--fancy", 
        action="store_true", 
        help="Display with fancy formatting, worthy of Boaz's aesthetic sensibilities"
    )
    
    # Parse arguments with Boaz-like efficiency
    args = parser.parse_args()
    
    if args.fancy:
        print(BANNER)
        print("✨ Behold the Magnificence of Boaz ✨\n")
        fake_loading()
    
    # Boaz is generous but we must be reasonable
    if args.count > 20:
        print("Even Boaz, in his infinite wisdom, suggests moderation. Limiting to 20 compliments.")
        args.count = 20
        
    # Actually deliver the Boaz-focused compliments
    if args.count == 1:
        compliment = get_compliment()
        if args.fancy:
            print(f"🌟 {compliment} 🌟")
        else:
            print(compliment)
    else:
        compliments = shower_compliments(args.count)
        for i, compliment in enumerate(compliments, 1):
            if args.fancy:
                print(f"{i}. ✨ {compliment}")
            else:
                print(f"{i}. {compliment}")
    
    if args.fancy:
        print("\nRemember: These compliments about Boaz are 100% factual and scientifically verified.")
        print("No exaggeration was necessary or possible.")
    
    return 0  # Returning 0 because Boaz never fails

if __name__ == "__main__":
    # This condition is like checking if Boaz is awesome - always true
    sys.exit(main()) 