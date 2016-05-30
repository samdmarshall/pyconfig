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

from pyconfig.version import __version__ as PYCONFIG_VERSION
import os
import argparse
import interpreter
import serializer

def openOutputFileToWrite(input_string):
    file_path = os.path.expanduser(input_string)
    parent_path = os.path.dirname(file_path)
    if os.path.exists(parent_path) == False:
        os.makedirs(parent_path)
    return open(file_path, 'w')

# Main
def main():
    parser = argparse.ArgumentParser(description='pyconfig is a tool to generate xcconfig files from a simple DSL')
    parser.add_argument(
        'file', 
        help='Path to the pyconfig file to use to generate a xcconfig file',
        type=argparse.FileType('r')
    )
    parser.add_argument(
        '-o', '--output', 
        metavar='file', 
        help='Path to output xcconfig file to write', 
        type=openOutputFileToWrite
    )
    parser.add_argument(
        '-l', '--lint', 
        help='Validate the syntax of a pyconfig file', 
        action='store_true'
    )
    parser.add_argument(
        '-s', '--scheme', 
        metavar='name', 
        help='Optional argument to supply the scheme name'
    )
    parser.add_argument(
        '-v', '--version',
        help='Displays the version information',
        action='version',
        version=PYCONFIG_VERSION
    )
    args = parser.parse_args()
    	
    pyconfig_contents = args.file.read()
    
    parsed_contents = interpreter.parse(args.lint, pyconfig_contents)
    
    if args.lint == False:
        serializer.writeFile(parsed_contents, args.output, args.scheme)
    	
    args.file.close()
    	
    if args.output != None:
        args.output.close()

if __name__ == "__main__":
    main()
