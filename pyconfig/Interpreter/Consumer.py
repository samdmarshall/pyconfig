# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
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

from .                 import LangParser
from .                 import Dependent
from ..Helpers.Logger  import Logger

def CreateNodeFromString(config_name="", config_contents=""):
    # now parse the file's contents
    parsed_contents = LangParser._config.parseString(config_contents) # pylint: disable=protected-access

    node = Dependent.DependentNode(parsed_contents, config_name)

    return node

def CreateGraphNodes(pyconfig_path_list=None):
    pyconfig_path_list = list() if pyconfig_path_list is None else pyconfig_path_list

    parsed_configs = set()

    for pyconfig_file_path in pyconfig_path_list:
        pyconfig_file = open(pyconfig_file_path, 'r')

        pyconfig_contents = pyconfig_file.read()
        pyconfig_file.close()

        Logger.write().info('Parsing %s ...' % pyconfig_file_path)

        node = CreateNodeFromString(pyconfig_file.name, pyconfig_contents)

        parsed_configs.add(node)

    return parsed_configs
