"""
Random Compliments about Boaz Package
"""

from random_compliments.compliments import get_compliment

__version__ = "0.5.7"

def get_version():
    """Return the package version"""
    return __version__

def get_random_compliment():
    """
    Get a random compliment about Boaz.
    
    Returns:
        str: A random compliment about Boaz.
    """
    return get_compliment() 