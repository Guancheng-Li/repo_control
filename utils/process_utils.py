"""
Authors: guanchenglichina@qq.com (Guancheng Li)
Utils for call subprocess command with the subprocess lib.
"""
import logging

from subprocess import Popen, CalledProcessError, PIPE
from typing import List, Tuple


def _run_child_process(cmds: List[str]) -> Tuple[bool, List[str], List[str]]:
    """Run command and return exit status, stdout, and stderr."""
    if not cmds:
        logging.error('The command is empty.')
        return False, None, None
    try:
        with Popen(cmds, stdout=PIPE, stderr=PIPE) as p:
            stdout, stderr = p.communicate()
    except CalledProcessError as e:
        logging.exception(
            'Subprocess error:\nCommand: {}\n{}'.format(' '.join(cmds)), str(e))
    return True, stdout, stderr


def _process_output(output: object) -> List[str]:
    """Decode and split by lines."""
    if not output:
        return None
    res = None
    try:
        res = output.decode()
    except ValueError as e:
        logging.exception(
            'Decode PIPE error:\PIPE: {}\n{}'.format(output), str(e))
        return None
    res = res.split('\n') if res else []
    res = [line for line in res if line]
    return res


def _print_pipe(output: List[str], line_number: bool) -> None:
    """Print pipe output line by line."""
    if not output:
        return
    for idx, line in enumerate(output):
        if line_number:
            print(idx + 1, line)
        else:
            print(line)


def run_child_process(cmds: List[str], output) -> Tuple[bool, List[str], List[str]]:
    """Run command and return exit status, maybe stdout, and stderr."""
    result, stdout, stderr = _run_child_process(cmds)
    if not result:
        return False, None, None
    if output == 'stdout':
        return True, _process_output(stdout), None
    if output == 'stderr':
        return True, None, _process_output(stderr)
    if output == 'all':
        return True, _process_output(stdout), _process_output(stderr)
    logging.error('Not supported mode: {}'.format(output))
    return False, None, None


def run_git_commands(cmds: List[str]) -> Tuple[bool, List[str], List[str]]:
    """Execute git commands, with out git bin."""
    return run_child_process(['git'] + cmds, 'all')


def run_git_commands_and_print(cmds: List[str], line_number=False) -> None:
    """Run git commands, print to screen."""
    _, stdout, stderr = run_git_commands(cmds)
    _print_pipe(stdout, line_number)
    _print_pipe(stderr, line_number)
