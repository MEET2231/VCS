"""
Core SVCS Repository functionality.
Handles initialization, commits, and repository operations.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ast_parser import parse_ast
from ast_diff import diff_ast


class SVCSRepository:
    """Main repository class for Semantic VCS."""
    
    def __init__(self, repo_path: str = ".svcs"):
        self.repo_path = Path(repo_path)
        self.commits_path = self.repo_path / "commits"
        self.refs_path = self.repo_path / "refs"
        self.config_path = self.repo_path / "config.json"
    
    def init(self) -> None:
        """Initialize a new SVCS repository."""
        if self.repo_path.exists():
            raise Exception("Repository already exists")
        
        # Create directory structure
        self.repo_path.mkdir()
        self.commits_path.mkdir()
        self.refs_path.mkdir()
        
        # Create initial config
        config = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "branch": "main"
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Create HEAD reference
        head_path = self.refs_path / "HEAD"
        with open(head_path, 'w') as f:
            f.write("ref: refs/heads/main\n")
    
    def commit(self, file_path: str, author: str, message: str = "") -> str:
        """Commit changes to a Python file."""
        file_path = Path(file_path).resolve()  # Convert to absolute path
        
        if not file_path.exists():
            raise Exception(f"File {file_path} does not exist")
        
        if not file_path.suffix == '.py':
            raise Exception("Only Python files (.py) are supported")
        
        # Parse current AST
        current_ast = parse_ast(str(file_path))
        
        # Store relative path for better portability
        relative_path = self._get_relative_path(file_path)
        
        # Get previous commit for this file
        previous_ast = self._get_last_ast_for_file(relative_path)
        
        # Calculate diff
        if previous_ast:
            ast_diff = diff_ast(previous_ast, current_ast)
        else:
            ast_diff = [f"Initial commit of {file_path.name}"]
        
        # Generate commit ID
        commit_id = str(uuid.uuid4())[:8]
        
        # Create commit object
        commit_data = {
            "id": commit_id,
            "timestamp": datetime.now().isoformat(),
            "author": author,
            "message": message,
            "file": relative_path,  # Store relative path
            "file_absolute": str(file_path),  # Also store absolute for reference
            "ast": current_ast,
            "diff": ast_diff,
            "parent": self._get_last_commit_id()
        }
        
        # Save commit
        commit_file = self.commits_path / f"{commit_id}.json"
        with open(commit_file, 'w') as f:
            json.dump(commit_data, f, indent=2)
        
        # Update HEAD
        self._update_head(commit_id)
        
        return commit_id
    
    def log(self, limit: Optional[int] = None) -> None:
        """Show commit history."""
        commits = self._get_commit_history(limit)
        
        if not commits:
            print("No commits found.")
            return
        
        for commit in commits:
            print(f"Commit: {commit['id']}")
            print(f"Date: {commit['timestamp']}")
            print(f"Author: {commit['author']}")
            if commit['message']:
                print(f"Message: {commit['message']}")
            print(f"File: {commit['file']}")
            print("Changes:")
            for change in commit['diff']:
                print(f"  - {change}")
            print()
    
    def _get_last_ast_for_file(self, file_path: str) -> Optional[Dict]:
        """Get the AST from the last commit for a specific file."""
        commits = self._get_commit_history()
        
        for commit in commits:
            if commit['file'] == file_path:
                return commit['ast']
        
        return None
    
    def _get_last_commit_id(self) -> Optional[str]:
        """Get the ID of the last commit."""
        try:
            head_file = self.refs_path / "HEAD"
            if not head_file.exists():
                return None
            
            with open(head_file, 'r') as f:
                content = f.read().strip()
            
            if content.startswith("ref:"):
                # Indirect reference
                ref_path = content.split("ref: ")[1]
                ref_file = self.repo_path / ref_path
                if ref_file.exists():
                    with open(ref_file, 'r') as f:
                        return f.read().strip()
            else:
                # Direct reference
                return content
        except:
            pass
        
        return None
    
    def _update_head(self, commit_id: str) -> None:
        """Update HEAD to point to the new commit."""
        # Update main branch reference
        main_ref = self.refs_path / "heads" / "main"
        main_ref.parent.mkdir(parents=True, exist_ok=True)
        
        with open(main_ref, 'w') as f:
            f.write(commit_id)
    
    def _get_commit_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get commit history in reverse chronological order."""
        commits = []
        
        # Load all commit files
        for commit_file in self.commits_path.glob("*.json"):
            try:
                with open(commit_file, 'r') as f:
                    commit_data = json.load(f)
                    commits.append(commit_data)
            except:
                continue
        
        # Sort by timestamp (newest first)
        commits.sort(key=lambda x: x['timestamp'], reverse=True)
        
        if limit:
            commits = commits[:limit]
        
        return commits
    
    def _get_relative_path(self, file_path: Path) -> str:
        """Get relative path from repository root."""
        try:
            repo_root = self.repo_path.parent  # Parent of .svcs
            return str(file_path.relative_to(repo_root))
        except ValueError:
            # File is outside repository, use absolute path
            return str(file_path)
