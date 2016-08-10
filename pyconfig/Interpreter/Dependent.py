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

import os
from ..Keyword             import ExportKeyword
from ..Keyword             import IncludeKeyword
from ..Keyword             import Constants
from ..Keyword             import Resolver
from ..Helpers.Logger      import Logger

def findParents(graph, current_config):
    included_configs = list()
    for config in graph:
        if config.exportName() == current_config.include_path:
            included_configs.append(config)
    return included_configs

class DependentNode(object):
    def __init__(self, contents, name):
        self.parents = set()
        self.children = set()
        flat_contents = list()
        starting_index = 0
        if len(contents):
            if contents[0][0] == Constants._export: # pylint: disable=protected-access
                flat_contents.append(contents[0])
                starting_index = 1
        for item in contents[starting_index:]:
            flat_contents.extend(item)
        parsed_contents = list()
        for item in flat_contents:
            resolved_type_initializer = Resolver.ResolveKeywordType(item)
            resolved_item = resolved_type_initializer()
            resolved_item.consume(item)
            parsed_contents.append(resolved_item)
        self.config = parsed_contents
        self.name = name

    def chainParents(self):
        # needs to include the current name or we will never get any elements
        chain = [self.name]
        for parent in self.parents:
            chain = parent.chainParents() + chain
        return chain

    def importChain(self):
        parents = self.chainParents()
        chain = parents + [self.name] # don't include children as they will resolve on their own.
        chain_set = set()
        # uniquing the list that was created
        chain = [link for link in chain if not (link in chain_set or chain_set.add(link))]
        return chain

    def filterContentsByType(self, class_type):
        results = [node for node in self.config if isinstance(node, class_type)]
        return results

    def exportPath(self):
        base_path = os.path.dirname(self.name)
        export_file = self.exportName()
        export_path = os.path.normpath(os.path.join(base_path, export_file))
        return export_path

    def exportName(self):
        xcconfig_name = ''
        exported_name_info = None
        export_info_array = self.filterContentsByType(ExportKeyword.ExportKeyword)
        if len(export_info_array):
            exported_name_info = export_info_array[0]
            xcconfig_name = exported_name_info.export_path
        else:
            file_name = os.path.splitext(os.path.basename(self.name))[0]
            xcconfig_name = file_name + '.xcconfig'
        return xcconfig_name

    def resolvePaths(self, graph):
        config_includes_array = self.filterContentsByType(IncludeKeyword.IncludeKeyword)
        for parent_config in config_includes_array:
            included_config_array = findParents(graph, parent_config)
            if len(included_config_array):
                parent_config_in_graph = included_config_array[0]
                parent_config_in_graph.children.add(self)
                self.parents.add(parent_config_in_graph)
            elif not parent_config.optional:
                Logger.write().warning('Could not find an included pyconfig with export name of "%s"!' % parent_config.include_path)
