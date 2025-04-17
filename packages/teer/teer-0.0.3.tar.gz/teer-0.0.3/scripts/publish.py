#!/usr/bin/env python
"""
Publish script for the Teer package.

This script:
1. Increments the version (patch, minor, or major)
2. Builds the package
3. Publishes to PyPI
4. Commits the version change to git
5. Creates a git tag for the new version
"""

import os
import sys
import subprocess
from pathlib import Path

# Import the version script
sys.path.append(str(Path(__file__).parent))
from version import main as increment_version

def run_command(command, check=True):
    """Run a shell command and return its output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=check, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result

def main():
    """Main function."""
    if len(sys.argv) != 2 or sys.argv[1] not in ["patch", "minor", "major"]:
        print("Usage: python publish.py [patch|minor|major]")
        sys.exit(1)
    
    increment_type = sys.argv[1]
    
    # Check if the working directory is clean
    result = run_command("git status --porcelain", check=False)
    if result.stdout.strip() and not result.stdout.strip().startswith("?? "):
        print("Error: Working directory is not clean. Please commit or stash your changes.")
        sys.exit(1)
    
    # Increment the version
    print(f"Incrementing {increment_type} version...")
    new_version = increment_version()
    
    # Build the package
    print("Building package...")
    run_command("hatch build")
    
    # Publish to PyPI
    print("Publishing to PyPI...")
    run_command("source .env && HATCH_INDEX_USER=__token__ HATCH_INDEX_AUTH=$PYPI_API_TOKEN hatch publish")
    
    # Commit the version change
    print("Committing version change...")
    run_command(f'git add src/teer/__about__.py')
    run_command(f'git commit -m "Bump version to {new_version}"')
    
    # Create a git tag
    print(f"Creating git tag v{new_version}...")
    run_command(f'git tag -a v{new_version} -m "Version {new_version}"')
    
    print(f"""
Version {new_version} has been:
- Built
- Published to PyPI
- Committed to git
- Tagged as v{new_version}

To push the changes to the remote repository, run:
git push && git push --tags
""")

if __name__ == "__main__":
    main()
