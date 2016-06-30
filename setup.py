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
            'pyconfig/Helpers',
            'pyconfig/Keyword',
        ],
        entry_points = { 'console_scripts': ['pyconfig = pyconfig:main'] },
        test_suite = 'tests.pyconfig_test',
        zip_safe = False,
        **install_requires_dict
    )
except ImportError as e:
    raise e
