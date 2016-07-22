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

# this is the base class defintion for all of the pyconfig DSL keywords.
## The majority of the functionality in this class is to say that we need
## to subclass and over-ride the methods.

class BaseKeyword(object):

    def __init__(self):
        self.__parsed_item = None

    def __eq__(self, other): # pylint: disable=no-self-use ; # pragma: no cover
        raise Exception('Please subclass this class and implement this method')

    def serialize(self): # pylint: disable=no-self-use ; # pragma: no cover
        raise Exception('Please subclass this class and implement this method')

    def consumePath(self, constant, parsed_item=list()): # pylint: disable=dangerous-default-value,no-self-use ; # pragma: no cover
        result = None
        if parsed_item[0].endswith(constant):
            result = parsed_item[1][1:-1]
        return result

    def consume(self, parsed_item=list()): # pylint: disable=dangerous-default-value ; # pragma: no cover
        self.__parsed_item = parsed_item

    def deserialize(self, xcconfig_line=''): # pylint: disable=no-self-use ; # pragma: no cover
        _unused = xcconfig_line
        raise Exception('Please subclass this class and implement this method')
