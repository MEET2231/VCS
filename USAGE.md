# SVCS Usage Guide

## Quick Start

1. **Initialize a repository**:
   ```bash
   python svcs.py init
   ```

2. **Commit a Python file**:
   ```bash
   python svcs.py commit myfile.py -m "Your commit message" -a "Your Name"
   ```

3. **View commit history**:
   ```bash
   python svcs.py log
   ```

## Detailed Commands

### `svcs init`
Creates a new SVCS repository in the current directory.
- Creates `.svcs/` folder with repository structure
- Initializes configuration and references

### `svcs commit <file.py>`
Commits changes to a Python file.

**Options:**
- `-m, --message`: Commit message (optional)
- `-a, --author`: Author name (default: "user")

**Examples:**
```bash
python svcs.py commit app.py -m "Added new function" -a "John Doe"
python svcs.py commit script.py  # Minimal commit
```

### `svcs log`
Shows commit history with semantic changes.

**Options:**
- `-n, --limit`: Limit number of commits shown

**Examples:**
```bash
python svcs.py log           # Show all commits
python svcs.py log -n 5      # Show last 5 commits
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
