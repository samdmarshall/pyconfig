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

import re
from .                   import XCLineItem
from ..Helpers.Switch    import Switch

def shouldAppendConditionItem(condition):
    result = False
    for case in Switch(condition):
        if case(''):
            break
        if case(' '):
            break
        if case():
            result = True
            break
    return result

def splitByConditions(conditions_string):
    results_array = list()
    conditions_string_array = re.split(r'[\[|\]]', conditions_string)
    for condition in conditions_string_array:
        if shouldAppendConditionItem(condition):
            results_array.append(condition)
    return results_array

class KeyValue(XCLineItem.XCLineItem):

    def __init__(self, line):
        super(KeyValue, self).__init__(line)
        offset = KeyValue.findKeyValueAssignmentOffset(self.contents, 0)
        self.__key = self.contents[:offset]
        self.__value = self.contents[offset+1:]

    def __eq__(self, other):
        contents_match = super(KeyValue, self).__eq__(other)
        keys_match = (self.key() == other.key())
        conditions_match = (self.conditions() == other.conditions())
        values_match = (self.value() == other.value())
        configs_match = (keys_match and conditions_match and values_match)
        if contents_match and not configs_match: # pragma: no cover
            raise ValueError('Error in parsing xcconfig files, contents match but parsed results do not!')
        return configs_match

    @classmethod
    def findKeyValueAssignmentOffset(cls, line, offset):
        result_offset = -1
        find_open_bracket = line.find('[')
        find_equals = line.find('=')
        new_offset = offset
        if find_open_bracket != -1:
            # conditional bracket
            find_close_bracket = line.find(']')
            if find_close_bracket != -1:
                find_close_bracket += 1
                # found conditional bracket close
                new_offset += find_close_bracket
                result_offset = cls.findKeyValueAssignmentOffset(line[find_close_bracket:], new_offset)
        else:
            if find_equals != -1:
                new_offset += find_equals
            result_offset = new_offset
        return result_offset

    def key(self):
        key = self.__key
        result_key = key
        find_bracket = key.find('[')
        if find_bracket == -1:
            find_space = key.find(' ')
            if find_space != -1:
                result_key = key[:find_space]
        else:
            result_key = key[:find_bracket]
        return result_key

    def conditions(self):
        conditions = {}
        key = self.__key
        find_bracket = key.find('[')
        if find_bracket != -1:
            key_conditions_string = key[find_bracket:]
            condition_strings_array = splitByConditions(key_conditions_string)
            for condition in condition_strings_array:
                equals_offset = condition.find('=')
                cond_key = condition[:equals_offset]
                cond_value = condition[equals_offset+1:]
                conditions[cond_key] = cond_value
        return conditions

    def value(self):
        value = self.__value
        if len(value) == 0:
            value = ''
        else:
            if value[0] == ' ':
                value = value[1:]
            comment_offset = value.find('//')
            if comment_offset != -1: # pragma: no cover
                value = value[:comment_offset]
        return value
