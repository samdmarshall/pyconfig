# DSL Documentation

This is documentation for the DSL language that `pyconfig` uses. 


## Keywords

There are a number of keywords that are reserved for the language to use, they are:

* `include`
* `setting`
* `for`
* `if`
* `use`
* `and`
* `inherits`

Additionally it uses the open and close curley braces (`{` and `}`, respectively) to encapsulate scope of structures.


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


### Inheriting Values
Additionally there is the option to inherit the values of the previous level that set this variable. To do this, append the `inherits` keyword to the end of the `setting` line of the build setting assignment.

Example:

	setting OTHER_CFLAGS inherits {
		for * {
			-Wall
		}
	}

Will generate a line in the xcconfig file that reads:

	OTHER_CFLAGS = $(inherited) -Wall

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

Additionally, you can chain multiple conditions together in a single if statement by using the `and` keyword:

	setting OTHER_LDFLAGS {
		if arch=i386 and sdk=iphone {
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