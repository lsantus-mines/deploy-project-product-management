"""Copy a committed source snapshot into deployment main without rewriting history.

GitHub workflows are destination-owned and excluded. Credentials stay in Git's
credential helper or checkout configuration; this program never reads tokens.
"""
import argparse
import io
import os
from pathlib import Path, PurePosixPath
import subprocess
import tarfile
import tempfile

DEPLOY_REPOSITORY = 'https://github.com/lsantus-mines/deploy-project-product-management.git'


def git(directory, *args, capture=True):
    result = subprocess.run(
        ['git', '-C', str(directory), *args], check=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return result.stdout if capture else b''


def excluded(name):
    parts = PurePosixPath(name).parts
    return '.git' in parts or parts[:2] == ('.github', 'workflows')


def normalized(repository):
    return repository.rstrip('/').removesuffix('.git').replace('git@github.com:', 'https://github.com/')


def snapshot(source, ref):
    revision = git(source, 'rev-parse', '--verify', f'{ref}^{{commit}}').decode().strip()
    archive = git(source, 'archive', '--format=tar', revision)
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        for member in stream.getmembers():
            name = member.name
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts:
                raise RuntimeError('Unsafe source path in Git archive')
            if excluded(name) or member.isdir():
                continue
            if not member.isfile():
                raise RuntimeError(f'Symlinks/submodules are unsupported: {name}')
            files[name] = (stream.extractfile(member).read(), member.mode & 0o777)
    return revision, files


def synchronize(source, target, ref='HEAD', repository=DEPLOY_REPOSITORY, dry_run=False):
    source, target = Path(source).resolve(), Path(target).resolve()
    if source == target or source in target.parents or target in source.parents:
        raise RuntimeError('Source and destination must be separate checkouts')
    origin = git(target, 'remote', 'get-url', 'origin').decode().strip()
    if normalized(origin) != normalized(repository):
        raise RuntimeError('Destination origin does not match the deployment repository')
    if git(target, 'status', '--porcelain', '--untracked-files=all').strip():
        raise RuntimeError('Destination has local changes; refusing to overwrite them')
    branch = git(target, 'branch', '--show-current').decode().strip()
    # actions/checkout may use a detached checkout of main.
    if branch and branch != 'main':
        raise RuntimeError('Destination must be on main or its detached checkout')
    revision, files = snapshot(source, ref)
    tracked = {
        name for name in git(target, 'ls-files', '-z').decode().split('\0')
        if name and not excluded(name)
    }
    changed = [name for name, (data, mode) in files.items()
               if not (target / name).is_file() or (target / name).is_symlink()
               or (target / name).read_bytes() != data
               or bool((target / name).stat().st_mode & 0o111) != bool(mode & 0o111)]
    removed = sorted(tracked - files.keys())
    print(f'Source {revision[:12]}: {len(changed)} changed, {len(removed)} removed; workflows preserved.', flush=True)
    if dry_run or not (changed or removed):
        return False
    # Fail rather than traverse a symlink in the destination.
    for name in set(changed + removed):
        path = target / name
        for ancestor in (path, *path.parents):
            if ancestor == target:
                break
            if ancestor.is_symlink():
                raise RuntimeError(f'Destination contains a symlink: {name}')
    # Delete only tracked snapshot files, inside this dedicated clean checkout.
    for name in removed:
        (target / name).unlink()
    for name in changed:
        path = target / name
        # A removed tracked directory may become a file, or vice versa.
        if path.is_dir():
            for child in sorted(path.rglob('*'), reverse=True):
                if child.is_dir():
                    child.rmdir()
                else:
                    raise RuntimeError(f'Unexpected remaining destination file: {child}')
            path.rmdir()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(files[name][0])
        os.chmod(path, files[name][1])
    git(target, 'add', '-A')
    git(target, '-c', 'user.name=FlowAssist deployment sync',
        '-c', 'user.email=41898282+github-actions[bot]@users.noreply.github.com',
        'commit', '-m', f'Sync primary main at {revision[:12]}', capture=False)
    # No force: concurrent destination changes are rejected, never overwritten.
    git(target, 'push', 'origin', 'HEAD:main', capture=False)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument('--ref', default='HEAD', help='Committed source ref; uncommitted edits are excluded')
    parser.add_argument('--checkout', help='Existing clean deployment checkout (e.g. GitHub Actions)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.checkout:
        synchronize(args.source, args.checkout, args.ref, dry_run=args.dry_run)
    else:
        with tempfile.TemporaryDirectory(prefix='flowassist-deploy-') as temp:
            subprocess.run(['git', 'clone', '--depth', '1', '--branch', 'main', DEPLOY_REPOSITORY, temp], check=True)
            synchronize(args.source, temp, args.ref, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
