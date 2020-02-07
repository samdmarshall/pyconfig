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

import string
import typing
from ..                   import Keyword
from ..Helpers.Logger     import Logger
from ..Helpers.Switch     import Switch
from ..Interpreter        import LangParser

build_setting_char_set = string.ascii_letters + '_' + string.digits

# pylint: disable=protected-access

def readStringFromContent(string_value, content=None, at_index=None) -> typing.Tuple[bool, int]:
    Logger.write().debug('Attempting to read `%s`' % string_value)
    end_index = at_index+len(string_value)
    read_string = content[at_index:end_index]
    status = read_string == string_value
    return (status, len(string_value))

def readUntilStringInContent(terminate_value, content=None, index=None) -> typing.Tuple[bool, int]:
    status = True
    start_index = index
    should_advance = index < len(content)
    current_char = content[index]
    while current_char != terminate_value and should_advance:
        index += 1
        current_char = content[index]
        should_advance = index+1 < len(content)
    status = current_char == terminate_value
    return (status, index - start_index)

def readFromCharacterSet(char_set, content=None, index=None) -> typing.Tuple[bool, int]:
    status = True
    start_index = index
    should_advance = index < len(content)
    current_char = content[index]
    while current_char in char_set and should_advance:
        index += 1
        current_char = content[index]
        should_advance = index+1 < len(content)
    return (status, index - start_index)

def readFromCharSetUntilCharFromContent(char_set, terminate_char, content=None, index=None) -> typing.Tuple[bool, int]:
    status, read_count = readFromCharacterSet(char_set, content, index)
    if status is True:
        current_char = content[index+read_count]
        status = current_char == terminate_char
    return (status, read_count)

def readScopeFromContent(starter, closer, content=None, index=None) -> typing.Tuple[bool, list, int, typing.Optional[str]]:
    current_char = content[index]
    error_msg = None
    status = current_char == starter
    scope_level = 0
    if status is True:
        scope_level += 1
    else: # pragma: no cover
        error_msg = 'Expected character `%s`, encountered `%s` ' % (starter, current_char)
    # advance past the scope starter
    start = index
    index += 1
    end = start
    while status is True and scope_level != 0:
        # ensure we don't go out of bounds of the content we are searching
        status = index <= len(content)
        if status is False: # pragma: no cover
            error_msg = 'Missing `%s` for `%s`' % (closer, starter)
            break
        # get the current character to look at
        current_char = content[index]
        # consume any whitespace
        status, index, _, _, _, error_msg = readWhitespace(content, index)
        if error_msg is not None:
            # the only error message that will come out of the `readWhitespace` function
            ## is that it encountered a non-whitespace character. This isn't really an
            ## error so instead of trying to fake it by continuing, we are going to try
            ## to reach another character of another type.
            status, index, error_msg = readNonWhitespace(content, index)
        if error_msg is not None:
            # now throw an error, because we have encountered a case that should be
            ## raised to the user's awareness.
            Logger.write().error(error_msg)
        # if a scope starter is encountered then increase the current scope level
        if current_char == starter:
            scope_level += 1
        # if a scope closer is encountered then decrease the current scope level
        if current_char == closer:
            scope_level -= 1
            # save the index that the scope ended on so we can capture the entire scope
            end = index
    # trip the ending brace
    end -= 1
    return  (status, content[start+1:end], index-start, error_msg)

