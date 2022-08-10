"""
Authors: guanchenglichina@qq.com (Guancheng Li)
The implement of one command.
Some helper functions also added.
TODO(Guancheng): Move helper functions in other places.
"""
import logging
from typing import Dict, List

import function_define
from utils.process_utils import (
    run_git_commands_and_print, run_git_commands
)

def _find_similar_branches(hint: str) -> List[str]:
    """Use hint to find out current local branches contains hint."""
    res, stdout, _ = run_git_commands(function_define.get_branch())
    candidates = []
    if not res or not stdout:
        return candidates
    for item in stdout:
        item = item[1:].strip()
        if hint in item:
            candidates.append(item)
    return candidates


def _find_merge_base() -> str:
    """Call command and find out the merge base commit sha."""
    res, stdout, _ = run_git_commands(function_define.get_merge_base())
    if res and stdout and len(stdout) == 1:
        return stdout[0]
    return ''


def _print_multiple_branches_hint(branches: str) -> None:
    """If multiple branches hit hint, list them."""
    print('Multiple branches matched, skip:')
    for idx, item in enumerate(branches):
        print(idx + 1, item)


def run_start(branch_name: str, base_branch: str) -> None:
    """Start branch on base branch."""
    args = [branch_name]
    if base_branch:
        args.append(base_branch)
    run_git_commands_and_print(function_define.get_start_branch(args))


def run_checkout(branch_name: str) -> None:
    """Checkout branch,
       if branhc name partialy matched with one, swith to it, otherwise, to itself,
       also branch name can be automatically normalized with username.
    """
    candidates = _find_similar_branches(branch_name)
    if not candidates:
        run_git_commands_and_print(function_define.get_checkout([branch_name]))
    elif (len(candidates) == 1):
        run_git_commands_and_print(function_define.get_checkout(candidates))
        return
    _print_multiple_branches_hint(candidates)


def run_abandon(branch_name: str) -> None:
    """Abandon branch, similar logic to find out target branch in checkout."""
    candidates = _find_similar_branches(branch_name)
    if not candidates:  # Not found
        run_git_commands_and_print(function_define.get_abandon([branch_name]))
    elif (len(candidates) == 1):
        run_git_commands_and_print(function_define.get_abandon(candidates))
        return
    _print_multiple_branches_hint(candidates)


def run_submodule_update() -> None:
    """Update submodule."""
    run_git_commands_and_print(function_define.get_submodule_update())


def run_status() -> None:
    """Print status."""
    run_git_commands_and_print(function_define.get_status())


def run_stage() -> None:
    """Stage all files."""
    run_git_commands_and_print(function_define.get_stage())


def run_branch() -> None:
    """Print local branches."""
    run_git_commands_and_print(function_define.get_branch())


def run_drop() -> None:
    """Drop the local changes, dangerous."""
    run_git_commands_and_print(function_define.get_stage())
    run_git_commands_and_print(function_define.get_commit_message('commit_to_drop'))
    run_git_commands_and_print(function_define.get_reset('HEAD^'))


def run_fetch() -> None:
    """Fetch the remote master head."""
    run_git_commands_and_print(function_define.get_fetch())


def run_rebase() -> None:
    """Rebase to local fetched master head."""
    run_git_commands_and_print(function_define.get_rebase())


def run_sync() -> None:
    """Fetch and rebase."""
    run_git_commands_and_print(function_define.get_fetch())
    run_git_commands_and_print(function_define.get_rebase())


def run_publish() -> None:
    """Push to the remote branch."""
    _, stdout, _ = run_git_commands(function_define.get_current_branch_name())
    branch_name = None
    if not stdout:
        logging.error('Failed to get current branch name, stop.')
        return
    branch_name = stdout[0]
    args = [branch_name]
    run_git_commands_and_print(function_define.get_publish(args))


def run_list_commit(filters: Dict[str, str]) -> None:
    """List commits, by default list myself when author not set."""
    # TODO(Guancheng): Refactor to support more filters
    cmds = None
    author = filters.get('author') if filters.get('author') else function_define.get_whoami()
    cmds = function_define.get_list_commit(['--author', author])
    run_git_commands_and_print(cmds)


def run_conflict() -> None:
    """List conflict files, useful if rebase/cherrypick conflicted."""
    run_git_commands_and_print(function_define.get_conflict_file())


def run_diff() -> None:
    """List edited files compare with merge base, useful when many commits in local branch."""
    merge_base_commit = _find_merge_base()
    if merge_base_commit:
        run_git_commands_and_print(function_define.get_diff(merge_base_commit), True)
    else:
        print('Cannot obtain the merge base commit sha.')

def run_amend() -> None:
    """Stage untracked files and amend to the last commit,
       temporarily cannot cannot obtain last commit id,
       won't check if it merged.
    """
    run_stage()
    run_git_commands_and_print(function_define.get_commit_amend(no_edit=True))


def run_test() -> None:
    """Test function to develop."""
    success, stdout, stderr = run_git_commands(function_define.get_fetch())
    print('Success: ', success)
    print('stdout:\n', stdout)
    print('stderr:\n', stderr)
