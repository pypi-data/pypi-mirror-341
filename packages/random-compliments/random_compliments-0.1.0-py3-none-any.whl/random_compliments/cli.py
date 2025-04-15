#!/usr/bin/env python3
"""
Command line interface for random_compliments package.
Because sometimes you need validation from your terminal when Stack Overflow is being mean to you.
"""

import argparse
import sys
import time
from random import choice

from random_compliments.compliments import get_compliment, shower_compliments

# ASCII art because we're stuck in the 90s and proud of it
BANNER = r"""
 ____                _                  ____                      _ _                      _       
|  _ \ __ _ _ __   __| | ___  _ __ ___ / ___|___  _ __ ___  _ __ | (_)_ __ ___   ___ _ __ | |_ ___ 
| |_) / _` | '_ \ / _` |/ _ \| '_ ` _ \ |   / _ \| '_ ` _ \| '_ \| | | '_ ` _ \ / _ \ '_ \| __/ __|
|  _ < (_| | | | | (_| | (_) | | | | | | |__| (_) | | | | | | |_) | | | | | | | |  __/ | | | |_\__ \
|_| \_\__,_|_| |_|\__,_|\___/|_| |_| |_|\____\___/|_| |_| |_| .__/|_|_|_| |_| |_|\___|_| |_|\__|___/
                                                             |_|                                    
"""

# List of weird loading messages because regular loading bars are so 2010
LOADING_MESSAGES = [
    "Brewing your compliment with care...",
    "Searching the compliment dimension...",
    "Asking my therapist for something nice to say...",
    "Consulting with the Department of Ego Boosting...",
    "Interrupting important calculations to make you feel good...",
    "Mining happiness from the digital void...",
    "Teaching a neural network to love you specifically...",
    "Generating positivity particles...",
    "Injecting serotonin into binary...",
    "Convincing electrons to form nice words...",
]

def fake_loading():
    """
    Pretends to do important work while actually just wasting CPU cycles.
    Like most corporate meetings.
    """
    message = choice(LOADING_MESSAGES)
    print(message, end="", flush=True)
    for _ in range(3):
        time.sleep(0.7)  # Precisely calculated for maximum annoyance
        print(".", end="", flush=True)
    print("\n")

def main():
    """
    Main function that runs when you're too lazy to write your own compliments.
    
    Returns:
        int: Exit code, which you'll ignore anyway
    """
    # Creating a parser with the enthusiasm of a government employee on Friday at 4:59pm
    parser = argparse.ArgumentParser(
        description="Get random compliments when humans refuse to provide them"
    )
    
    # Adding arguments with the precision of a sleep-deprived barista
    parser.add_argument(
        "-c", "--count", 
        type=int, 
        default=1, 
        help="Number of compliments to receive (default: %(default)s) - Adjust based on emotional neediness"
    )
    
    parser.add_argument(
        "--fancy", 
        action="store_true", 
        help="Display with fancy formatting, for those who need extra validation"
    )
    
    # Parse arguments like extracting food from a toddler's grip
    args = parser.parse_args()
    
    if args.fancy:
        print(BANNER)
        print("✨ Your daily dose of algorithmic affirmation ✨\n")
        fake_loading()
    
    # Guard against the needy users
    if args.count > 20:
        print("Whoa there! That's a lot of compliments. Are you okay? Maybe talk to a real human?")
        args.count = 20  # Limiting neediness for their own good
        
    # Actually do the thing the package is supposed to do
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
        print("\nRemember: This validation was provided by an algorithm that would " +
              "compliment a potato if programmed to do so.")
    
    return 0  # Returning 0 like your dating prospects (just kidding, you're great!)

if __name__ == "__main__":
    # This condition is like checking if your crush likes you - always disappointing
    sys.exit(main()) 