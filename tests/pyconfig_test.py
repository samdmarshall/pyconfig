import os
import sys
import string
import unittest
import pyconfig

test_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')

def LoadTestDirectoryAndTestWithName(test, test_pyconfig_path_sub, test_file_name):
    test_pyconfig_path = os.path.join(test_directory, test_pyconfig_path_sub)
    test_generated_output = os.path.join(test_pyconfig_path, test_file_name+'.xcconfig')
    test_expected_output = os.path.join(test_pyconfig_path, test_file_name+'_output.xcconfig')
    pyconfig.main(['-q', test_pyconfig_path])
    with open(test_generated_output, 'r') as generated, open(test_expected_output, 'r') as expected:
        generated_lines = generated.readlines()[2:]
        expected_lines = expected.readlines()[2:]
        generated.close()
        expected.close()
        if generated_lines != expected_lines:
            print('Generated: '+str(generated_lines))
            print('Expected: '+str(expected_lines))
            test.assertEqual(generated_lines, expected_lines)

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
        
    def test_export_without_keyword(self):
        LoadTestDirectoryAndTestWithName(self, 'export/without-export', 'test')
        
    def test_include(self):
        LoadTestDirectoryAndTestWithName(self, 'include', 'test')
        
    def test_inherits(self):
        LoadTestDirectoryAndTestWithName(self, 'inherits', 'test')
        
    def test_variable_substitution_with_use(self):
        LoadTestDirectoryAndTestWithName(self, 'variable substitution/with-use', 'test')
        
    def test_variable_substitution_without_use(self):
        LoadTestDirectoryAndTestWithName(self, 'variable substitution/without-use', 'test')

if __name__ == '__main__':
    unittest.main()