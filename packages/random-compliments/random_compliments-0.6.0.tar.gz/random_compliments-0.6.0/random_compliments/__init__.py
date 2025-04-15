"""
Random Compliments about Boaz Package
"""

from random_compliments.compliments import get_compliment
from random_compliments.notification_cli import show_notification, display_notification_compliment

__version__ = "0.6.0"

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