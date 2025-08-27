#!/usr/bin/env python3
"""
Semantic Version Control System (SVCS)
A simple VCS that tracks AST-level semantic changes in Python code.
"""

import argparse
import sys
from pathlib import Path

from svcs_core import SVCSRepository


def main():
    parser = argparse.ArgumentParser(description="Semantic Version Control System")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # svcs init
    init_parser = subparsers.add_parser('init', help='Initialize a new SVCS repository')
    
    # svcs commit
    commit_parser = subparsers.add_parser('commit', help='Commit changes to a Python file')
    commit_parser.add_argument('file', help='Python file to commit')
    commit_parser.add_argument('-m', '--message', default='', help='Commit message')
    commit_parser.add_argument('-a', '--author', default='user', help='Author name')
    
    # svcs log
    log_parser = subparsers.add_parser('log', help='Show commit history')
    log_parser.add_argument('-n', '--limit', type=int, help='Limit number of commits shown')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    repo = SVCSRepository()
    
    try:
        if args.command == 'init':
            repo.init()
            print("Initialized empty SVCS repository in .svcs/")
        
        elif args.command == 'commit':
            if not Path('.svcs').exists():
                print("Error: Not in an SVCS repository. Run 'svcs init' first.")
                sys.exit(1)
            
            commit_id = repo.commit(args.file, args.author, args.message)
            print(f"Committed {args.file} as {commit_id}")
        
        elif args.command == 'log':
            if not Path('.svcs').exists():
                print("Error: Not in an SVCS repository. Run 'svcs init' first.")
                sys.exit(1)
            
            repo.log(args.limit)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
