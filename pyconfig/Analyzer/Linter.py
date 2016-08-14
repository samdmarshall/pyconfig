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

import string
from ..                   import Keyword
from ..Helpers.Logger     import Logger
from ..Helpers.Switch     import Switch

build_setting_char_set = string.ascii_letters + '_' + string.digits

class Linter(object):
    def __init__(self, contents):
        self.error = None
        self.contents = contents
        self.index = 0
        self.line_number = 1
        self.char_number = 1
        self.last_newline = 0

    def readWhitespace(self, current_char, optional=False):
        status = current_char in string.whitespace
        if status is True:
            if current_char == '\n':
                self.line_number += 1
                self.char_number = 0
                self.last_newline = self.index + 1
            self.index += 1
            self.char_number += 1
        else:
            if optional is False: # pragma: no cover
                self.error = (self.contents[self.last_newline:self.index]+'|')
        return status

    def readScope(self, starter, closer):
        current_char = self.contents[self.index]
        start_line_number = self.line_number
        start_char_number = self.char_number
        status = current_char == starter
        scope_level = 0
        if status is True:
            scope_level += 1
        else: # pragma: no cover
            self.error = 'Expected character `%s`, encountered `%s` at line: %i, index: %i' % (starter, current_char, self.line_number, self.char_number)
        self.index += 1
        self.char_number += 1
        start = self.index
        end = start
        while status is True and scope_level != 0:
            # ensure we don't go out of bounds of the content we are searching
            if self.index >= len(self.contents):
                self.error = 'Missing `%s` for `%s` on line: %i, index: %i' % (closer, starter, start_line_number, start_char_number)
                status = False
                break
            # get the current character to look at
            current_char = self.contents[self.index]
            # consume any whitespace
            status = self.readWhitespace(current_char, True)
            if status is False:
                # if there wasn't whitespace, then advance the counter and make sure we continue
                ## without any errors
                self.index += 1
                self.char_number += 1
                status = True
            if current_char == starter:
                scope_level += 1
            if current_char == closer:
                scope_level -= 1
                end = self.index
        # don't include the last bracket
        end -= 1
        return (status, self.contents[start:end])

    def readFromCharacterSetUntilCharacter(self, char_set, terminate_char):
        status = True
        current_char = self.contents[self.index]
        while current_char in char_set:
            self.index += 1
            self.char_number += 1
            current_char = self.contents[self.index]
        status = current_char == terminate_char
        if status is False: # pragma: no cover
            self.error = 'Encountered `%s` before `%s` at line: %i, index: %i' % (current_char, terminate_char, self.line_number, self.char_number)
        return status

    def readQuotedString(self):
        status = True
        while status is True:
            status = self.readString('"')
            if status is False: break
            # check to see that we have a end-quote before the newline
            status = self.findCharacterBeforeCharacter('"', '\n')
            if status is False: break
            # read end of quote
            status = self.readString('"')
            if status is False: break
            break
        return status

    def readString(self, string_value, optional=False):
        read_string = self.contents[self.index:self.index+len(string_value)]
        status = read_string == string_value
        if status is True:
            self.index += len(string_value)
            self.char_number += len(string_value)
        else:
            if optional is False: # pragma: no cover
                self.error = 'Expected `%s` at line %i, index: %i' % (string_value, self.line_number, self.char_number)
        return status

    def findCharacterBeforeCharacter(self, expected_char, unexpected_char):
        status = True
        unexpected_index = self.contents[self.index:].find(unexpected_char)
        expected_index = self.contents[self.index:].find(expected_char)
        if unexpected_index != -1:
            status = expected_index < unexpected_index
        if status is False: # pragma: no cover
            self.error = 'Expected `%s` before `%s` at line %i, index: %i' % (expected_char, unexpected_char, self.line_number, self.char_number)
        else:
            self.index += expected_index
        return status

    def validates(self):
        should_advance = len(self.contents) > 0
        status = True
        has_finished_exports = False
        has_finished_includes = False
        first_export = True
        current_keyword = None
        while should_advance is True and status is True:
            current_character = self.contents[self.index]
            for case in Switch(current_character):
                if case(Keyword.Constants._comment[0]):
                    old_index = self.index
                    self.index += self.contents[self.index:].index('\n')
                    self.char_number += self.index - old_index
                    break
                if case(Keyword.Constants._export[0]):
                    status = has_finished_exports is False
                    if status is False: # pragma: no cover
                        self.error = 'Encountered keyword `%s` after encountering keyword `%s`. Please place the `%s` keyword before the `%s` keyword.' % (Keyword.Constants._export, current_keyword, Keyword.Constants._export, current_keyword)
                        break
                    status = first_export is True
                    if status is False: # pragma: no cover
                        self.error = 'Encountered more than one `%s` keyword at line %i, index: %i' % (Keyword.Constants._export, line_number, char_number)
                        break
                    status = self.readString(Keyword.Constants._export)
                    if status is False: break
                    # check for a white space
                    status = self.readString(' ')
                    if status is False: break
                    # check for double-quote string
                    status = self.readQuotedString()
                    first_export = False
                    break
                if case(Keyword.Constants._required_include[0]): pass
                if case(Keyword.Constants._optional_include[0]): pass
                if case(Keyword.Constants._include[0]):
                    current_keyword = Keyword.Constants._include
                    has_finished_exports = True
                    if current_character == Keyword.Constants._required_include[0] \
                         or current_character == Keyword.Constants._optional_include[0]:
                        self.index += 1
                        self.char_number += 1
                    status = self.readString(Keyword.Constants._include)
                    if status is False: break
                    # check for a white space
                    status = self.readString(' ')
                    if status is False: break
                    # check for double-quote string
                    status = self.readQuotedString()
                    break
                if case(Keyword.Constants._setting[0]):
                    current_keyword = Keyword.Constants._setting
                    has_finished_exports = True
                    has_finished_includes = True
                    # read the setting keyword
                    status = self.readString(Keyword.Constants._setting)
                    if status is False: break
                    # read whitespace
                    status = self.readString(' ')
                    if status is False: break
                    # read the build setting name
                    status = self.readFromCharacterSetUntilCharacter(build_setting_char_set, ' ')
                    if status is False: break
                    # read whitespace
                    status = self.readString(' ')
                    if status is False: break
                    # read optional "use"
                    status = self.readString(Keyword.Constants._use, True)
                    if status is True:
                        status = self.readString(' ')
                        if status is False: break
                        status = self.readFromCharacterSetUntilCharacter(build_setting_char_set, ' ')
                        if status is False: break
                        status = self.readString(' ')
                        if status is False: break
                    # read optional "inherits"
                    status = self.readString(Keyword.Constants._inherits, True)
                    if status is True:
                        status = self.readString(' ')
                        if status is False: break
                    # read scope
                    status, scope_contents = self.readScope('{', '}')
                    if status is False: break
                    # read contents to ensure it is valid
                    break
                if case():
                    status = self.readWhitespace(current_character)
                    break
            should_advance = self.index < len(self.contents)
        return status
