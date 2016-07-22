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

import os
import sys
import string
import itertools
import unittest
import pyconfig
import pyconfig.Deserializer.xcconfig

test_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')

def LoadTestDirectoryAndTestWithName(test, test_pyconfig_path_sub, test_file_name, additional_flags=[], override=False):
    test_pyconfig_path = os.path.join(test_directory, test_pyconfig_path_sub)
    test_generated_output = os.path.join(test_pyconfig_path, test_file_name+'.xcconfig')
    test_expected_output = os.path.join(test_pyconfig_path, test_file_name+'_output.xcconfig')
    args = ['--quiet']
    if not override:
        args.append(test_pyconfig_path)
    args.extend(additional_flags)
    pyconfig.main(args)
    generated_output = pyconfig.Deserializer.xcconfig.xcconfig(test_generated_output)
    expected_output = pyconfig.Deserializer.xcconfig.xcconfig(test_expected_output)
    for generated, expected in list(zip(generated_output.lines, expected_output.lines)):
        test.assertEqual(generated, expected)

class pyconfigTestCases(unittest.TestCase):

    def test_comments(self):
        LoadTestDirectoryAndTestWithName(self, 'comments', 'test')
        
    def test_conditionals(self):
        LoadTestDirectoryAndTestWithName(self, 'conditionals', 'test')
       
    def test_direct_assignment_specific(self):
        LoadTestDirectoryAndTestWithName(self, 'direct assignment/specific', 'test')
        
    def test_direct_assignment_automatic(self):
        LoadTestDirectoryAndTestWithName(self, 'direct assignment/automatic', 'test')
        
    def test_export_with_keyword(self):
        LoadTestDirectoryAndTestWithName(self, 'export/with-export', 'defaults')
    
    def test_export_with_keyword_and_include(self):
        LoadTestDirectoryAndTestWithName(self, 'export/with-export-and-include', 'defaults')
        
    def test_export_without_keyword(self):
        LoadTestDirectoryAndTestWithName(self, 'export/without-export', 'test')

    def test_include_optional(self):
        LoadTestDirectoryAndTestWithName(self, 'include/optional', 'test')

    def test_include_required(self):
        LoadTestDirectoryAndTestWithName(self, 'include/required', 'test')

    def test_include_legacy(self):
        LoadTestDirectoryAndTestWithName(self, 'include/legacy', 'test')

    def test_include_missing_required(self):
        LoadTestDirectoryAndTestWithName(self, 'include/missing required', 'test')
        
    def test_inherits(self):
        LoadTestDirectoryAndTestWithName(self, 'inherits', 'test')
        
    def test_variable_substitution_with_use(self):
        LoadTestDirectoryAndTestWithName(self, 'variable substitution/with-use', 'test')
        
    def test_variable_substitution_without_use(self):
        LoadTestDirectoryAndTestWithName(self, 'variable substitution/without-use', 'test')
    
    def test_search_direct_file(self):
        test_pyconfig_path_sub = 'search/direct-file'
        test_pyconfig_path = os.path.join(test_directory, test_pyconfig_path_sub)
        direct_file_path = os.path.join(test_pyconfig_path, 'test.pyconfig')
        LoadTestDirectoryAndTestWithName(self, test_pyconfig_path_sub, 'test', [direct_file_path], True)
    
    def test_search_directory_path(self):
        test_pyconfig_path_sub = 'search/directory'
        test_pyconfig_path = os.path.join(test_directory, test_pyconfig_path_sub)
        LoadTestDirectoryAndTestWithName(self, test_pyconfig_path, 'test-dir/test', [test_pyconfig_path], True)
    
    def test_duplicate_definition_single_file(self):
        LoadTestDirectoryAndTestWithName(self, 'duplicate definitions/single file', 'test')
    
    def test_duplicate_definition_multiple_files(self):
        test_pyconfig_path_sub = 'duplicate definitions/multiple files'
        test_pyconfig_path = os.path.join(test_directory, test_pyconfig_path_sub)
        LoadTestDirectoryAndTestWithName(self, test_pyconfig_path, 'test', [test_pyconfig_path], True)
    
    def test_flags_scheme_name(self):
        LoadTestDirectoryAndTestWithName(self, 'flags/scheme name', 'test', ['--scheme', 'MyAppDebug'])

if __name__ == '__main__':
    unittest.main()