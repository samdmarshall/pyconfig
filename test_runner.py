#!/usr/bin/python
import os
import sys
import string
import subprocess

def make_call(call_args):
    error = 0
    output = ''
    try:
        output = subprocess.check_output(call_args)
        error = 0
    except subprocess.CalledProcessError as e:
        output = e.output
        error = e.returncode
    return output

test_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
known_tests = [
    (os.path.join(test_directory, 'comments'), 'test'),
    (os.path.join(test_directory, 'conditionals'), 'test'),
    (os.path.join(test_directory, 'direct assignment/specific'), 'test'),
    (os.path.join(test_directory, 'direct assignment/automatic'), 'test'),
    (os.path.join(test_directory, 'export/with-export'), 'defaults'),
    (os.path.join(test_directory, 'export/without-export'), 'test'),
    (os.path.join(test_directory, 'include'), 'test'),
    (os.path.join(test_directory, 'inherits'), 'test'),
    (os.path.join(test_directory, 'variable substitution/with-use'), 'test'),
    (os.path.join(test_directory, 'variable substitution/without-use'), 'test'),
]

# Main
def main():
    for test_pyconfig_path, test_file_name in known_tests:
        test_generated_output = os.path.join(test_pyconfig_path, test_file_name+'.xcconfig')
        test_expected_output = os.path.join(test_pyconfig_path, test_file_name+'_output.xcconfig')
        result = make_call(('pyconfig', test_pyconfig_path))
        with open(test_generated_output, 'r') as generated, open(test_expected_output, 'r') as expected:
            generated_lines = generated.readlines()[2:]
            expected_lines = expected.readlines()[2:]
            test_failure = generated_lines != expected_lines
            generated.close()
            expected.close()
            if test_failure:
                print('Generated: '+str(generated_lines))
                print('Expected: '+str(expected_lines))
                raise Exception('Test Case Failure: '+test_pyconfig_path)

if __name__ == "__main__":
    main()