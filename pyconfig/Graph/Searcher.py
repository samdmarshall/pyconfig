# Copyright (c) 2016-2020, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/pyconfig
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import typing
from ..Helpers.Logger import Logger

def LocateParentWithPath(start_file_path: str, parent_item: str) -> typing.Optional[str]:
    parent_path: typing.Optional[str] = start_file_path
    search_file_path = os.path.join(start_file_path, parent_item)
    if start_file_path == '/':
        parent_path = None
    if os.path.isdir(search_file_path) is False and parent_path is not None:
        parent_path = LocateParentWithPath(os.path.dirname(start_file_path), parent_item)
    return parent_path

def locateWorkingDirectoryForPath(file_path: str) -> str:
    working_path = file_path
    if os.path.isfile(file_path):
        fs_path = os.path.dirname(file_path)
        working_path = os.path.normpath(os.path.join(os.getcwd(), fs_path))
    return working_path

def locateDirectories(root: str, dirs: list) -> list:
    found_configs = list()
    for dir_name in dirs:
        relative_path = os.path.join(root, dir_name)
        found_configs.extend(locateConfigs(relative_path))
    return found_configs

def locateFiles(root: str, files: list) -> list:
    found_configs = list()
    for file_name in files:
        relative_path = os.path.join(root, file_name)
        full_path = os.path.normpath(os.path.join(os.getcwd(), relative_path))
        _name, extension = os.path.splitext(file_name)
        if extension == '.pyconfig':
            Logger.write().info('Found %s' % relative_path)
            found_configs.append(full_path)
    return found_configs

def locateConfigs(fs_path: str) -> list:
    found_configs = list()
    for root, dirs, files in os.walk(fs_path, followlinks=True):
        found_configs.extend(locateDirectories(root, dirs))
        found_configs.extend(locateFiles(root, files))
    if not os.path.isdir(fs_path):
        full_path = os.path.normpath(os.path.join(os.getcwd(), fs_path))
        found_configs.append(full_path)
    return found_configs
