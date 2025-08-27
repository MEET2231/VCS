#!/usr/bin/env python3
"""
Semantic Version Control System (SVCS)
A simple VCS that tracks AST-level semantic changes in Python code.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from svcs_core import SVCSRepository


def main():
    parser = argparse.ArgumentParser(description="Semantic Version Control System")
    parser.add_argument('--repo', '-r', help='Repository path (default: current directory)')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # svcs init
    init_parser = subparsers.add_parser('init', help='Initialize a new SVCS repository')
    init_parser.add_argument('path', nargs='?', default='.', help='Directory to initialize repository in')
    
    # svcs commit
    commit_parser = subparsers.add_parser('commit', help='Commit changes to a Python file')
    commit_parser.add_argument('file', help='Python file to commit (can be absolute or relative path)')
    commit_parser.add_argument('-m', '--message', default='', help='Commit message')
    commit_parser.add_argument('-a', '--author', default='user', help='Author name')
    
    # svcs log
    log_parser = subparsers.add_parser('log', help='Show commit history')
    log_parser.add_argument('-n', '--limit', type=int, help='Limit number of commits shown')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Determine repository path
    if args.repo:
        repo_path = Path(args.repo)
    elif args.command == 'init':
        repo_path = Path(args.path)
    else:
        # Look for .svcs in current directory or parent directories
        repo_path = find_repository()
        if not repo_path:
            print("Error: Not in an SVCS repository. Run 'svcs init' first or specify --repo path.")
            sys.exit(1)
    
    try:
        if args.command == 'init':
            repo = SVCSRepository(repo_path / '.svcs')
            repo.init()
            print(f"Initialized empty SVCS repository in {repo_path / '.svcs'}")
        
        elif args.command == 'commit':
            repo = SVCSRepository(repo_path / '.svcs')
            if not (repo_path / '.svcs').exists():
                print(f"Error: No SVCS repository found at {repo_path}. Run 'svcs init' first.")
                sys.exit(1)
            
            # Convert file path to absolute path
            file_path = Path(args.file)
            if not file_path.is_absolute():
                file_path = Path.cwd() / file_path
            
            commit_id = repo.commit(str(file_path), args.author, args.message)
            print(f"Committed {file_path} as {commit_id}")
        
        elif args.command == 'log':
            repo = SVCSRepository(repo_path / '.svcs')
            if not (repo_path / '.svcs').exists():
                print(f"Error: No SVCS repository found at {repo_path}. Run 'svcs init' first.")
                sys.exit(1)
            
            repo.log(args.limit)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def find_repository(start_path: Path = None) -> Optional[Path]:
    """Find the nearest SVCS repository by walking up the directory tree."""
    if start_path is None:
        start_path = Path.cwd()
    
    current = start_path.resolve()
    
    # Walk up the directory tree
    while current != current.parent:
        if (current / '.svcs').exists():
            return current
        current = current.parent
    
    # Check root directory
    if (current / '.svcs').exists():
        return current
    
    return None


if __name__ == '__main__':
    main()
