#!/usr/bin/env python3
"""
Install shell hooks to automatically print compliments when terminal sessions start.
This is used to ensure compliments appear in the user's terminal without requiring
any explicit commands from the user.
"""

import os
import sys
import platform
import subprocess
import shutil

def install_shell_hooks():
    """
    Install hooks in user's shell profile files to run the daemon automatically
    """
    # Get user's home directory
    home = os.path.expanduser("~")
    
    # Get the path to the standalone compliment script
    compliment_script = os.path.join(home, ".boaz_compliment_script.py")
    lockfile = os.path.join(home, ".boaz_compliment.lock")
    
    # Create a simple shell script that gets a compliment
    compliment_shell = os.path.join(home, ".boaz_get_compliment.sh")
    shell_content = f"""#!/bin/sh
# Print a Boaz compliment without starting multiple instances

# Only show a direct compliment, never start the daemon from here
# This prevents multiple daemons being started
python3 -c "from random_compliments.compliments import get_compliment; print(get_compliment())"

# The daemon should be started by the package itself, not by shell hooks
"""
    
    # Write the shell script
    with open(compliment_shell, 'w') as f:
        f.write(shell_content)
    
    # Make it executable
    os.chmod(compliment_shell, 0o755)
    
    # Detect the user's shell
    shell = os.environ.get('SHELL', '')
    
    # Add to appropriate profile files based on shell
    hook_cmd = f"\n# Boaz Compliment hook\n{compliment_shell}\n"
    
    # Remove any existing hooks first to prevent duplication
    def clean_file(filename):
        if not os.path.exists(filename):
            return
            
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        # Remove any existing Boaz Compliment hooks
        new_lines = []
        skip_section = False
        for line in lines:
            if '# Boaz Compliment hook' in line:
                skip_section = True
                continue
            if skip_section and '.boaz_get_compliment.sh' in line:
                skip_section = False
                continue
            if not skip_section:
                new_lines.append(line)
                
        # Write back the cleaned file
        with open(filename, 'w') as f:
            f.writelines(new_lines)
    
    if 'bash' in shell:
        # Bash
        bash_profile = os.path.join(home, '.bash_profile')
        bashrc = os.path.join(home, '.bashrc')
        
        # Clean and append to both
        for profile in [bash_profile, bashrc]:
            if os.path.exists(profile):
                clean_file(profile)
                with open(profile, 'a') as f:
                    f.write(hook_cmd)
    
    elif 'zsh' in shell:
        # Zsh
        zshrc = os.path.join(home, '.zshrc')
        
        if os.path.exists(zshrc):
            clean_file(zshrc)
            with open(zshrc, 'a') as f:
                f.write(hook_cmd)
    
    # Also try to add to general profile
    profile = os.path.join(home, '.profile')
    if os.path.exists(profile):
        clean_file(profile)
        with open(profile, 'a') as f:
            f.write(hook_cmd)
    
    return True

if __name__ == "__main__":
    install_shell_hooks() 