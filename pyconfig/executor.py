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

import word
import pyparsing
import keyword

# parsing conditional statement expressions
_conditionalExpr = pyparsing.Group(
    word._conditionalValue 
    + pyparsing.Suppress(keyword._equals) 
    + word._conditionalComparator
)
_conditionalName = pyparsing.Group(pyparsing.delimitedList(_conditionalExpr, keyword._and))

# include "other.xcconfig" # with optional trailing comment
_include = pyparsing.Suppress(keyword._include) + pyparsing.dblQuotedString + pyparsing.Suppress(pyparsing.ZeroOrMore(pyparsing.pythonStyleComment))

# group( comma, separated, values, to be used as assignment, for build configurations )
_bc_value = pyparsing.Group(pyparsing.Optional(pyparsing.commaSeparatedList.ignore(pyparsing.pythonStyleComment)))

# 
_if_value = pyparsing.Word(pyparsing.alphanums)

#
_if_cond = pyparsing.Keyword(keyword._if) + _conditionalName + pyparsing.Optional(pyparsing.Suppress(keyword._openBrace) + _if_value + pyparsing.Suppress(keyword._closeBrace))

#
_for_bc = pyparsing.Keyword(keyword._for) + word._buildConfigurationName + pyparsing.Optional(pyparsing.Suppress(keyword._openBrace) 
    + pyparsing.Optional(pyparsing.pythonStyleComment)
    + _bc_value 
    + pyparsing.Suppress(keyword._closeBrace))

#
_values = pyparsing.delimitedList(pyparsing.Group(_for_bc), pyparsing.Empty()) ^ pyparsing.delimitedList(pyparsing.Group(_if_cond), pyparsing.Empty())

#
_setting = pyparsing.Group(pyparsing.Suppress(pyparsing.ZeroOrMore(pyparsing.pythonStyleComment)) + pyparsing.Suppress(keyword._setting)
    + word._buildSettingName 
    + pyparsing.Group(pyparsing.Optional(pyparsing.Keyword(keyword._use) + word._buildSettingName) + pyparsing.Optional(pyparsing.Keyword(keyword._inherits)))
    + pyparsing.Suppress(keyword._openBrace) + pyparsing.Optional(pyparsing.pythonStyleComment)
    + pyparsing.Group(_values) + pyparsing.Optional(pyparsing.pythonStyleComment)
    + pyparsing.Suppress(keyword._closeBrace))

#
_config = pyparsing.Suppress(pyparsing.ZeroOrMore(pyparsing.pythonStyleComment)) + pyparsing.Optional(pyparsing.delimitedList(_include, pyparsing.Empty())) + pyparsing.delimitedList(_setting, pyparsing.Empty())