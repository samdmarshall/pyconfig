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

def locateConfigs(fs_path):
    found_configs = list()
    if os.path.isdir(fs_path):
        for root, dirs, files in os.walk(fs_path, followlinks=True):
            for dir_name in dirs:
                relative_path = os.path.join(root, dir_name)
                found_configs.extend(locateConfigs(relative_path))
            for file_name in files:
                relative_path = os.path.join(root, file_name)
                full_path = os.path.normpath(os.path.join(os.getcwd(), relative_path))
                name, extension = os.path.splitext(file_name)
                if extension == '.pyconfig':
                    found_configs.append(full_path)
    else:
        full_path = os.path.normpath(os.path.join(os.getcwd(), fs_path))
        found_configs.append(full_path)
    return found_configs

# Main
def main():
    found_tests = locateConfigs(sys.argv[1])
    for test_pyconfig_path in found_tests:
        test_directory = os.path.dirname(test_pyconfig_path)
        name, extension = os.path.splitext(test_pyconfig_path)
        test_generated_output = os.path.join(test_directory, name+'.xcconfig')
        test_expected_output = os.path.join(test_directory, name+'_output.xcconfig')
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