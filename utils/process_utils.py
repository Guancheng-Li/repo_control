"""
Authors: guanchenglichina@qq.com (Guancheng Li)
Utils for call subprocess command with the subprocess lib.
"""
import logging
import os
import sys

from subprocess import Popen, CalledProcessError, PIPE, STDOUT,check_call
from typing import List


def _run_child_process(cmds: List[str]):
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


def _run_child_process_sync(cmds: List[str]):
    # Not work for publish, print
    if not cmds:
        logging.error('The command is empty.')
        return
    print(' '.join(cmds))


def _process_output(output: object):
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


def run_child_process(cmds: List[str], output):
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


def run_git_commands_sync(cmds: List[str]):
    _run_child_process_sync(['git'] + cmds)


def output_pipe(output, line_number):
    if not output:
        return
    for idx, line in enumerate(output):
        if line_number:
            print(idx + 1, line)
        else:
            print(line)


def run_git_commands(cmds: List[str]):
    return run_child_process(['git'] + cmds, 'all')


def run_git_commands_and_print(cmds: List[str], line_number=False):
    _, stdout, stderr = run_git_commands(cmds)
    output_pipe(stdout, line_number)
    output_pipe(stderr, line_number)
