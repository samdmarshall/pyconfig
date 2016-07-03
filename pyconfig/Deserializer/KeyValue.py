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
from . import XCLineItem

class KeyValue(XCLineItem):
    
    def __init__(self, line):
        super(KeyValue, self).__init__(line)
        offset = KeyValue.FindKeyValueAssignmentOffset(self.contents, 0)
        self.__key = self.contents[:offset]
        self.__value = self.contents[offset+1:]
    
    @classmethod
    def FindKeyValueAssignmentOffset(cls, line, offset):
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
                return KeyValue.FindKeyValueAssignmentOffset(line[find_close_bracket:], new_offset)
            else:
                print('[xcconfig_kv]: error!')
                return -1;
        else:
            if find_equals != -1:
                new_offset += find_equals
            return new_offset
    
    def key(self):
        key = self.__key
        find_bracket = key.find('[')
        if find_bracket == -1:
            find_space = key.find(' ')
            if find_space != -1:
                return key[:find_space]
            return key
        else:
            return key[:find_bracket]
    
    def conditions(self):
        conditions = {}
        key = self.__key
        find_bracket = key.find('[')
        if find_bracket != -1:
            key_conditions_string = key[find_bracket:]
            condition_strings = list(filter(lambda cond_string: cond_string != '' and cond_string != ' ', re.split(r'[\[|\]]', key_conditions_string)))
            for condition in condition_strings:
                equals_offset = condition.find('=')
                cond_key = condition[:equals_offset]
                cond_value = condition[equals_offset+1:]
                conditions[cond_key] = cond_value
        return conditions
    
    def value(self, value_type):
        value = self.__value
        if len(value) == 0:
            return ''
        if value[0] == ' ':
            value = value[1:]
        comment_offset = value.find('//')
        if comment_offset != -1:
            value = value[:comment_offset]
        if value_type == None:
            return value
        else:
            if value_type == 'string':
                return str(value)
            if value_type == 'stringlist':
                # this has to change to be separated by strings
                return list(value)