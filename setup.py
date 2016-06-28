module_dependencies = []
module_version = '1.0.2'
try:
    import sys
    if not sys.version_info > (2, 7):
        print('This software requires that you be running at least Python 2.7')
        sys.exit()
    else:
        install_dependency_list = ['argparse', 'sys', 'os', 'pyparsing', 'logging']
        found_modules = {}
        for dependency in install_dependency_list:
            try:
                found_modules[dependency] = __import__(dependency)
            except ImportError:
                module_dependencies.append(dependency)
except ImportError as e:
    raise e
 
install_requires_dict = {'install_requires': module_dependencies}

try:
    import os
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

    install_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(install_path)
    commit_hash = make_call(('git', 'rev-parse', '--short', 'HEAD')).decode('utf-8').strip('\n')
    remote_origin = make_call(('git', 'ls-remote', '--get-url')).decode('utf-8').strip('\n')
    if len(commit_hash) > 0 and len(remote_origin) > 0:
        versions_path = os.path.join(install_path, 'pyconfig/version.py')
        fd = open(versions_path, 'w')
        fd.write('__version__ = "'+module_version+' ('+remote_origin+' @ '+commit_hash+')"')
        fd.close()
except ImportError as e:
    raise e
 
try:
    from setuptools import setup

    setup(
        name = 'pyconfig',
        version = module_version,
        description = 'Tool for generating xcconfig files',
        url = 'https://github.com/samdmarshall/pyconfig',
        author = 'Samantha Marshall',
        author_email = 'hello@pewpewthespells.com',
        license = 'BSD 3-Clause',
        packages = [ 
            'pyconfig',
            'pyconfig/Helpers'
        ],
        entry_points = { 'console_scripts': ['pyconfig = pyconfig:main'] },
        test_suite = 'tests.pyconfig_test',
        zip_safe = False,
        **install_requires_dict
    )
except ImportError as e:
    raise e
