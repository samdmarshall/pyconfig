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

module_dependencies = []
module_version = '1.0.2'
try:
    import sys
    if not sys.version_info > (2, 7):
        print('This software requires that you be running at least Python 2.7')
        sys.exit()
    else:
        install_dependency_list = [
            'argparse', 
            'sys', 
            'os', 
            'pyparsing', 
            'logging',
            're'
        ]
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
            'pyconfig/Analyzer',
            'pyconfig/Deserializer',
            'pyconfig/Graph',
            'pyconfig/Helpers',
            'pyconfig/Interpreter',
            'pyconfig/Keyword',
            'pyconfig/Serializer',
            'pyconfig/Settings',
        ],
        package_data = {
            'pyconfig/Settings': ['defaults.xcconfig', 'runtime.xcconfig']
        },
        entry_points = { 
            'console_scripts': [ 'pyconfig = pyconfig:main' ] 
        },
        test_suite = 'tests.pyconfig_test',
        zip_safe = False,
        **install_requires_dict
    )
except ImportError as e:
    raise e
