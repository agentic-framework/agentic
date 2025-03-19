# Lessons Learned: Git Operations

This document records important lessons learned during the development and maintenance of the Agentic framework, particularly focusing on git operations and common pitfalls.

## Using `git mv` vs. Regular `mv`

### The Issue

During the reorganization of the Agentic framework to separate documentation and scripts into dedicated folders, we initially used the regular `mv` command to move files instead of `git mv`. This led to git seeing the original files as deleted and the new files in the new directories as untracked, rather than recognizing them as moved files.

```bash
# What we initially did (incorrect):
mv README.md docs/
mv check_environment.py scripts/

# Git status showed:
# deleted: README.md
# deleted: check_environment.py
# Untracked files:
#   docs/README.md
#   scripts/check_environment.py
```

This approach loses the file history in git, as git doesn't know that the files were moved rather than deleted and recreated.

### The Solution

The correct approach is to use `git mv` to move files within a git repository:

```bash
# Correct approach:
git mv README.md docs/
git mv check_environment.py scripts/

# Git status showed:
# renamed: README.md -> docs/README.md
# renamed: check_environment.py -> scripts/check_environment.py
```

Using `git mv` ensures that git tracks the file movement and preserves the file history.

### Update: Moving README.md Back to Root

Later in the project, we decided to move the README.md file back to the root directory for better visibility on GitHub and other platforms. Again, we used `git mv` to preserve the file history:

```bash
# Moving README.md back to root
git mv docs/README.md ./

# Git status showed:
# renamed: docs/README.md -> README.md
```

This change required updating references to docs/README.md in various documentation files to point to the root README.md file instead.

### Recovery Strategy

If you've already used regular `mv` instead of `git mv`, you can recover by:

1. Making a backup of the moved files (to preserve any changes)
2. Using `git restore .` to restore the original files
3. Using `git mv` to properly move the files
4. Copying the content from the backup to the newly moved files

```bash
# 1. Backup moved files
cp -r docs docs_backup
cp -r scripts scripts_backup

# 2. Restore original files
git restore .

# 3. Properly move files with git mv
git mv README.md docs/
git mv check_environment.py scripts/

# 4. Copy content from backup to newly moved files
cp -f docs_backup/* docs/
cp -f scripts_backup/* scripts/

# 5. Clean up backup directories
rm -rf docs_backup scripts_backup
```

## Other Git Best Practices

### Commit Frequently

Make small, focused commits that address a single issue or feature. This makes it easier to:
- Understand the history of changes
- Revert specific changes if needed
- Review code

### Write Clear Commit Messages

Follow the conventional commits format:
```
type(scope): description
```

Where:
- `type` is one of: feat, fix, docs, style, refactor, test, chore
- `scope` is optional and indicates the part of the codebase affected
- `description` is a clear, concise description of the change

### Use Branches

Create feature branches for new development and merge them back to the main branch when complete. This keeps the main branch stable and makes it easier to work on multiple features simultaneously.

### Review Changes Before Committing

Always review your changes before committing:
```bash
git diff
git status
```

This helps catch unintended changes and ensures you're only committing what you intend to.

## Conclusion

Understanding how git tracks files and using the appropriate git commands is crucial for maintaining a clean and accurate version history. The `git mv` command is specifically designed for moving files within a git repository, and using it instead of regular `mv` ensures that git correctly tracks file movements.
