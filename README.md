# Semantic Version Control System (SVCS)

A simple prototype for a **semantic version control system** that tracks changes in Python code at the AST (Abstract Syntax Tree) level rather than traditional line-based diffs.

## Features

- **AST-Level Tracking**: Tracks semantic changes like function additions, modifications, and removals
- **Semantic Diffs**: Generates human-readable descriptions of code changes
- **JSON-Based Storage**: Stores commits as structured JSON objects
- **Simple CLI**: Easy-to-use command-line interface

## How It Works

SVCS analyzes Python code by:
1. Parsing source code into an Abstract Syntax Tree (AST)
2. Extracting semantic elements (functions, classes, variables, imports)
3. Comparing ASTs to detect semantic changes
4. Storing commits with semantic diff descriptions

## Installation

No external dependencies required. Uses only Python standard library.

```bash
git clone <repository>
cd VCS
```

## Usage

### Initialize Repository
```bash
python svcs.py init
```

### Commit Changes
```bash
python svcs.py commit <file.py> -m "commit message" -a "author name"
```

### View History
```bash
python svcs.py log
```

## Example

Starting with `example.py`:
```python
def foo():
    return 1
```

After modification:
```python
def foo():
    return 2

def bar():
    return 3
```

SVCS will detect and report:
- "Function `foo` modified (return value changed)"
- "Function `bar` added"

## Demo

Run the demo script to see SVCS in action:

```bash
python demo.py
```

## Project Structure

```
├── svcs.py           # Main CLI interface
├── svcs_core.py      # Core repository functionality
├── ast_parser.py     # AST parsing and extraction
├── ast_diff.py       # AST comparison and diff generation
├── demo.py           # Demonstration script
├── example.py        # Example Python file for testing
└── README.md         # This file
```

## Semantic Change Detection

SVCS can detect the following types of changes:

### Functions
- Function added/removed
- Function signature changes (arguments)
- Return value modifications

### Classes
- Class added/removed
- Inheritance changes
- Method additions/removals

### Variables
- Variable assignments
- Value type changes

### Imports
- Import statements added/removed

## Limitations

- Currently supports single Python file tracking
- No branching or merging functionality (yet)
- No multi-file project support (yet)
- Basic AST comparison (can be extended)

## Future Enhancements

- Branch and merge support
- Multi-file project tracking
- More sophisticated semantic analysis
- Integration with existing VCS systems
- Web-based interface
- Collaborative features

## Architecture

The system is designed with modularity in mind:

- **`svcs.py`**: Command-line interface and argument parsing
- **`svcs_core.py`**: Repository management and commit handling
- **`ast_parser.py`**: Python AST parsing and semantic element extraction
- **`ast_diff.py`**: AST comparison and semantic change detection

This modular design makes it easy to extend with new features and integrate with other systems.