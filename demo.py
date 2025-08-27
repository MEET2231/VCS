#!/usr/bin/env python3
"""
Test script to demonstrate SVCS functionality.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd_args):
    """Run a command and print the output."""
    if isinstance(cmd_args, str):
        cmd_args = cmd_args.split()
    
    cmd_str = " ".join(cmd_args)
    print(f"$ {cmd_str}")
    
    result = subprocess.run(cmd_args, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    print()
    return result.returncode == 0


def demo():
    """Demonstrate SVCS functionality."""
    print("=== Semantic Version Control System Demo ===\n")
    
    # Clean up any existing .svcs directory
    if Path(".svcs").exists():
        import shutil
        shutil.rmtree(".svcs")
    
    # Initialize repository
    print("1. Initialize SVCS repository:")
    run_command(["python", "svcs.py", "init"])
    
    # Make initial commit
    print("2. Initial commit of example.py:")
    run_command(["python", "svcs.py", "commit", "example.py", "-m", "Initial commit", "-a", "developer"])
    
    # Modify the file
    print("3. Modifying example.py:")
    with open("example.py", "w") as f:
        f.write("""def foo():
    return 2

def bar():
    return 3
""")
    print("Modified example.py to change return value and add bar() function\n")
    
    # Commit changes
    print("4. Commit changes:")
    run_command(["python", "svcs.py", "commit", "example.py", "-m", "Modified foo and added bar", "-a", "developer"])
    
    # Show log
    print("5. Show commit history:")
    run_command(["python", "svcs.py", "log"])
    
    # Modify again
    print("6. Modifying example.py again:")
    with open("example.py", "w") as f:
        f.write("""def foo(x, y):
    return x + y

def bar():
    return 3

class Calculator:
    def add(self, a, b):
        return a + b
""")
    print("Modified example.py to change foo signature and add Calculator class\n")
    
    # Final commit
    print("7. Final commit:")
    run_command(["python", "svcs.py", "commit", "example.py", "-m", "Modified foo signature and added Calculator class", "-a", "developer"])
    
    # Show final log
    print("8. Final commit history:")
    run_command(["python", "svcs.py", "log"])


if __name__ == "__main__":
    demo()
