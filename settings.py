"""
Authors: guanchenglichina@qq.com (Guancheng Li)
Settings for the repo control tool.
"""
import logging
import os
import shutil
import time

# PATH
TEMP_PATH = '/tmp/repo_control'
TEMP_LOGGING_PATH = os.path.join(TEMP_PATH, 'logging')

BASE_PATH = os.path.expanduser('~/.repo_control')
SETTINGS_PATH = os.path.join(BASE_PATH, 'settings')
LOGGING_PATH = os.path.join(BASE_PATH, 'logging')

PATHS = [
    TEMP_PATH,
    TEMP_LOGGING_PATH,
    BASE_PATH,
    SETTINGS_PATH,
    LOGGING_PATH,
]


def _setings_initialization():
    for item in PATHS:
        os.makedirs(item, exist_ok=True)
    logging.info('Settings has been initialized.')


def _clean_up(include_user_path=False):
    if os.path.isdir(TEMP_PATH):
        shutil.rmtree(TEMP_PATH)
    if include_user_path and os.path.isdir(BASE_PATH):
        shutil.rmtree(BASE_PATH)


def _check_settings() -> bool:
    for item in PATHS:
        if not os.path.isdir(item):
            return False
    return True


def settings_setup(simple_mode=False, clean_up=False):
    flag_file = os.path.join(BASE_PATH, 'settings_setup.Done')
    execute = False
    if simple_mode and os.path.isfile(flag_file):
        execute = True

    if clean_up:
        _clean_up(include_user_path=True)
        execute = True

    if not _check_settings():
        execute = True

    if execute:
        _setings_initialization()
        with open(flag_file, 'w+') as fp:
            fp.write(time.time())
