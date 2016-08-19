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
from ..Settings           import TypeConstants
from ..Settings           import Builtin
from ..Settings           import Runtime
from ..Keyword            import SettingKeyword
from ..Helpers.Logger     import Logger
from ..SCM                import SCM

def findPreviousDefinition(kv_array, configuration, setting_key):
    previous_definition_indexes = list()
    for file_name, value in kv_array:
        if file_name != configuration:
            setting_values = list(value.keys())
            if setting_key in setting_values:
                previous_definition_indexes.append(file_name)
    return previous_definition_indexes

def findDuplicates(dictionary):
    results = dict()
    settings_set = set()
    snapshot_of_dict = list(dictionary.items())
    for configuration, values in snapshot_of_dict:
        setting_values = list(values.keys())
        duplicates = settings_set.copy()
        shared_values = duplicates.intersection(setting_values)
        if len(shared_values):
            for item in shared_values:
                previous_definitions = findPreviousDefinition(snapshot_of_dict, configuration, item)
                previous_definitions.append(configuration)
                results[item] = previous_definitions
        settings_set.update(setting_values)
    return results

def gatherAllVariables(dictionary):
    settings_set = set()
    snapshot_of_dict = list(dictionary.items())
    for _configuration, values in snapshot_of_dict:
        for keyword in values.values():
            settings_set.add(keyword.build_setting_name)
            if keyword.substitutes:
                settings_set.add(keyword.substitution_variable_name)
    return settings_set

class Engine(object):

    def __init__(self):
        # accessing the lookup tables
        self.__type_table = TypeConstants.ConstantLookupTable
        self.__builtin_table = Builtin.BuiltinLookupTable
        self.__runtime_table = Runtime.RuntimeLookupTable
        self.__namespace_table = dict()
        self.__user_defined_table = set()

    def __runInitializer(self, configuration):
        """
        This method is to pass through the passed in file
        """
        self.__namespace_table[configuration.name] = dict()
        for item in configuration.config:
            is_setting = isinstance(item, SettingKeyword.SettingKeyword)
            if is_setting:
                is_unset = (item.build_setting_name not in list(self.__namespace_table[configuration.name].keys()))
                if is_unset:
                    self.__namespace_table[configuration.name][item.build_setting_name] = item
                else: # pragma: no cover
                    previous_item = self.__namespace_table[configuration.name][item.build_setting_name]
                    current_line_number = str(item._BaseKeyword__parsed_item.line) # pylint: disable=protected-access
                    previous_line_number = str(previous_item._BaseKeyword__parsed_item.line) # pylint: disable=protected-access
                    print_string = 'Found duplicate defintion for "'+item.build_setting_name+'":'\
                        '\n> '+configuration.name+':'+current_line_number+''\
                        '\n> '+configuration.name+':'+previous_line_number+''
                    Logger.write().warning(print_string)

    def __runDuplicates(self, configuration):
        duplicate_results = findDuplicates(self.__namespace_table)
        for key, value in list(duplicate_results.items()):
            for file_containing_dups in value:
                if file_containing_dups == configuration.name:
                    # if this is the current config, then ignore it and move on
                    continue
                if file_containing_dups in configuration.importChain(): # pragma: no cover
                    # only raise a warning if a duplicate build setting is declared
                    ## in the same chain of imports.
                    print_message = 'Found duplicate definition for "'+key+'" in files:'\
                        '\n> '+configuration.name+'' \
                        '\n> '+file_containing_dups
                    Logger.write().warning(print_message)

    def __gatherUserDefinedVariables(self):
        self.__user_defined_table = set()
        snapshot_of_dict = list(self.__namespace_table.items())
        for _configuration, values in snapshot_of_dict:
            for keyword in values.values():
                build_setting_name = keyword.build_setting_name
                is_builtin = build_setting_name in self.__builtin_table
                is_runtime = build_setting_name in self.__runtime_table
                is_known = build_setting_name in self.__type_table.keys()
                if not is_builtin and not is_runtime and not is_known:
                    self.__user_defined_table.add(build_setting_name)

    def __runMissing(self):
        variables = gatherAllVariables(self.__namespace_table)
        # remove any variables that are defined as part of the builtin set
        variables.difference_update(self.__builtin_table)
        # remove any variables that are defined at runtime
        variables.difference_update(self.__runtime_table)
        # remove any known variable that gets defined by Xcode
        variables.difference_update(self.__type_table.keys())
        # remove variables specifically defined by the user
        variables.difference_update(self.__user_defined_table)
        # this leaves only variables that are not defined by Xcode or by the user
        for key in variables: # pragma: no cover
            # note that this will announce for each time a config containing a
            ## build setting that is not defined is used. meaning that this
            ## will trigger multiple times for the same issue, this is intended
            ## as each chain of imported configs should be treated as if used
            ## for a separate build configuration
            Logger.write().warning('No definition for variable "%s"' % key)

    def process(self, configuration):
        # ignore the SCM generated configuration file
        Logger.write().debug('Analyzer is processing "%s"' % configuration.name)
        if os.path.basename(configuration.name) != SCM.SCM_NODE_NAME:
            Logger.write().info('Analyzing %s ...' % configuration.name)
            self.__runInitializer(configuration)
            self.__runDuplicates(configuration)
            self.__gatherUserDefinedVariables()
            self.__runMissing()
