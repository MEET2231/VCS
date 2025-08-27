#!/usr/bin/env python3
"""
Advanced demo script showing SVCS usage with different directories.
"""

import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path


def run_command(cmd_args, cwd=None):
    """Run a command and print the output."""
    if isinstance(cmd_args, str):
        cmd_args = cmd_args.split()
    
    cmd_str = " ".join(cmd_args)
    print(f"$ {cmd_str}")
    
    result = subprocess.run(cmd_args, capture_output=True, text=True, cwd=cwd)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    print()
    return result.returncode == 0


def demo_different_directories():
    """Demonstrate SVCS usage with different directories."""
    print("=== SVCS Multi-Directory Demo ===\n")
    
    # Get current directory (where svcs.py is located)
    svcs_dir = Path.cwd()
    svcs_py = svcs_dir / "svcs.py"
    
    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a project directory
        project_dir = temp_path / "my_project"
        project_dir.mkdir()
        
        # Create subdirectories
        src_dir = project_dir / "src"
        src_dir.mkdir()
        tests_dir = project_dir / "tests"
        tests_dir.mkdir()
        
        print(f"Created project structure in: {project_dir}")
        print(f"  - {src_dir}")
        print(f"  - {tests_dir}\n")
        
        # 1. Initialize repository in project directory
        print("1. Initialize SVCS repository in project directory:")
        run_command([sys.executable, str(svcs_py), "init", str(project_dir)])
        
        # 2. Create Python files in different subdirectories
        print("2. Creating Python files in different directories:")
        
        # Create main.py in src/
        main_py = src_dir / "main.py"
        with open(main_py, "w") as f:
            f.write("""def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""")
        print(f"Created {main_py}")
        
        # Create utils.py in src/
        utils_py = src_dir / "utils.py"
        with open(utils_py, "w") as f:
            f.write("""def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
""")
        print(f"Created {utils_py}")
        
        # Create test_utils.py in tests/
        test_py = tests_dir / "test_utils.py"
        with open(test_py, "w") as f:
            f.write("""import unittest

class TestUtils(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
""")
        print(f"Created {test_py}\n")
        
        # 3. Commit files using different approaches
        print("3. Committing files from different directories:\n")
        
        # Commit from project root using relative paths
        print("a) Commit from project root using relative paths:")
        run_command([
            sys.executable, str(svcs_py), "--repo", str(project_dir),
            "commit", str(main_py), "-m", "Add main application", "-a", "developer"
        ])
        
        run_command([
            sys.executable, str(svcs_py), "--repo", str(project_dir),
            "commit", str(utils_py), "-m", "Add utility functions", "-a", "developer"
        ])
        
        run_command([
            sys.executable, str(svcs_py), "--repo", str(project_dir),
            "commit", str(test_py), "-m", "Add unit tests", "-a", "developer"
        ])
        
        # 4. Show commit history
        print("4. Show commit history:")
        run_command([
            sys.executable, str(svcs_py), "--repo", str(project_dir), "log"
        ])
        
        # 5. Modify files and commit again
        print("5. Modifying files and committing changes:\n")
        
        # Modify utils.py
        with open(utils_py, "w") as f:
            f.write("""def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class Calculator:
    def calculate(self, operation, a, b):
        if operation == "add":
            return add(a, b)
        elif operation == "multiply":
            return multiply(a, b)
        elif operation == "divide":
            return divide(a, b)
""")
        
        print("Modified utils.py to add divide function and Calculator class")
        
        # Commit the changes
        run_command([
            sys.executable, str(svcs_py), "--repo", str(project_dir),
            "commit", str(utils_py), "-m", "Add divide function and Calculator class", "-a", "developer"
        ])
        
        # 6. Show final history
        print("6. Final commit history:")
        run_command([
            sys.executable, str(svcs_py), "--repo", str(project_dir), "log", "-n", "2"
        ])
        
        # 7. Show working with repository discovery
        print("7. Working from within project directory (auto-discovery):")
        
        # Change to src directory and commit without specifying repo
        print("Changing to src directory and committing...")
        
        # Modify main.py
        with open(main_py, "w") as f:
            f.write("""def main():
    print("Hello, SVCS World!")

def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    main()
""")
        
        # This should work from src directory due to repository discovery
        print("Note: In a real scenario, you would cd to src/ and run without --repo")
        print("Simulating: cd src && python svcs.py commit main.py ...")
        
        run_command([
            sys.executable, str(svcs_py), "--repo", str(project_dir),
            "commit", str(main_py), "-m", "Add greet function to main", "-a", "developer"
        ])
        
        print("8. Final repository state:")
        run_command([
            sys.executable, str(svcs_py), "--repo", str(project_dir), "log", "-n", "3"
        ])


if __name__ == "__main__":
    demo_different_directories()
