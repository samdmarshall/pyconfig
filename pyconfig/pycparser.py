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
from . import pycword
from . import pyckeyword

# export path of the current pyconfig file
_export = pyparsing.Group(                \
    pyparsing.Keyword(pyckeyword._export) \
    + pyparsing.dblQuotedString           \
    + pyparsing.Suppress(                 \
        pyparsing.ZeroOrMore(             \
            pyparsing.pythonStyleComment  \
        )                                 \
    )                                     \
)

# include "other.xcconfig" # with optional trailing comment
_include = pyparsing.Group(                                \
    pyparsing.Keyword(pyckeyword._include)                 \
    + pyparsing.dblQuotedString                            \
    + pyparsing.Suppress(                                  \
        pyparsing.ZeroOrMore(pyparsing.pythonStyleComment) \
    )                                                      \
)

# parsing conditional statement expressions
_conditionalExpr = pyparsing.Group(                       \
    pycword._conditionalValue                             \
    + pyparsing.Suppress(pyckeyword._equals)              \
    + pycword._conditionalComparator                      \
)

_conditionalName = pyparsing.Group(pyparsing.delimitedList(_conditionalExpr, pyckeyword._and))


# group( comma, separated, values, to be used as assignment, for build configurations )
_bc_value = pyparsing.Group(                                                                \
    pyparsing.Optional(pyparsing.commaSeparatedList.ignore(pyparsing.pythonStyleComment))   \
)

# 
_if_value = pyparsing.Word(pyparsing.alphanums)

#
_if_cond = pyparsing.Keyword(pyckeyword._if)         \
+ _conditionalName                                   \
+ pyparsing.Optional(                                \
    pyparsing.Suppress(pyckeyword._openBrace)        \
    + _if_value                                      \
    + pyparsing.Suppress(pyckeyword._closeBrace)     \
)

#
_for_bc = pyparsing.Keyword(pyckeyword._for)                  \
+ pycword._buildConfigurationName                             \
+ pyparsing.Optional(                                         \
    pyparsing.Suppress(pyckeyword._openBrace)                 \
    + pyparsing.Optional(pyparsing.pythonStyleComment)        \
    + _bc_value                                               \
    + pyparsing.Suppress(pyckeyword._closeBrace)              \
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
_setting = pyparsing.Suppress(pyparsing.ZeroOrMore(pyparsing.pythonStyleComment))            \
+ pyparsing.Group(                                                                           \
    pyparsing.Keyword(pyckeyword._setting)                                                   \
    + pycword._buildSettingName                                                              \
    + pyparsing.Group(                                                                       \
        pyparsing.Optional(pyparsing.Keyword(pyckeyword._use) + pycword._buildSettingName)   \
        + pyparsing.Optional(pyparsing.Keyword(pyckeyword._inherits))                        \
    )                                                                                        \
    + pyparsing.Suppress(pyckeyword._openBrace)                                              \
    + pyparsing.Optional(pyparsing.pythonStyleComment)                                       \
    + pyparsing.Group(_values)                                                               \
    + pyparsing.Optional(pyparsing.pythonStyleComment)                                       \
    + pyparsing.Suppress(pyckeyword._closeBrace)                                             \
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
+ pyparsing.Group(                                           \
    pyparsing.delimitedList(_setting, pyparsing.Empty())     \
)
