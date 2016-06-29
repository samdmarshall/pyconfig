#!/usr/bin/env python

import sys
import os
import filecmp
import shutil

# Copies the commit-msg file into the .git/hooks directory to be executed by
# git during commits if it does not already exist or if the file has been changed. 
# Files in the .git/hooks are not tracked, so any updates to commit-msg must 
# occur in the root and be copied over.
base_git_hooks_path = '.git/hooks/'
base_tools_hooks_path = './tools/hooks/'
hooks = [ 'pre-commit', 'post-commit' ]

for hook in hooks:
    tools_hook_path = os.path.join(base_tools_hooks_path, hook)
    git_hook_path = os.path.join(base_git_hooks_path, hook)
    if not os.path.exists(git_hook_path) or filecmp.cmp(tools_hook_path, git_hook_path):
        shutil.copy2(tools_hook_path, base_git_hooks_path)
