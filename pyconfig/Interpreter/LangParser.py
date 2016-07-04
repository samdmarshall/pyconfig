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

import sys
import pyparsing
from .. import Keyword

if sys.version_info >= (3, 0):
    def unichr(c):
        return chr(c)
    def xrange(n):
        return range(n)

unicodePrintables = u''.join(unichr(c) for c in xrange(65536) if not unichr(c).isspace())

_commaSeparatedItem = pyparsing.Combine(                     \
    pyparsing.OneOrMore(                                     \
        pyparsing.Word(unicodePrintables, excludeChars=',')  \
        + pyparsing.Optional(                                \
            pyparsing.Word(" \t")                            \
            + ~pyparsing.Literal(",")                        \
            + ~pyparsing.LineEnd()                           \
        )                                                    \
    )                                                        \
).streamline()

_genericCSVList = pyparsing.delimitedList(                                                  \
    pyparsing.Optional( pyparsing.quotedString.copy() | _commaSeparatedItem, default="")    \
)

def KeywordWithDoubleQuotedParameter(keyword):
    return pyparsing.Group(                   \
        pyparsing.Keyword(keyword)            \
        + pyparsing.dblQuotedString           \
        + pyparsing.Suppress(                 \
            pyparsing.ZeroOrMore(             \
                pyparsing.pythonStyleComment  \
            )                                 \
        )                                     \
    )

# export path of the current pyconfig file
_export = KeywordWithDoubleQuotedParameter(Keyword.Constants._export)

# include "other.xcconfig" # with optional trailing comment
_include = KeywordWithDoubleQuotedParameter(Keyword.Constants._include)

# parsing conditional statement expressions
_conditionalExpr = pyparsing.Group(                             \
    Keyword.Words._conditionalValue                             \
    + pyparsing.Suppress(Keyword.Constants._equals)             \
    + Keyword.Words._conditionalComparator                      \
)

_conditionalName = pyparsing.Group(pyparsing.delimitedList(_conditionalExpr, Keyword.Constants._and))


# group( comma, separated, values, to be used as assignment, for build configurations )
_bc_value = pyparsing.Group(                                                   \
    pyparsing.Optional(                                                        \
        _genericCSVList.ignore(pyparsing.pythonStyleComment)                   \
    )                                                                          \
)

# 
_if_value = pyparsing.Word(pyparsing.alphanums)

#
_if_cond = pyparsing.Keyword(Keyword.Constants._if)     \
+ _conditionalName                                      \
+ pyparsing.Optional(                                   \
    pyparsing.Suppress(Keyword.Constants._openBrace)    \
    + _if_value                                         \
    + pyparsing.Suppress(Keyword.Constants._closeBrace) \
)

#
_for_bc = pyparsing.Keyword(Keyword.Constants._for)           \
+ Keyword.Words._buildConfigurationName                       \
+ pyparsing.Optional(                                         \
    pyparsing.Suppress(Keyword.Constants._openBrace)          \
    + pyparsing.Optional(pyparsing.pythonStyleComment)        \
    + _bc_value                                               \
    + pyparsing.Suppress(Keyword.Constants._closeBrace)       \
)

#
_values = pyparsing.delimitedList(    \
    pyparsing.Group(_for_bc),         \
    pyparsing.Empty()                 \
) ^ pyparsing.delimitedList(          \
    pyparsing.Group(_if_cond),        \
    pyparsing.Empty()                 \
)

#
_setting = pyparsing.Suppress(pyparsing.ZeroOrMore(pyparsing.pythonStyleComment))                 \
+ pyparsing.Group(                                                                                \
    pyparsing.Keyword(Keyword.Constants._setting)                                                 \
    + Keyword.Words._buildSettingName                                                             \
    + pyparsing.Group(                                                                            \
        pyparsing.Optional(pyparsing.Keyword(Keyword.Constants._use)                              \
        + Keyword.Words._buildSettingName)                                                        \
        + pyparsing.Optional(pyparsing.Keyword(Keyword.Constants._inherits))                      \
    )                                                                                             \
    + pyparsing.Suppress(Keyword.Constants._openBrace)                                            \
    + pyparsing.Optional(pyparsing.pythonStyleComment)                                            \
    + pyparsing.Group(_values)                                                                    \
    + pyparsing.Optional(pyparsing.pythonStyleComment)                                            \
    + pyparsing.Suppress(Keyword.Constants._closeBrace)                                           \
)

# composing the configuration file parser
_config = pyparsing.Suppress(                                \
    pyparsing.ZeroOrMore(                                    \
        pyparsing.pythonStyleComment                         \
    )                                                        \
)                                                            \
+ pyparsing.Optional(_export)                                \
+ pyparsing.Optional(                                        \
    pyparsing.Group(                                         \
        pyparsing.delimitedList(_include, pyparsing.Empty()) \
    )                                                        \
)                                                            \
+ pyparsing.Optional(                                        \
    pyparsing.Group(                                         \
        pyparsing.delimitedList(_setting, pyparsing.Empty()) \
    )                                                        \
)
