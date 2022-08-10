#!/usr/bin/env python3
"""
Authors: guanchenglichina@qq.com (Guancheng Li)
An repo control tool for simplify the git command.

ONLY the simplest function statements,
DO NOT implement functions in this file,
WON'T obey code style in other files considering the click decorator and arg process.
"""

import click
import logging

import git_command_impl


def setup_logging(logging_level):
    log = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging_level)


########## Statements ##########
@click.group()
def main():
    setup_logging(logging.INFO)


@main.command()
def version():
    click.echo('1.0.1')


@main.command()
@click.argument('branch_name', nargs=1, required=True)
@click.option('--base-branch', type=str, default='', help='Base branch.')
def start(branch_name, base_branch):
    # TODO(Guancheng): Add flag for no username.
    git_command_impl.run_start(branch_name, base_branch)


@main.command()
@click.argument('branch_name', nargs=1, required=True)
def checkout(branch_name):
    # TODO(Guancheng): Add flag for no username.
    git_command_impl.run_checkout(branch_name)


@main.command()
@click.argument('branch_name', nargs=1, required=True)
def abandon(branch_name):
    # TODO(Guancheng): Add flag for no username.
    git_command_impl.run_abandon(branch_name)


@main.command()
def submodule_update():
    git_command_impl.run_submodule_update()


@main.command()
def status():
    git_command_impl.run_status()


@main.command()
def branch():
    git_command_impl.run_branch()


@main.command()
def sync():
    git_command_impl.run_sync()


@main.command()
def fetch():
    git_command_impl.run_fetch()


@main.command()
def rebase():
    git_command_impl.run_rebase()


@main.command()
def stage():
    git_command_impl.run_stage()


@main.command()
def publish():
    git_command_impl.run_publish()


@main.command()
def drop():
    git_command_impl.run_drop()


@main.command()
@click.option('--author', type=str, default='', help='Commit author.')
def list_commit(author):
    filters = {'author': author}
    git_command_impl.run_list_commit(filters)


@main.command()
def conflict():
    # NOT tested
    git_command_impl.run_conflict()


@main.command()
def diff():
    git_command_impl.run_diff()


@main.command()
def amend():
    git_command_impl.run_amend()


@main.command()
def test():
    git_command_impl.run_test()


if __name__ == '__main__':
    main()
