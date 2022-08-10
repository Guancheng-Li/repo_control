"""
Authors: guanchenglichina@qq.com (Guancheng Li)
Define commands.
"""
from typing import List

from utils.process_utils import run_child_process

import settings

def _normalize_branch_name(branch_name: str, prefix: str) -> str:
    """Add prefix if needed."""
    # TODO(Guancheng): add ut after add Bazel
    if branch_name.startswith(prefix + '/'):
        return branch_name
    return '{}/{}'.format(prefix, branch_name)


def get_whoami() -> str:
    """Get user name."""
    status, stdout, _ = run_child_process(['whoami'], 'stdout')
    if status and stdout:
        return stdout[0]
    return ''


def _normalize_user_branch(branch_name: str) -> str:
    """Normalize on demand."""
    if branch_name in ['master', 'main']:
        return branch_name
    if branch_name == settings.REMOTE_MAIN_STREAM:
        return branch_name
    return _normalize_branch_name(branch_name, get_whoami())


def get_submodule_update() -> List[str]:
    """Tokens to submodule update."""
    return ['submodule', 'update', '--init', '--recursive']


def get_start_branch(args: List[str]) -> List[str]:
    """Tokens to create a new branch base on another(master if not provided)."""
    args = args[:2] if len(args) > 2 else args
    res = ['checkout', '-b']
    res.append(_normalize_user_branch(args[0]))
    res.append(
        _normalize_user_branch(args[1]) if len(args) > 1 \
            else f'origin/{settings.REMOTE_MAIN_STREAM}')
    return res


def get_checkout(args: List[str]) -> List[str]:
    """Tokens to checkout branch."""
    return ['checkout', _normalize_user_branch(args[0])]


def get_abandon(args: List[str]) -> List[str]:
    """Tokens to abandon branch."""
    return ['branch', '-D', _normalize_user_branch(args[0])]


def get_status() -> List[str]:
    """Tokens to show status."""
    return ['status']


def get_branch() -> List[str]:
    """Tokens to show branches."""
    return ['branch']


def get_fetch() -> List[str]:
    """Tokens to fetch commits."""
    return ['fetch']


def get_stage() -> List[str]:
    """Tokens to stage all."""
    return ['stage', '-A']


def get_commit(args: List[str]) -> List[str]:
    """Tokens to commit changes."""
    assert args, 'Must provide args!'
    return ['commit'] + args


def get_commit_message(message: str) -> List[str]:
    """Tokens to commit changes with message."""
    return get_commit(['-m', f'"{message}"'])


def get_commit_amend(no_edit: bool) -> List[str]:
    """Tokens to commit changes with message."""
    args = ['--amend']
    if no_edit:
        args += ['--no-edit']
    return get_commit(args)


def get_reset(commit_sha: str) -> List[str]:
    """Tokens to hard reset to commit sha."""
    assert commit_sha, 'Must provide commit sha!'
    return ['reset', '--hard', commit_sha]


def get_fetch() -> List[str]:
    """Tokens to fetch remote commits."""
    return ['fetch']


def get_rebase() -> List[str]:
    """Tokens to rebase to local master."""
    return ['rebase', f'origin/{settings.REMOTE_MAIN_STREAM}']


def get_current_branch_name() -> List[str]:
    """Tokens to obtain current branch name."""
    # git symbolic-ref --short -q HEAD 2>&1
    return ['symbolic-ref', '--short', '-q', 'HEAD']


def get_publish(args: List[str]) -> List[str]:
    """Tokens to publish to remote branch."""
    return ['push', 'origin', _normalize_user_branch(args[0]), '-f']


def get_list_commit(args: List[str]) -> List[str]:
    """Tokens to list commit with flags."""
    if args:
        return ['log'] + args
    return ['log']


def get_conflict_file() -> List[str]:
    """Tokens to list conflict files."""
    return ['ls-files', '-u', '|', 'cut' '-f', '2', '|', 'sort', '-u']


def get_merge_base() -> List[str]:
    """Tokens to get the merge rebase."""
    return ['merge-base', 'HEAD', f'origin/{settings.REMOTE_MAIN_STREAM}']


def get_diff(commit_sha: str) -> List[str]:
    """Tokens to list the changed files compare with commit sha."""
    return ['diff', '--name-only', 'HEAD', commit_sha]
