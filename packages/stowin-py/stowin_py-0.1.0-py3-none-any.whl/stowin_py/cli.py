import os
from pathlib import Path
import click
import re
from typing import List, Pattern
from tqdm import tqdm

def compile_patterns(patterns: tuple[str]) -> List[Pattern]:
    """Compile regex patterns, adding ^ and $ if not present"""
    compiled = []
    for pattern in patterns:
        if not pattern.startswith('^'):
            pattern = '^' + pattern
        if not pattern.endswith('$'):
            pattern = pattern + '$'
        try:
            compiled.append(re.compile(pattern))
        except re.error as e:
            raise click.BadParameter(f"Invalid regex pattern '{pattern}': {e}")
    return compiled

@click.command()
@click.argument('source',
              type=click.Path(exists=True, file_okay=False, dir_okay=True),
              metavar='<source>')
@click.argument('target',
              type=click.Path(exists=True, file_okay=False, dir_okay=True),
                default=None,
                required=False)
@click.option('--dry-run', is_flag=True, help='Do not actually create symlinks')
@click.option('--adopt', is_flag=True, help='Adopt existing files')
@click.option('--force', is_flag=True, help='Override existing files')
@click.option('--backup/--no-backup', default=True, help='Backup existing files')
@click.option('--relative', is_flag=True, help='Create relative symlinks')
@click.option('--ignore', multiple=True, metavar='<pattern>', help=r'Ignore regex patterns (e.g. ".*\.pyc")')
@click.option('-v', '--verbose', count=True, help='Increase verbosity')
def cli(source: str, target: str, force: bool, dry_run: bool, adopt: bool,
         backup: bool, relative: bool, ignore: tuple[str], verbose: int):

    def log(msg: str, level: int = 1):
        if verbose >= level:
            click.echo(msg)

    source_path = Path(source).resolve()

    # Set target_path to source parent if target is None
    target_path = Path(target).resolve() if target else source_path.parent

    if not source_path.is_dir():
        raise click.BadParameter(f"Source {source} must be a directory")
    if not target_path.is_dir():
        raise click.BadParameter(f"Target {target} must be a directory")

    # Compile regex patterns
    ignore_patterns = compile_patterns(ignore)

    def should_ignore(file_path: Path) -> bool:
        """Check if file matches any ignore pattern"""
        return any(pattern.search(str(file_path)) for pattern in ignore_patterns)

    try:
        files_to_process = [f for f in source_path.rglob('*')
                          if f.is_file() and not should_ignore(f)]

        with tqdm(files_to_process, disable=not verbose) as pbar:
            for source_file in pbar:
                pbar.set_description(f"Processing {source_file.name}")

                rel_path = source_file.relative_to(source_path)
                target_file = target_path / rel_path

                if target_file.exists() or target_file.is_symlink():
                    if adopt:
                        source_file.parent.mkdir(parents=True, exist_ok=True)
                        target_file.rename(source_file)
                        log(f"Adopted {target_file} -> {source_file}", 2)
                    elif not force:
                        log(f"Skipping {target_file}: already exists", 1)
                        continue
                    else:
                        if backup and target_file.exists():
                            backup_file = target_file.with_suffix(target_file.suffix + '.bak')
                            target_file.rename(backup_file)
                            log(f"Backed up {target_file} -> {backup_file}", 2)
                        target_file.unlink(missing_ok=True)

                if dry_run:
                    log(f"Would link {source_file} -> {target_file}", 1)
                    continue

                target_file.parent.mkdir(parents=True, exist_ok=True)

                try:
                    if relative:
                        source_file = os.path.relpath(source_file, target_file.parent)
                    target_file.symlink_to(source_file)
                    log(f"Linked {source_file} -> {target_file}", 1)
                except OSError as e:
                    click.echo(f"Failed to create symlink {target_file}: {e}", err=True)

        click.echo(f'Successfully stowed {source} to {target_path}')

    except PermissionError as e:
        click.echo(f"Permission denied: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error during stowing: {e}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    cli()
