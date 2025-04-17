#!/usr/bin/env python
"""
Version management script for the Teer package.
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# Path to the version file
VERSION_FILE = Path("src/teer/__about__.py")

def get_current_version():
    """Get the current version from the version file."""
    with open(VERSION_FILE, "r") as f:
        content = f.read()
    
    # Extract version using regex
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError(f"Could not find version in {VERSION_FILE}")
    
    return match.group(1)

def set_version(new_version):
    """Set a new version in the version file."""
    with open(VERSION_FILE, "r") as f:
        content = f.read()
    
    # Replace version using regex
    new_content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open(VERSION_FILE, "w") as f:
        f.write(new_content)
    
    print(f"Version updated to {new_version}")

def increment_version(current_version, increment_type):
    """Increment the version according to semver rules."""
    major, minor, patch = map(int, current_version.split('.'))
    
    if increment_type == "patch":
        patch += 1
    elif increment_type == "minor":
        minor += 1
        patch = 0
    elif increment_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"Unknown increment type: {increment_type}")
    
    return f"{major}.{minor}.{patch}"

def main():
    """Main function."""
    if len(sys.argv) != 2 or sys.argv[1] not in ["patch", "minor", "major"]:
        print("Usage: python version.py [patch|minor|major]")
        sys.exit(1)
    
    increment_type = sys.argv[1]
    current_version = get_current_version()
    new_version = increment_version(current_version, increment_type)
    set_version(new_version)
    
    return new_version

if __name__ == "__main__":
    main()
