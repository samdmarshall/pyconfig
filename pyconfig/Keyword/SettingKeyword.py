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

from .             import Constants
from .             import BaseKeyword
from ..Helpers     import OrderedDictionary

class SettingKeyword(BaseKeyword.BaseKeyword):

    def __init__(self):
        super(SettingKeyword, self).__init__()
        self.uses_if = False
        self.uses_for = False

        self.inherits = False

        self.substitutes = False
        self.substitution_variable_name = 'CONFIGURATION'

        self.configuration_values = OrderedDictionary.OrderedDictionary()
        self.default_value = ''

        self.build_setting_name = ''

    def __eq__(self, other): # pragma: no cover
        cmp_name = (self.build_setting_name == other.build_setting_name)
        cmp_if = (self.uses_if and (self.uses_if == other.uses_if))
        cmp_for = (self.uses_for and (self.uses_for == other.uses_for))
        return cmp_name and (cmp_if or cmp_for)

    def consumeForStatement(self, statement):
        configuration_name = statement[1]
        value = ''
        if len(statement) == 3:
            value = statement[2]
        if configuration_name != Constants._specialCase: # pylint: disable=protected-access
            self.configuration_values[configuration_name] = ' '.join(value)
        else:
            self.default_value = ' '.join(value)

    def consumeModifiers(self, modifiers):
        if len(modifiers):
            if modifiers[0] == Constants._use: # pylint: disable=protected-access
                self.substitutes = True
                self.substitution_variable_name = modifiers[1]
            if modifiers[-1] == Constants._inherits: # pylint: disable=protected-access
                self.inherits = True

    def consumeConfigurationAssignment(self, configurations):
        keywords_used = list()
        for setting_configuration in configurations:
            keywords_used.append(setting_configuration[0])

        keyword_used = set(keywords_used)
        if len(keyword_used) > 1: # pragma: no cover
            raise ValueError('More than one type of assignment was used for the build setting "%s"' % self.build_setting_name)

        used_keyword_in_assignemnt = next(iter(keyword_used))
        self.uses_if = (used_keyword_in_assignemnt == Constants._if) # pylint: disable=protected-access
        self.uses_for = (used_keyword_in_assignemnt == Constants._for) # pylint: disable=protected-access

    def consumeIfStatement(self, statement):
        conditions = statement[1]
        assignment_value = statement[2]
        conditional_key_value_list = list()
        for condition in conditions:
            conditional_key_value_list.append('='.join(condition))
        conditional_key_value_string = ','.join(conditional_key_value_list)
        self.configuration_values[conditional_key_value_string] = assignment_value

    def consume(self, parsed_item=None):
        parsed_item = list() if parsed_item is None else parsed_item
        super(SettingKeyword, self).consume(parsed_item)

        if parsed_item[0] != Constants._setting:  # pylint: disable=protected-access
            raise ValueError('SettingKeyword can only consume parsed build setting elements!') # pragma: no cover

        self.build_setting_name = parsed_item[1]
        self.consumeModifiers(parsed_item[2])
        configurations = parsed_item[3]

        self.consumeConfigurationAssignment(configurations)

        for setting_configuration in configurations:
            configuration_type = setting_configuration[0]

            if configuration_type == Constants._for: # pylint: disable=protected-access
                self.consumeForStatement(setting_configuration)

            if configuration_type == Constants._if: # pylint: disable=protected-access
                self.consumeIfStatement(setting_configuration)

    def serializeInheritedValues(self):
        serialize_string = ''
        if self.inherits:
            serialize_string += '$(inherited) '
        return serialize_string

    def isConfigurationCase(self):
        keys = list(self.configuration_values.keys())
        return (len(keys) > 1) or (len(keys) and keys[0] != Constants._specialCase) # pylint: disable=protected-access

    def serializeForStatement(self, key, value):
        serialize_string = ''
        serialize_string += self.build_setting_name
        if self.isConfigurationCase():
            serialize_string += '_' + key
        serialize_string += ' = '
        serialize_string += self.serializeInheritedValues()
        serialize_string += value + '\n'
        return serialize_string

    def serializeForConditionalStatement(self):
        serialize_string = ''
        serialize_string += self.build_setting_name + ' = '
        serialize_string += self.serializeInheritedValues()
        if self.isConfigurationCase():
            serialize_string += '$('+self.build_setting_name+'_$('+self.substitution_variable_name+'))'
            if len(self.default_value):
                serialize_string += ' '
        serialize_string += self.default_value
        serialize_string += '\n'
        return serialize_string

    def serializeIfStatement(self, key, value):
        serialize_string = ''
        serialize_string += self.build_setting_name+'['+key+']'+' = '
        serialize_string += self.serializeInheritedValues()
        serialize_string += value+'\n'
        return serialize_string

    def serialize(self):
        serialize_string = ''
        if self.uses_for:
            for key, value in self.configuration_values.items():
                serialize_string += self.serializeForStatement(key, value)
            serialize_string += self.serializeForConditionalStatement()

        if self.uses_if:
            for key, value in self.configuration_values.items():
                serialize_string += self.serializeIfStatement(key, value)
        return serialize_string
