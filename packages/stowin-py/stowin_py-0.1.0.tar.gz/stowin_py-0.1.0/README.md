# Stowin

A GNU Stow alternative written in Python

## Installation

```bash
pip install stowin-py
```

## Usage

```bash
stowin SOURCE [--target TARGET] [OPTIONS]
```

### Options:
- `-t, --target`: Target directory (defaults to source parent)
- `--dry-run`: Do not actually create symlinks
- `--adopt`: Adopt existing files
- `--force`: Override existing files
- `--backup/--no-backup`: Backup existing files
- `--relative`: Create relative symlinks
- `--ignore`: Ignore regex patterns
- `-v, --verbose`: Increase verbosity

## Example

```bash
stowin ~/.dotfiles -t ~
```
