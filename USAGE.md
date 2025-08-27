# SVCS Usage Guide

## Quick Start

1. **Initialize a repository**:
   ```bash
   python svcs.py init                    # Initialize in current directory
   python svcs.py init /path/to/project   # Initialize in specific directory
   ```

2. **Commit a Python file**:
   ```bash
   python svcs.py commit myfile.py -m "Your commit message" -a "Your Name"
   python svcs.py --repo /path/to/repo commit /path/to/file.py -m "Message" -a "Author"
   ```

3. **View commit history**:
   ```bash
   python svcs.py log
   python svcs.py --repo /path/to/repo log
   ```

## Working with Different Directories

SVCS now supports working with files and repositories in different directories:

### Repository Location Options

1. **Auto-discovery**: SVCS will search for `.svcs` directory starting from current directory and walking up the tree
2. **Explicit repository**: Use `--repo` flag to specify repository location
3. **Initialize anywhere**: Initialize repositories in any directory

### Examples

```bash
# Initialize repository in a project directory
python svcs.py init /home/user/my_project

# Commit files from anywhere using --repo flag
python svcs.py --repo /home/user/my_project commit /home/user/my_project/src/main.py -m "Add main" -a "dev"

# Work from within project (auto-discovery)
cd /home/user/my_project
python /path/to/svcs.py commit src/main.py -m "Update main" -a "dev"
python /path/to/svcs.py log

# Commit files outside project directory
python svcs.py --repo /home/user/my_project commit /tmp/script.py -m "Add script" -a "dev"
```

## Detailed Commands

### `svcs init [path]`
Creates a new SVCS repository.

**Arguments:**
- `path`: Directory to initialize repository in (default: current directory)

**Examples:**
```bash
python svcs.py init                    # Initialize in current directory
python svcs.py init my_project         # Initialize in ./my_project/
python svcs.py init /abs/path/project  # Initialize in absolute path
```

### `svcs commit <file.py>`
Commits changes to a Python file.

**Global Options:**
- `--repo, -r`: Repository path (auto-discovered if not specified)

**Options:**
- `-m, --message`: Commit message (optional)
- `-a, --author`: Author name (default: "user")

**Examples:**
```bash
# From within repository
python svcs.py commit app.py -m "Added new function" -a "John Doe"

# Specify repository explicitly
python svcs.py --repo /project commit /project/src/app.py -m "Update" -a "Jane"

# Commit file outside repository
python svcs.py --repo /project commit /external/script.py -m "External script" -a "Dev"
```

### `svcs log`
Shows commit history with semantic changes.

**Global Options:**
- `--repo, -r`: Repository path (auto-discovered if not specified)

**Options:**
- `-n, --limit`: Limit number of commits shown

**Examples:**
```bash
python svcs.py log                    # Show all commits (auto-discover repo)
python svcs.py --repo /project log    # Show commits from specific repo
python svcs.py log -n 5               # Show last 5 commits
```

## Understanding Semantic Changes

SVCS tracks these types of changes:

### Function Changes
- **Added**: "Function `new_func` added"
- **Removed**: "Function `old_func` removed"
- **Modified signature**: "Function `func` signature modified (arguments added/removed/changed)"
- **Modified return**: "Function `func` modified (return value changed)"

### Class Changes
- **Added**: "Class `NewClass` added"
- **Removed**: "Class `OldClass` removed"
- **Inheritance**: "Class `MyClass` inheritance modified"
- **Methods**: "Method `new_method` added to class `MyClass`"

### Variable Changes
- **New assignment**: "Variable `x` assigned (Constant)"
- **Value change**: "Variable `x` assigned new value (Name)"

### Import Changes
- **Added**: "Import added: import os"
- **Removed**: "Import removed: from sys import argv"

## Repository Structure

```
.svcs/
├── commits/           # Individual commit files
│   ├── abc123.json   # Commit data with AST and diff
│   └── def456.json
├── refs/             # References (branches, HEAD)
│   ├── HEAD          # Current branch pointer
│   └── heads/
│       └── main      # Main branch pointer
└── config.json       # Repository configuration
```

## Tips

1. **Meaningful commits**: Use descriptive commit messages to track your changes
2. **Regular commits**: Commit frequently to track incremental changes
3. **Single file focus**: Currently works best with single Python files
4. **Check syntax**: Ensure your Python file is syntactically correct before committing

## Troubleshooting

### "Not in an SVCS repository"
Run `python svcs.py init` first to initialize the repository.

### "Syntax error in file.py"
Fix the Python syntax errors in your file before committing.

### "File does not exist"
Ensure the Python file exists and the path is correct.

### "Only Python files (.py) are supported"
SVCS currently only supports `.py` files.

## Examples

### Example 1: Function modification
```python
# Before
def calculate(x):
    return x * 2

# After  
def calculate(x, y):
    return x * y

# SVCS will detect:
# - Function `calculate` signature modified (arguments added)
# - Function `calculate` modified (return value changed)
```

### Example 2: Class addition
```python
# Before
def helper():
    pass

# After
def helper():
    pass

class DataProcessor:
    def process(self, data):
        return data

# SVCS will detect:
# - Class `DataProcessor` added
# - Method `process` added to class `DataProcessor`
```