def readConditionFromContent(content=None, index=None) -> typing.Tuple[bool, int]: # pylint: disable=too-many-branches
    status = True
    current_char = content[index]
    original_index = index
    for case in Switch(current_char):
        if case('a'):
            status, read_count = readStringFromContent('arch', content, index)
            if status is True:
                index += read_count
            break
        if case('c'):
            status, read_count = readStringFromContent('config', content, index)
            if status is True:
                index += read_count
            break
        if case('s'):
            status, read_count = readStringFromContent('sdk', content, index)
            if status is True:
                index += read_count
            break
        if case('v'):
            status, read_count = readStringFromContent('variant', content, index)
            if status is True:
                Logger.write().warning('Use of `variant` conditional value, this could exhibit unexpected behavior!')
                index += read_count
            break
        if case('d'):
            status, read_count = readStringFromContent('dialect', content, index)
            if status is True:
                Logger.write().warning('Use of `dialect` conditional value, this could exhibit unexpected behavior!')
                index += read_count
            break
        if case(): # pragma: no cover
            break
    # ensure reading should continue
    while status is True:
        # read `=`
        status, read_count = readStringFromContent('=', content, index)
        if status is False:
            break # pragma: no cover
        index += read_count
        # read conditional value assignment
        status, read_count = readUntilStringInContent(' ', content, index)
        if status is False:
            status, read_count = readUntilStringInContent('\n', content, index)
        if status is False:
            break # pragma: no cover
        index += read_count
        break
    return (status, index - original_index)

def readNonWhitespace(content=None, index=None) -> typing.Tuple[bool, int, typing.Optional[str]]:
    error_msg = None
    current_char = content[index]
    status = current_char not in string.whitespace
    if status is True:
        index += 1
    else:
        error_msg = 'Was expecting non-whitespace after a failure to read whitespace, but encountered a whitespace character!'
    result = (status, index, error_msg)
    return result

def readWhitespace(content=None, index=None) -> typing.Tuple[bool, int, int, int, int, typing.Optional[str]]:
    line_number = 0
    char_number = 0
    last_newline = -1
    error = None
    current_char = content[index]
    status = current_char in string.whitespace
    if status is True:
        if current_char == '\n':
            line_number += 1
            char_number = -2
            last_newline = index + 1
        index += 1
        char_number += 1
    else:
        error = ('Expected whitespace, but found `%s`' % current_char)
    result = (status, index, line_number, char_number, last_newline, error)
    return result

def validateCommaSeparatedValues(content) -> bool:
    index = 0
    status = index < len(content)
    while status is True:
        # check to see if this is a single value assignment, if so we can short-circuit
        ## the check and exit now
        first_comma_index = content[index:].find(',')
        if first_comma_index == -1:
            break
        # now perform a full check on the content
        results = LangParser._genericCSVList.parseString(content)
        status = len(results) > 0 and len(results[-1]) > 0
        break
    return status

