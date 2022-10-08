#!/bin/bash

TARGET_PATH=~/.repo_control
mkdir $TARGET_PATH
cp -r ./* $TARGET_PATH/
chmod +x $TARGET_PATH/repo_control_main.py


sudo cp ./repo /usr/share/bash-completion/completions/repo

git config color.status always

pip3 install click > /dev/null

echo "alias repo='${TARGET_PATH}/repo_control_main.py'" >> ~/.bashrc
.  ~/.bashrc
