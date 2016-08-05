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
from ..Graph          import Searcher
from ..Interpreter    import Consumer
from ..Helpers.Switch import Switch
from ..Helpers        import Executor
from ..Helpers.Logger import Logger

SCM_DEFAULT_EXPORT_NAME = 'scm-version'
SCM_NODE_NAME = 'SCM Information'

def DetectError(output, error, detect_mode, error_string):
    should_append_data = True
    if error != 0 and detect_mode is False: # pragma: no cover
        should_append_data = False
        Logger.write().error(error_string % output)
    return should_append_data

def InfoFromGit(detect_mode=False):
    content_string = ''
    should_append_data = True

    output, error = Executor.Invoke(('git', 'symbolic-ref', '--short', 'HEAD'))
    should_append_data = DetectError(output, error, detect_mode, 'Error fetching branch name: "%s"')
    branch_name = output.strip('\n')

    output, error = Executor.Invoke(('git', 'rev-parse', '--short', branch_name))
    should_append_data = DetectError(output, error, detect_mode, 'Error fetching commit hash: "%s"')
    commit_hash = output.strip('\n')

    if should_append_data is True:
        content_string += 'setting PYCONIFG_GIT_BRANCH_NAME {\n'\
                          '    for * {\n'\
                          '        '+branch_name+'\n'\
                          '    }\n'\
                          '}\n'\
                          'setting PYCONFIG_GIT_COMMIT_HASH {\n'\
                          '    for * {\n'\
                          '        '+commit_hash+'\n'\
                          '    }\n'\
                          '}\n'
    return content_string

def InfoFromSVN(detect_mode=False):
    content_string = ''
    should_append_data = True

    working_dir = os.getcwd()
    svn_root_dir = Searcher.LocateParentWithPath(working_dir, '.svn')

    if svn_root_dir is not None:
        os.chdir(svn_root_dir)

        output, error = Executor.Invoke(('svnversion'))
        should_append_data = DetectError(output, error, detect_mode, 'Error fetching svn revision: "%s"')
        revision_number = output.strip('\n')

        os.chdir(working_dir)

        if should_append_data is True:
            content_string += 'setting PYCONFIG_SVN_REVISION {\n'\
                              '    for * {\n'\
                              '        '+revision_number+'\n'\
                              '    }\n'\
                              '}\n'
    return content_string

def InfoFromMercurial(detect_mode=False):
    content_string = ''

    content_string = ''
    should_append_data = True

    output, error = Executor.Invoke(('hg', 'identify', '--branch'))
    should_append_data = DetectError(output, error, detect_mode, 'Error fetching branch name: "%s"')
    branch_name = output.strip('\n')

    output, error = Executor.Invoke(('hg', 'identify', '--id'))
    should_append_data = DetectError(output, error, detect_mode, 'Error fetching revision number: "%s"')
    commit_hash = output.strip('\n')

    if should_append_data is True:
        content_string += 'setting PYCONIFG_HG_BRANCH_NAME {\n'\
                          '    for * {\n'\
                          '        '+branch_name+'\n'\
                          '    }\n'\
                          '}\n'\
                          'setting PYCONFIG_HG_REVISION {\n'\
                          '    for * {\n'\
                          '        '+commit_hash+'\n'\
                          '    }\n'\
                          '}\n'
    return content_string

def GenerateSCMContents(scm_type='detect'):
    scm_content_string = ''
    detect_mode = False
    for case in Switch(scm_type):
        if case('detect'):
            detect_mode = True
        if case('git'):
            scm_content_string += InfoFromGit(detect_mode)
            if not detect_mode:
                break
        if case('svn'):
            scm_content_string += InfoFromSVN(detect_mode)
            if not detect_mode:
                break
        if case('hg'):
            scm_content_string += InfoFromMercurial(detect_mode)
            if not detect_mode:
                break
        if case():
            break
    return scm_content_string

def CreateNodeForSCM(scm_type='detect', file_path=''):
    working_dir = Searcher.locateWorkingDirectoryForPath(file_path)

    original_dir = os.getcwd()
    os.chdir(working_dir)

    scm_contents = 'export "'+SCM_DEFAULT_EXPORT_NAME+'.xcconfig"\n'
    scm_contents += GenerateSCMContents(scm_type)

    os.chdir(original_dir)

    scm_output_path = os.path.join(working_dir, SCM_NODE_NAME)

    node = Consumer.CreateNodeFromString(scm_output_path, scm_contents)

    return node