class Linter(object):
    def __init__(self, contents):
        self.error = None

        self.contents = contents

        self.index = 0
        self.line_number = 1
        self.char_number = 1
        self.last_newline = 0

        self.has_finished_exports = False
        self.has_finished_includes = False
        self.first_export = True
        self.current_keyword = None

    def readWhitespace(self, content=None, index=None) -> bool:
        status, index_increase, line_increase, char_number, last_newline_increase, error = readWhitespace(content, index)
        # update error message
        if error is not None: # pragma: no cover
            self.error = '%s at line: %i, index: %i' % (error, self.line_number, self.char_number)
        while status is True:
            # update the index
            self.index = index_increase
            # update the line number
            self.line_number += line_increase
            # update the char number
            if char_number == -1:
                self.char_number = 1
            else:
                self.char_number += char_number
            # update the last newline index
            if last_newline_increase != -1:
                self.last_newline = last_newline_increase
            break
        return status

    def readScope(self, starter, closer) -> typing.Tuple[bool, list]:
        Logger.write().debug('Attempting to read content between matching `%s` and `%s`' % (starter, closer))
        current_char = self.contents[self.index]
        start_line_number = self.line_number
        start_char_number = self.char_number
        status = current_char == starter
        scope_level = 0
        if status is True:
            scope_level += 1
        else: # pragma: no cover
            self.error = 'Expected character `%s`, encountered `%s` at line: %i, index: %i' % (starter, current_char, self.line_number, self.char_number)
        # advance past the scope starter
        self.index += 1
        self.char_number += 1
        start = self.index
        end = start
        while status is True and scope_level != 0:
            # ensure we don't go out of bounds of the content we are searching
            status = self.index <= len(self.contents)
            if status is False: # pragma: no cover
                self.error = 'Missing `%s` for `%s` on line: %i, index: %i' % (closer, starter, start_line_number, start_char_number)
                break
            # get the current character to look at
            current_char = self.contents[self.index]
            # consume any whitespace
            status = self.readWhitespace(self.contents, self.index)
            if status is False:
                # if there wasn't whitespace, then advance the counter and make sure we continue
                ## without any errors
                self.index += 1
                self.char_number += 1
                status = True
            # if a scope starter is encountered then increase the current scope level
            if current_char == starter:
                scope_level += 1
            # if a scope closer is encountered then decrease the current scope level
            if current_char == closer:
                scope_level -= 1
                # save the index that the scope ended on so we can capture the entire scope
                end = self.index
        # don't include the last bracket
        end -= 1
        return (status, self.contents[start:end])

    def readFromCharacterSetUntilCharacter(self, char_set, terminate_char) -> bool:
        status, read_count = readFromCharSetUntilCharFromContent(char_set, terminate_char, self.contents, self.index)
        self.index += read_count
        self.char_number += read_count
        current_char = self.contents[self.index]
        if status is False: # pragma: no cover
            self.error = 'Encountered `%s` before `%s` at line: %i, index: %i' % (current_char, terminate_char, self.line_number, self.char_number)
        return status

    def readQuotedString(self) -> bool:
        status = True
        while status is True:
            status = self.readString('"')
            if status is False:
                break # pragma: no cover
            # check to see that we have a end-quote before the newline
            status = self.findCharacterBeforeCharacter('"', '\n')
            if status is False:
                break # pragma: no cover
            # read end of quote
            status = self.readString('"')
            if status is False:
                break # pragma: no cover
            break
        return status

    def readString(self, string_value, optional=False) -> bool:
        status, read_count = readStringFromContent(string_value, self.contents, self.index)
        if status is True:
            self.index += read_count
            self.char_number += read_count
        else:
            if optional is False: # pragma: no cover
                self.error = 'Expected `%s` at line %i, index: %i' % (string_value, self.line_number, self.char_number)
        return status

    def findCharacterBeforeCharacter(self, expected_char, unexpected_char) -> bool:
        status = True
        unexpected_index = self.contents[self.index:].find(unexpected_char)
        expected_index = self.contents[self.index:].find(expected_char)
        if unexpected_index != -1:
            status = expected_index < unexpected_index
        else:
            Logger.write().debug('Could not find `%s` after `%s`, continuing...' % (unexpected_char, expected_char))
        if status is False: # pragma: no cover
            self.error = 'Expected `%s` before `%s` at line %i, index: %i' % (expected_char, unexpected_char, self.line_number, self.char_number)
        else:
            self.index += expected_index
        return status

    def validateIf(self, scope_contents, index) -> typing.Tuple[bool, int]: # pylint: disable=too-many-branches
        status = True
        while status is True:
            should_try_reading_assignment = True
            # read `if`
            status, read_count = readStringFromContent('if', scope_contents, index)
            if status is False:
                break # pragma: no cover
            index += read_count
            # read whitespace
            status, read_count = readStringFromContent(' ', scope_contents, index)
            if status is False:
                break # pragma: no cover
            index += read_count
            # read condition
            reading_conditions = True
            while reading_conditions is True and status is True:
                # read conditional
                status, read_count = readConditionFromContent(scope_contents, index)
                if status is False:
                    break # pragma: no cover
                index += read_count
                # if the next character is a newline, then break, because this is the end of this definition
                newline_index = scope_contents[index:].find('\n')
                is_newline = newline_index == 0
                if is_newline:
                    should_try_reading_assignment = False
                    break
                # read space
                status, read_count = readStringFromContent(' ', scope_contents, index)
                if status is False:
                    break # pragma: no cover
                index += read_count
                # read next character to decide if we need to repeat or not
                current_char = scope_contents[index]
                for case in Switch(current_char):
                    if case('a'):
                        # read `and` keyword
                        status, read_count = readStringFromContent('and', scope_contents, index)
                        if status is False:
                            break # pragma: no cover
                        index += read_count
                        # read space
                        status, read_count = readStringFromContent(' ', scope_contents, index)
                        if status is False:
                            break # pragma: no cover
                        index += read_count
                        break
                    if case():
                        reading_conditions = False
                        break
            if status is False:
                break # pragma: no cover
            if should_try_reading_assignment is True:
                # read scope
                Logger.write().debug('Attempting to read content between matching `%s` and `%s`' % ('{', '}'))
                status, assignment_scope, read_count, self.error = readScopeFromContent('{', '}', scope_contents[index:], 0)
                if status is False:
                    break # pragma: no cover
                index += read_count
                status = validateCommaSeparatedValues(assignment_scope)
            break
        return (status, index)

    def validateFor(self, scope_contents, index) -> typing.Tuple[bool, int]:
        status = True
        while status is True:
            # read `for`
            status, read_count = readStringFromContent('for', scope_contents, index)
            index += read_count
            if status is False:
                break # pragma: no cover
            # read whitespace
            status, read_count = readStringFromContent(' ', scope_contents, index)
            index += read_count
            if status is False:
                break # pragma: no cover
            # read the assignment value of `for`
            status, read_count = readStringFromContent('*', scope_contents, index)
            index += read_count
            if status is False:
                status, read_count = readFromCharacterSet(build_setting_char_set, scope_contents, index)
                index += read_count
            if status is False:
                break # pragma: no cover
            # if the next character is a newline, then break, because this is the end of this definition
            newline_index = scope_contents[index:].find('\n')
            is_newline = newline_index == 0
            if is_newline:
                break
            # read whitespace
            status, read_count = readStringFromContent(' ', scope_contents, index)
            index += read_count
            if status is False:
                break # pragma: no cover
            # read the scope
            Logger.write().debug('Attempting to read content between matching `%s` and `%s`' % ('{', '}'))
            status, assignment_scope, read_count, self.error = readScopeFromContent('{', '}', scope_contents[index:], 0)
            if status is False:
                break # pragma: no cover
            index += read_count
            status = validateCommaSeparatedValues(assignment_scope)
            if status is False:
                self.error = 'Error in validating contents of scope ending at line %i, please check to make sure you have no trailing commas' % self.line_number # pragma: no cover
            break
        return (status, index)

    def readSettingScopeContent(self, scope_contents, original_index) -> bool:
        status = True
        offset = original_index
        index = original_index - offset
        should_advance = index < len(scope_contents)
        while status is True and should_advance is True:
            current_char = scope_contents[index]
            Logger.write().debug('New read at (%i) from (%i)' % (index, offset))
            for case in Switch(current_char):
                if case('i'):
                    Logger.write().debug('Attempting to read `if` statement')
                    status, index = self.validateIf(scope_contents, index)
                    break
                if case('f'):
                    Logger.write().debug('Attempting to read `for` statement')
                    status, index = self.validateFor(scope_contents, index)
                    break
                if case():
                    status, index_increase, _, _, _, self.error = readWhitespace(scope_contents, index)
                    if status is False:
                        break # pragma: no cover
                    index = index_increase
                    break
            should_advance = index < len(scope_contents)
        return status

    def validateComment(self) -> bool:
        old_index = self.index
        eol_index = self.contents[self.index:].find('\n')
        if eol_index == -1:
            eol_index = len(self.contents) - old_index
        self.index += eol_index
        self.char_number += self.index - old_index
        return True

    def validateExport(self) -> bool:
        status = True
        while status is True:
            status = self.has_finished_exports is False
            if status is False: # pragma: no cover
                self.error = 'Encountered keyword `%s` after encountering keyword `%s`. Please place the `%s` keyword before the `%s` keyword.' % (Keyword.Constants._export, self.current_keyword, Keyword.Constants._export, self.current_keyword)
                break
            status = self.first_export is True
            if status is False: # pragma: no cover
                self.error = 'Encountered more than one `%s` keyword at line %i, index: %i' % (Keyword.Constants._export, self.line_number, self.char_number)
                break
            status = self.readString(Keyword.Constants._export)
            if status is False:
                break # pragma: no cover
            # check for a white space
            status = self.readString(' ')
            if status is False:
                break # pragma: no cover
            # check for double-quote string
            status = self.readQuotedString()
            self.first_export = False
            break
        return status

    def validateInclude(self) -> bool:
        status = True
        while status is True:
            status = self.has_finished_includes is False
            if status is False: # pragma: no cover
                self.error = 'Encountered `%s` after `%s` keyword at line: %i, index: %i' % (Keyword.Constants._include, self.current_keyword, self.line_number, self.char_number)
                break
            self.current_keyword = Keyword.Constants._include
            self.has_finished_exports = True
            # if the include statement started with `!` or `?`, then read either of
            ## those and advance one character
            current_character = self.contents[self.index]
            is_required_include = current_character == Keyword.Constants._required_include[0]
            is_optional_include = current_character == Keyword.Constants._optional_include[0]
            if is_required_include or is_optional_include:
                self.index += 1
                self.char_number += 1
            # read the "include" keyword
            status = self.readString(Keyword.Constants._include)
            if status is False:
                break # pragma: no cover
            # check for a white space
            status = self.readString(' ')
            if status is False:
                break # pragma: no cover
            # check for double-quote string
            status = self.readQuotedString()
            if status is False:
                break # pragma: no cover
            break
        return status

    def validateSetting(self) -> bool: # pylint: disable=too-many-branches
        status = True
        while status is True:
            self.current_keyword = Keyword.Constants._setting
            self.has_finished_exports = True
            self.has_finished_includes = True
            # read the setting keyword
            status = self.readString(Keyword.Constants._setting)
            if status is False:
                break # pragma: no cover
            # read whitespace
            status = self.readString(' ')
            if status is False:
                break # pragma: no cover
            # read the build setting name
            status = self.readFromCharacterSetUntilCharacter(build_setting_char_set, ' ')
            if status is False:
                break # pragma: no cover
            # read whitespace
            status = self.readString(' ')
            if status is False:
                break # pragma: no cover
            # read optional "use"
            status = self.readString(Keyword.Constants._use, True)
            if status is True:
                status = self.readString(' ')
                if status is False:
                    break # pragma: no cover
                status = self.readFromCharacterSetUntilCharacter(build_setting_char_set, ' ')
                if status is False:
                    break # pragma: no cover
                status = self.readString(' ')
                if status is False:
                    break # pragma: no cover
            # read optional "inherits"
            status = self.readString(Keyword.Constants._inherits, True)
            if status is True:
                status = self.readString(' ')
                if status is False:
                    break # pragma: no cover
            # read scope
            status, scope_contents = self.readScope('{', '}')
            if status is False:
                break # pragma: no cover
            # read contents to ensure it is valid
            status = self.readSettingScopeContent(scope_contents, self.index)
            if status is False:
                break # pragma: no cover
            break
        return status

    def validates(self) -> bool: # pylint: disable=too-many-branches,too-many-statements
        should_advance = len(self.contents) > 0
        status = True
        while should_advance is True and status is True:
            Logger.write().debug('New read at (%i) line: %i, index: %i' % (self.index, self.line_number, self.char_number))
            current_character = self.contents[self.index]
            for case in Switch(current_character):
                if case(Keyword.Constants._comment[0]):
                    Logger.write().debug('Attempting to read comment...')
                    status = self.validateComment()
                    break
                if case(Keyword.Constants._export[0]):
                    Logger.write().debug('Attempting to read export statement...')
                    status = self.validateExport()
                    break
                if case(Keyword.Constants._required_include[0]):
                    pass # pragma: no cover
                if case(Keyword.Constants._optional_include[0]):
                    pass # pragma: no cover
                if case(Keyword.Constants._include[0]):
                    Logger.write().debug('Attempting to read include statement...')
                    status = self.validateInclude()
                    break
                if case(Keyword.Constants._setting[0]):
                    Logger.write().debug('Attempting to read setting statement...')
                    status = self.validateSetting()
                    break
                if case():
                    status = self.readWhitespace(self.contents, self.index)
                    break
            should_advance = self.index < len(self.contents)
        return status
