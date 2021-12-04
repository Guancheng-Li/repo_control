"""
Authors: guanchenglichina@qq.com (Guancheng Li)
The implement of one command.
Some helper functions also added.
TODO(Guancheng): Move helper functions in other places.
"""
import logging, os, git
from typing import Dict

import function_define
from utils.process_utils import (
    run_git_commands_and_print, run_git_commands, run_git_commands_sync
)

def _find_similar_branches(hint):
    res, stdout, _ = run_git_commands(function_define.get_branch())
    candidates = []
    if not res or not stdout:
        return candidates
    for item in stdout:
        item = item[1:].strip()
        if hint in item:
            candidates.append(item)
    return candidates


def _find_merge_base():
    res, stdout, _ = run_git_commands(function_define.get_merge_base())
    if res and len(stdout) == 1:
        return stdout[0]
    return ''


def _print_multiple_branches_hint(branches):
    print('Multiple branches matched, skip:')
    for idx, item in enumerate(branches):
        print(idx + 1, item)
    return


def run_start(branch_name, base_branch):
    args = [branch_name]
    if base_branch:
        args.append(base_branch)
    run_git_commands_and_print(function_define.get_start_branch(args))


def run_checkout(branch_name):
    candidates = _find_similar_branches(branch_name)
    if not candidates:
        run_git_commands_and_print(function_define.get_checkout([branch_name]))
    elif (len(candidates) == 1):
        run_git_commands_and_print(function_define.get_checkout(candidates))
        return
    _print_multiple_branches_hint(candidates)


def run_abandon(branch_name):
    candidates = _find_similar_branches(branch_name)
    if not candidates:  # Not found
        run_git_commands_and_print(function_define.get_abandon([branch_name]))
    elif (len(candidates) == 1):
        run_git_commands_and_print(function_define.get_abandon(candidates))
        return
    _print_multiple_branches_hint(candidates)


def run_submodule_update():
    run_git_commands_and_print(function_define.get_submodule_update())


def run_status():
    run_git_commands_and_print(function_define.get_status())


def run_stage():
    run_git_commands_and_print(function_define.get_stage())


def run_branch():
    run_git_commands_and_print(function_define.get_branch())


def run_drop():
    run_git_commands_and_print(function_define.get_stage())
    run_git_commands_and_print(function_define.get_commit('commit_to_drop'))
    run_git_commands_and_print(function_define.get_reset('HEAD^'))


def run_sync():
    run_git_commands_and_print(function_define.get_sync())


def run_publish():
    _, stdout, _ = run_git_commands(function_define.get_current_branch_name())
    branch_name = None
    if not stdout:
        logging.error('Failed to get current branch name, stop.')
        return
    branch_name = stdout[0]
    args = [branch_name]
    run_git_commands_and_print(function_define.get_publish(args))


def run_list_commit(filters: Dict[str, str]):
    # TODO(Guancheng): Refactor to support more filters
    cmds = None
    author = filters.get('author') if filters.get('author') else function_define.get_whoami()
    cmds = function_define.get_list_commit(['--author', author])
    run_git_commands_and_print(cmds)


def run_conflict():
    run_git_commands_and_print(function_define.get_conflict_file())


def run_diff():
    merge_base_commit = _find_merge_base()
    if merge_base_commit:
        run_git_commands_and_print(function_define.get_diff(merge_base_commit), True)
    else:
        print('Cannot obain the merge base commit sha.')


def run_test():
    # repo = git.Repo(os.getcwd())
    # repo.remotes.origin.pull()
    # os.system('git fetch')
    success, stdout, stderr = run_git_commands(function_define.get_fetch())
    print('Success: ', success)
    print('stdout:\n', stdout)
    print('stderr:\n', stderr)
