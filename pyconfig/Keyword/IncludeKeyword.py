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

from . import Constants
from . import BaseKeyword

class IncludeKeyword(BaseKeyword.BaseKeyword):

    def __init__(self):
        super(IncludeKeyword, self).__init__()
        self.include_path = None
        self.optional = False

    def __eq__(self, other): # pragma: no cover
        cmp_include = (self.include_path == other.include_path)
        return cmp_include

    def consume(self, parsed_item=None) -> None:
        parsed_item = list() if parsed_item is None else parsed_item
        super(IncludeKeyword, self).consume(parsed_item)
        self.optional = parsed_item[0].startswith('?')
        self.include_path = self.consumePath(Constants._include, parsed_item) # pylint: disable=protected-access

    def serialize(self) -> str:
        serialized_string = ''
        include_type_string = ''
        if self.optional:
            include_type_string += '?'
        if self.include_path:
            serialized_string += '#include'+include_type_string+' "'+self.include_path+'"\n'
        return serialized_string
