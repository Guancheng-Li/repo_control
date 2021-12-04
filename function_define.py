"""
Authors: guanchenglichina@qq.com (Guancheng Li)
Define commands.
"""
from utils.process_utils import run_child_process

def _normalize_branch_name(branch_name, prefix):
    # TODO(Guancheng): add ut
    if branch_name.startswith(prefix + '/'):
        return branch_name
    return '{}/{}'.format(prefix, branch_name)


def get_whoami():
    status, stdout, _ = run_child_process(['whoami'], 'stdout')
    if status and stdout:
        return stdout[0]
    return ''


def _normalize_user_branch(branch_name):
    if branch_name in ['master', 'main']:
        return branch_name
    return _normalize_branch_name(branch_name, get_whoami())


def get_submodule_update():
    return ['submodule', 'update', '--init', '--recursive']


def get_start_branch(args):
    args = args[:2] if len(args) > 2 else args
    # TODO add who am i
    res = ['checkout', '-b']
    res.append(_normalize_user_branch(args[0]))
    res.append(_normalize_user_branch(args[1]) if len(args) > 1 else 'origin/master')
    return res


def get_checkout(args):
    return ['checkout', _normalize_user_branch(args[0])]


def get_abandon(args):
    return ['branch', '-D', _normalize_user_branch(args[0])]


def get_status():
    return ['status']


def get_branch():
    return ['branch']


def get_fetch():
    return ['fetch']


def get_stage():
    return ['stage', '-A']


def get_commit(m):
    assert m, 'Must provide message info!'
    return ['commit', '-m', '\'{}\''.format(m)]


def get_reset(commit):
    assert commit, 'Must provide commit sha!'
    return ['reset', '--hard', commit]


def get_sync():
    # git pull origin master
    return ['rebase', 'origin/master']


def get_current_branch_name():
    # git symbolic-ref --short -q HEAD 2>&1
    return ['symbolic-ref', '--short', '-q', 'HEAD']


def get_publish(args):
    return ['push', 'origin', _normalize_user_branch(args[0]), '-f']


def get_list_commit(args):
    if args:
        return ['log'] + args
    return ['log']


def get_conflict_file():
    return ['ls-files', '-u', '|', 'cut' '-f', '2', '|', 'sort', '-u']


def get_merge_base():
    return ['merge-base', 'HEAD', 'origin/master']


def get_diff(commit):
    return ['diff', '--name-only', 'HEAD', commit]
