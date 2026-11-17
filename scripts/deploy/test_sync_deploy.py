"""Local-only integration tests for the cross-repository synchronization."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import subprocess
import tempfile
import unittest

from sync_deploy import synchronize


def run(*args):
    return subprocess.check_output(args, stderr=subprocess.PIPE).decode().strip()


def commit(repo, message):
    run('git', '-C', str(repo), 'add', '-A')
    run('git', '-C', str(repo), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', message)
    return run('git', '-C', str(repo), 'rev-parse', 'HEAD')


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='flowassist-sync-test-')
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.source, self.target, self.remote = root/'source', root/'target', root/'deploy.git'
        for repo in (self.source, self.target):
            repo.mkdir()
            run('git', 'init', '-b', 'main', str(repo))
        run('git', 'init', '--bare', str(self.remote))
        (self.source/'app.js').write_text('new application\n')
        (self.source/'.github/workflows').mkdir(parents=True)
        (self.source/'.github/workflows/source.yml').write_text('source workflow\n')
        self.source_revision = commit(self.source, 'source snapshot')
        (self.target/'old.txt').write_text('obsolete\n')
        (self.target/'.github/workflows').mkdir(parents=True)
        (self.target/'.github/workflows/owned.yml').write_text('destination-owned\n')
        self.initial = commit(self.target, 'independent destination history')
        run('git', '-C', str(self.target), 'remote', 'add', 'origin', str(self.remote))
        run('git', '-C', str(self.target), 'push', 'origin', 'main')

    def sync(self, **kwargs):
        with redirect_stdout(io.StringIO()):
            return synchronize(self.source, self.target, repository=str(self.remote), **kwargs)

    def test_sync_preserves_history_workflows_and_is_idempotent(self):
        self.assertTrue(self.sync())
        self.assertEqual((self.target/'app.js').read_text(), 'new application\n')
        self.assertFalse((self.target/'old.txt').exists())
        self.assertEqual((self.target/'.github/workflows/owned.yml').read_text(), 'destination-owned\n')
        self.assertFalse((self.target/'.github/workflows/source.yml').exists())
        run('git', '-C', str(self.target), 'merge-base', '--is-ancestor', self.initial, 'HEAD')
        self.assertEqual(run('git', '-C', str(self.remote), 'rev-parse', 'refs/heads/main'), run('git', '-C', str(self.target), 'rev-parse', 'HEAD'))
        self.assertFalse(self.sync())

    def test_dry_run_never_changes_destination(self):
        self.assertFalse(self.sync(dry_run=True))
        self.assertTrue((self.target/'old.txt').exists())
        self.assertEqual(run('git', '-C', str(self.target), 'rev-parse', 'HEAD'), self.initial)

    def test_dirty_or_wrong_destination_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'origin'):
            synchronize(self.source, self.target, repository='https://github.com/wrong/repo')
        (self.target/'uncommitted.txt').write_text('do not overwrite\n')
        with self.assertRaisesRegex(RuntimeError, 'local changes'):
            self.sync()

    def test_uncommitted_source_edits_are_excluded(self):
        (self.source/'app.js').write_text('uncommitted change\n')
        self.sync()
        self.assertEqual((self.target/'app.js').read_text(), 'new application\n')

    def test_concurrent_remote_commit_is_never_overwritten(self):
        other = Path(self.temp.name)/'other'
        run('git', 'clone', '--branch', 'main', str(self.remote), str(other))
        (other/'remote-change.txt').write_text('preserve this commit\n')
        newer = commit(other, 'concurrent destination commit')
        run('git', '-C', str(other), 'push', 'origin', 'main')
        with self.assertRaises(subprocess.CalledProcessError):
            self.sync()
        self.assertEqual(run('git', '-C', str(self.remote), 'rev-parse', 'refs/heads/main'), newer)


if __name__ == '__main__':
    unittest.main()
