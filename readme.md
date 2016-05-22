# pyconfig
pyconfig is a tool that allows you to write the contents of your xcconfig files in a simple and more expressive language and have them be generated prior to building a target in Xcode. 


## Contributing and Code of Conduct
This project and related material has a Code of Conduct that is listed in the [contributing.md](./contributing.md) file. This must be read and adhered to when interacting with this project. Additionally this code is released under a 3-clause BSD license that you can read [here](./LICENSE).


## Requirements
This script was written against system Python (2.7.10) on OS X 10.11.4. It uses two modules: `argparse` and `pyparsing`. Both of these come as part of the system Python installation for OS X, but you will have to install them yourself if necessary on other systems. Both of these modules can be accquired through `pip install`.


## Installation
To install this tool, you must download the `pyconfig.py` script file in this repo. This can be done by cloning the repo from GitHub or by downloading the script file directly. Since this is not a packaged tool that can be installed via `pip` or `brew`, it is recommended that you clone the repo to download the script and keep it up to date.


## Usage
To use `pyconfig` to generate an xcconfig file, you will have to pass it an input and the `--output` flag:

	$ ./pyconfig.py <file path to the configuration file> --output <file path to write the xcconfig file>

You must create the intermediary directories if they do not already exist for the xcconfig file to be written to disk.

You can also use `pyconfig` to perform syntax validation on the configuration file by passing the `--lint` flag:

	$ ./pyconfig.py <file path to the configuration file> --lint

Doing this should raise any of the major syntax errors and print out nothing if it passed successfully.

There is an additional flag that allows you to pass in an additional variable at execution of the script to represent the name of the scheme you are running. This feature exists to allow the generation of the xcconfig files to be added as a pre-build script phase to an Xcode scheme to re-define the build settings as necessary.

	$ ./pyconfig.py <file path to the configuration file> --output <file path to write the xcconfig file> --scheme <name of scheme>

When using the `--scheme` flag, a new variable will be written to the generated xcconfig file as:

	SCHEME_NAME = <value that was passed in via the flag>


## Syntax
One of the greatest benefits to using xcconfig files are part of your build process is that they make the configuration of build settings be represented inside of a human-readable plain-text file rather than being part of the Xcode project's `pbxproj` file. The following sections detail the major aspects of the `pyconfig` language structures.

For the documentation on the DSL syntax please refer to the [documentation](./documentation.md) file.

# Future Plans
I hope to be able to further enhance the capabilities of this tool to make the management of the xcconfig files easy and understandable to newcomers. There are some additional tweaks to the syntax that I would like to add, including the ability to add comments anywhere in the configuration files. If you have an idea as to how to better extend this tool you should open a new issue to discuss it.

