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

import sys
import argparse
from .version         import __version__ as PYCONFIG_VERSION
from .Interpreter     import Consumer
from .Graph           import Searcher
from .Graph           import Grapher
from .Helpers.Logger  import Logger
from .Serializer      import Serializer
from .Analyzer        import Engine

# Main
def main(argv=sys.argv[1:]):
    # setup the argument parsing
    parser = argparse.ArgumentParser(description='pyconfig is a tool to generate xcconfig files from a simple DSL')
    parser.add_argument(
        '--version',
        help='Displays the version information',
        action='version',
        version=PYCONFIG_VERSION
    )
    parser.add_argument(
        'file',
        metavar='<path>',
        help='Path to the pyconfig file to use to generate a xcconfig file',
    )
    parser.add_argument(
        '--scheme',
        metavar='name',
        action='store',
        help='Optional argument to supply the scheme name'
    )
    parser.add_argument(
        '--no-analyze',
        help='Skips the step of analyzing the pyconfig files before writing to disk',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--dry-run',
        help='Runs normally except will not write out a file',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--scm-info',
        help='Generate an additional xcconfig that contains metadata about the current source control environment',
        choices=['detect', 'git', 'svn', 'hg'],
        action='store'
    )
    parser.add_argument(
        '--quiet',
        help='Silences all logging output',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--verbose',
        help='Adds verbosity to logging output',
        default=False,
        action='store_true'
    )
    args = parser.parse_args(argv)

    # perform the logging modifications before we do any other operations
    Logger.isVerbose(args.verbose)
    Logger.isSilent(args.quiet)

    # take the input path and search for pyconfig files, returning an array of
    ## file paths.
    found_pyconfig_files = Searcher.locateConfigs(args.file)

    # once we have the array of files, parse each file and attach the results
    ## to a graph node object. Return all of the created nodes as a set.
    parsed_configs = Consumer.CreateGraphNodes(found_pyconfig_files)

    # after all the nodes have been constructed, the file paths that each node
    ## has should be resolved to the full file path. This is done as a for loop
    ## instead of a map() call to be compatible with Python 3.
    for node in parsed_configs:
        node.resolvePaths(parsed_configs)
    # once the file paths have been resolved, then transform the set of files into
    ## an array that is ordered from root config to highest level config. Since the
    ## map of config files has many roots and many children, this will traverse one
    ## branch then move onto the next root and navigate to a child, and repeat this
    ## until it has consumed all of the nodes.
    mapped_nodes = Grapher.TraverseNodes(parsed_configs)

    # initialize the analyzer engine, there is only one instance of this across all
    ## of the files used in this pass. The intended behavior here is to raise any
    ## issues that could impact the outcome of a particular build.
    analyzer_engine = Engine.Engine()

    # detect if there was an option to generate data from the SCM used for this repo
    ## if there is, then it should be inserted at the head of the list of files and 
    ## be written first. 
    
    # TODO: I will have to think about how to filter and detect for use of the SCM 
    ## variables so that the include can automatically be added during serialization.
    if args.scm_info is not None:
        Logger.write().info('SCM method: %s' % args.scm_info)

    # iterate through the ordered nodes
    for current_config in mapped_nodes:
        # unless the `--no-analyze` flag was passed, the analysis engine should be
        ## used to process each configuration.
        if not args.no_analyze:
            analyzer_engine.process(current_config)
        # unless the `--dry-run` flag was passed, each configuration file should be
        ## serialized to disk as an xcconfig file.
        if not args.dry_run:
            Serializer.writeFile(current_config, args.scheme)

if __name__ == "__main__": # pragma: no cover
    main()
