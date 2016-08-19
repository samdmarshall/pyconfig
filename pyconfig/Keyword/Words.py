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

import pyparsing
from . import Constants

def addLocnToTokens(string_value, location, token):
    token['locn'] = location
    substring = string_value[:location]
    token['line'] = substring.count('\n') + 1

_include = pyparsing.Word('?!', Constants._include) # pylint: disable=protected-access

# build setting Word definition
_settingBody = pyparsing.alphanums+'_'
_settingStart = pyparsing.alphas
_buildSettingName = pyparsing.Word(_settingStart, _settingBody)

_buildSettingName.setParseAction(addLocnToTokens)

#
_directAssignment = pyparsing.Word(Constants._specialCase) # pylint: disable=protected-access

_directAssignment.setParseAction(addLocnToTokens)

# build configuration Word definition
_configutationWord = pyparsing.alphanums+'_'
_buildConfigurationName = pyparsing.Word(_configutationWord) ^ _directAssignment

_buildConfigurationName.setParseAction(addLocnToTokens)

# conditional value
_conditionalValue = pyparsing.Word(pyparsing.alphas)

_conditionalValue.setParseAction(addLocnToTokens)

# conditional comparator
_conditionalComparator = pyparsing.Word(pyparsing.alphanums+'*\"\'_-')

_conditionalComparator.setParseAction(addLocnToTokens)
