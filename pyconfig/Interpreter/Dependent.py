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

class DependentNode(object):
    def __init__(self, contents, name):
        self.parents = set()
        self.children = set()
        flat_contents = list()
        starting_index = 0
        if len(contents):
            if contents[0][0] == Constants._export:
                flat_contents.append(contents[0])
                starting_index = 1
        for item in contents[starting_index:]:
            flat_contents.extend(item)
        parsed_contents = list()
        for item in flat_contents:
            ResolvedType = Resolver.ResolveKeywordType(item)
            resolved_item = ResolvedType()
            resolved_item.consume(item)
            parsed_contents.append(resolved_item)
        self.config = parsed_contents
        self.name = name
    
    def __repr__(self): # pragma: no cover
        return self.name

    def filterContentsByType(self, class_type):
        return list(filter(lambda node: type(node) == class_type, self.config))
    
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
            if len(export_info_array) > 1: # pragma: no cover
                Logger.write().error('More than one export keyword per file in %s !' % self.name)
        if exported_name_info:
            xcconfig_name = exported_name_info.export_path
        else:
            file_name = os.path.splitext(os.path.basename(self.name))[0]
            xcconfig_name = file_name + '.xcconfig'
        return xcconfig_name
    
    def resolvePaths(self, graph):
        found_included_configs = None
        config_includes_array = self.filterContentsByType(IncludeKeyword.IncludeKeyword)
        for parent_config in config_includes_array:
            exported_name = parent_config.include_path
            included_config_array = list(filter(lambda config: config.exportName() == exported_name, graph))
            if len(included_config_array):
                parent_config_in_graph = included_config_array[0]
                parent_config_in_graph.children.add(self)
                self.parents.add(parent_config_in_graph)
            else: # pragma: no cover
                Logger.write().warning('Could not find an included pyconfig with export name of "%s"!' % exported_name)

            
            