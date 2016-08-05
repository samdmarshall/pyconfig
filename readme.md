pyconfig 
========

[![Code Climate](https://img.shields.io/codeclimate/github/samdmarshall/pyconfig.svg)](https://codeclimate.com/github/samdmarshall/pyconfig)
[![Test Coverage](https://img.shields.io/codeclimate/coverage/github/samdmarshall/pyconfig.svg)](https://codeclimate.com/github/samdmarshall/pyconfig/coverage)
[![CircleCI branch](https://img.shields.io/circleci/project/samdmarshall/pyconfig/develop.svg)](https://circleci.com/gh/samdmarshall/pyconfig/tree/develop)
[![Dependency Status](https://dependencyci.com/github/samdmarshall/pyconfig/badge)](https://dependencyci.com/github/samdmarshall/pyconfig)

**pyconfig** is a tool that allows you to write the contents of your [`.xcconfig` files](http://pewpewthespells.com/blog/xcconfig_guide.html) in a simple and more expressive language and have them be generated prior to building a target in Xcode. 


## Contributing and Code of Conduct [![License](https://img.shields.io/badge/License-3--Clause%20BSD-blue.svg)](./LICENSE)
This project and related material has a Code of Conduct that is listed in the [contributing.md](./contributing.md) file. This must be read and adhered to when interacting with this project. Additionally this code is released under a 3-clause BSD license that you can read [here](./LICENSE).


## Requirements ![Python](https://img.shields.io/badge/Python2-2.7.10-brightgreen.svg) ![Python](https://img.shields.io/badge/Python3-3.5.0-brightgreen.svg)
This tool is built and tested against Python 2.7.10 and 3.5.0. 

   Module | Version
----------|-----------
pyparsing | >=2.0.3

Note: All of these modules come as part of the system Python installation for OS X (which is 2.7.10 as of 10.11.5), but you will have to install them yourself if necessary on other systems. These modules can be accquired through `pip install`.


## Installation [![homebrew](https://img.shields.io/badge/homebrew-v1.1-brightgreen.svg)](https://github.com/samdmarshall/homebrew-formulae) [![homebrew](https://img.shields.io/badge/homebrew-HEAD-orange.svg)](https://github.com/samdmarshall/homebrew-formulae)
Via [homebrew](http://brew.sh):

	$ brew update
	$ brew tap samdmarshall/formulae
	$ brew install samdmarshall/formulae/pyconfig

To install the tool from the repo, clone from Github then run the respective `make` command for the desired version.

### Installing for Python 2

	$ make build2

### Installing for Python 3

	$ make build3


## Usage
To use **pyconfig** to generate an `.xcconfig` file, you will have to pass it a path as input:

	$ pyconfig <file path to the configuration file or directory>

There are a number of flags that can be passed to modify the behavior of **pyconfig**:

   Flags | Usage
-------------------|-----------------------------------------------------------
`--version`        | Displays the version of **pyconfig** and exits
`--scheme <name>`  | Add additional variable defined as `SCHEME_NAME = <name>`
`--no-analyze`     | Skip the analysis step of processing the `.pyconfig` files
`--dry-run`        | Do not write any output files
`--quiet`          | Silences all logging output
`--verbose`        | Logs additional information
`--scm-info <type>`| Write an additional `.xcconfig` file that contains information from the source control management software for versioning


## Syntax
One of the greatest benefits to using `.xcconfig` files are part of your build process is that they make the configuration of build settings be represented inside of a human-readable plain-text file rather than being part of the Xcode project's `.pbxproj` file. For the documentation on the DSL syntax please refer to the [wiki](../../wiki), which is located at the docs directory of this repo.

# Future Plans
I hope to be able to further enhance the capabilities of this tool to make the management of the `.xcconfig` files easy and understandable to newcomers. If you have an idea as to how to better extend this tool you should open a new issue to discuss it.

