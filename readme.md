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


### Include Statements
To import values from other xcconfig files, you can use the `include` keyword to have the generated file import another.

Example:

	include "Codesign.xcconfig"

This will cause the following line to be generated at the top of the xcconfig file:

	#include "Codesign.xcconfig"

`pyconfig` supports any number of includes in a configuration file, but they all must be at the top of the file. 


### Build Settings
The function of xcconfig files is to define build settings for an Xcode target when run in a specific build configuration. The `pyconfig` language uses simple and declarative statements to outline what the name of the build setting is and encapsulates the scope of how that variable is set in the file.

	setting OTHER_LDFLAGS {
		...
	}

This syntax can be used to declare any build setting variable, however it must conform to the expected format of build settings names you would have in an xcconfig file. If you are unfamiliar with the rules around the naming conventions in xcconfig files you should refer to [this page](http://pewpewthespells.com/blog/xcconfig_guide.html).


### Variable Substitution
The `pyconfig` language was written with variable subsitution as a first-class feature. By default it will assume you are going to be using different build configurations to denote differences in expected settings. 

Example:

	setting OTHER_LDFLAGS {
		for Debug {
			-lz,
			-framework "Reveal"
		}
		for Release
	}

Will generate the following assignments:

	OTHER_LDFLAGS_Debug = -lz -framework "Reveal"
	OTHER_LDFLAGS_Release = 
	OTHER_LDFLAGS = $(OTHER_LDFLAGS_$(CONFIGURATION))

Since this is a powerful way to conditionally supply specific values to the build system you can extend the substitution behavior by supplying your own variable to subtitute using the `use` keyword.

	setting PRODUCT_NAME use WRAPPER_EXTENSION {
		for app {
			"My App"
		}
		for xctest {
			"Unit Test Bundle"
		}
		for bundle {
			"Generic Bundle"
		}
	}
	
This will cause `pyconfig` to generate the following variables in the xcconfig file:

	PRODUCT_NAME_app = "My App"
	PRODUCT_NAME_xctest = "Unit Test Bundle"
	PRODUCT_NAME_bundle = "Generic Bundle"
	PRODUCT_NAME = $(PRODUCT_NAME_$(WRAPPER_EXTENSION))


### Direct Assignment
The language leverages the `for` keyword used as part of build setting variable substitution in addition with a special keyword  (`*`) that denotes direct assignment of a build setting variable.

Example:

	setting OTHER_CFLAGS {
		for * {
			-Wall,
			-Werror
		}
	} 

This code will produce the following assignment in the generated xcconfig file:

	OTHER_CFLAGS = -Wall -Werror

**Note: When listing values to assign, the `pyconfig` format does NOT support trailing commas on the final list items and may pass linting validation but not generate correctly.**


### Conditional Variables
In additional to variable substitution, xcconfig files have a built-in way to perform assignment based on a condition determined at build-time. The `pyconfig` language supports this through the keyword `if`. 

Example:

	setting OTHER_LDFLAGS {
		if arch=arm* {
			-l"iOSOnlyLibrary"
		}
	}

This will be translated into:

	OTHER_LDFLAGS[arch=arm*] = -l"iOSOnlyLibrary"

Additionally, you can chain multiple conditions together in a single if statement by using the and keyword (`&`):

	setting OTHER_LDFLAGS {
		if arch=i386 & sdk=iphone {
			-l"iOSSimulatorOnlyLibrary"
		}
	}

To get the resulting xcconfig assignment:

	OTHER_LDFLAGS[arch=i386,sdk=iphone] = -l"iOSSimulatorOnlyLibrary"
	
	
### Comments
Documentation is important, so adding comments to explain why and how settings are being composed is vital. The `pyconfig` language has support for Python style comments using the `#` character. These comments can be made in a number of places inside of the configuration file. It is important to note that these comments are not transfered into the xcconfig file as the layout cannot be guaranteed to make sense.

Example:

	# comments can be made before,
	include "Codesign.xcconfig" # inline with,
	# and after include statements
	
	# they can also be made before setting statments
	setting FOO {
		for * {
			"bar"
		}
	}
	# and after, but not inside of the `setting` structure itself. 
	

# Future Plans
I hope to be able to further enhance the capabilities of this tool to make the management of the xcconfig files easy and understandable to newcomers. There are some additional tweaks to the syntax that I would like to add, including the ability to add comments anywhere in the configuration files. If you have an idea as to how to better extend this tool you should open a new issue to discuss it.

