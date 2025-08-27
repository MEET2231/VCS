# SVCS Multi-Directory Support

## New Features

### 1. Repository Auto-Discovery
SVCS now searches for `.svcs` directories starting from the current directory and walking up the directory tree, similar to Git.

### 2. Explicit Repository Specification
Use the `--repo` or `-r` flag to specify which repository to use:
```bash
python svcs.py --repo /path/to/project commit file.py -m "message"
```

### 3. Initialize Anywhere
Initialize repositories in any directory:
```bash
python svcs.py init /path/to/new/project
```

### 4. Absolute and Relative Path Support
- Files can be anywhere on the filesystem
- Stores both relative (from repo root) and absolute paths
- Works with files outside the repository directory

## Usage Patterns

### Pattern 1: Centralized Repository
```bash
# Create a central repository
python svcs.py init /repos/my_project

# Commit files from various locations
python svcs.py --repo /repos/my_project commit /src/app.py -m "Update app"
python svcs.py --repo /repos/my_project commit /tests/test.py -m "Add tests"
python svcs.py --repo /repos/my_project commit /scripts/deploy.py -m "Add deploy script"
```

### Pattern 2: Project-Based Repository
```bash
# Initialize in project root
cd /projects/my_app
python /tools/svcs.py init

# Work from anywhere within project
cd src/
python /tools/svcs.py commit main.py -m "Update main"

cd ../tests/
python /tools/svcs.py commit test_main.py -m "Add tests"

# View history
python /tools/svcs.py log
```

### Pattern 3: Development Workflow
```bash
# Setup
mkdir project && cd project
python svcs.py init
mkdir src tests docs

# Create files
echo "def main(): pass" > src/app.py
echo "import unittest" > tests/test_app.py
echo "# Documentation" > docs/readme.py

# Commit from project root
python svcs.py commit src/app.py -m "Initial app" -a "dev"
python svcs.py commit tests/test_app.py -m "Initial tests" -a "dev"
python svcs.py commit docs/readme.py -m "Initial docs" -a "dev"

# View project history
python svcs.py log
```

## File Path Handling

### Relative Paths (Preferred)
When files are within the repository directory, SVCS stores relative paths for better portability:
```
Repository: /home/user/project/.svcs
File: /home/user/project/src/main.py
Stored as: src/main.py
```

### Absolute Paths
When files are outside the repository directory, SVCS stores absolute paths:
```
Repository: /home/user/project/.svcs
File: /tmp/external_script.py
Stored as: /tmp/external_script.py
```

## Best Practices

1. **Initialize at project root**: `python svcs.py init` in your main project directory
2. **Use relative paths**: Keep files within the project when possible
3. **Consistent author names**: Use the same author name for related commits
4. **Descriptive messages**: Write clear commit messages describing semantic changes
5. **Regular commits**: Commit frequently to track incremental changes

## Migration from Single-Directory

If you have an existing SVCS repository that only worked in one directory:

1. **Move repository**: The `.svcs` directory can be moved anywhere
2. **Update paths**: File paths in commits will be automatically handled
3. **Use new features**: Start using `--repo` flag or repository auto-discovery

## Troubleshooting

### "No SVCS repository found"
- Ensure `.svcs` directory exists
- Use `--repo` flag to specify repository location
- Check that you're in or below a directory with a `.svcs` folder

### "File not found"
- Verify file paths are correct
- Use absolute paths if files are outside current directory
- Check file permissions and existence

### Repository Discovery Issues
- SVCS searches up the directory tree from current location
- Ensure there's a `.svcs` directory somewhere in the parent path
- Use `--repo` flag if auto-discovery doesn't work
