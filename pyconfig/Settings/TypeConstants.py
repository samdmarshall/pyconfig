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

# this is a lookup table that defines the type that should be assigned to each of the
## known build settings. This is currently only used to eliminate variables from the
## pool that is assumed to be "undefined" by the user. This should eventually be used
## to validate the contents of assignment and warn when something is being assigned
## that might cause undesird behavior.
ConstantLookupTable = {
    'ACTION': str,
    'ADDITIONAL_SDKS': str,
    'ALTERNATE_GROUP': str,
    'ALTERNATE_MODE': str,
    'ALTERNATE_OWNER': str,
    'ALTERNATE_PERMISSIONS_FILES': list,
    'ALWAYS_SEARCH_USER_PATHS': bool,
    'APPLE_INTERNAL_DEVELOPER_DIR': str,
    'APPLE_INTERNAL_DIR': str,
    'APPLE_INTERNAL_DOCUMENTATION_DIR': str,
    'APPLE_INTERNAL_LIBRARY_DIR': str,
    'APPLE_INTERNAL_TOOLS': str,
    'APPLICATION_EXTENSION_API_ONLY': bool,
    'APPLY_RULES_IN_COPY_FILES': bool,
    'ARCHS': str,
    'ARCHS_STANDARD': list,
    'ARCHS_STANDARD_32_64_BIT': list,
    'ARCHS_STANDARD_32_BIT': list,
    'ARCHS_STANDARD_64_BIT': list,
    'ARCHS_STANDARD_INCLUDING_64_BIT': list,
    'ARCHS_UNIVERSAL_IPHONE_OS': list,
    'ASSETCATALOG_COMPILER_APPICON_NAME': str,
    'ASSETCATALOG_COMPILER_LAUNCHIMAGE_NAME': str,
    'ASSETCATALOG_NOTICES': bool,
    'ASSETCATALOG_OTHER_FLAGS': list,
    'ASSETCATALOG_WARNINGS': bool,
    'AVAILABLE_PLATFORMS': str,
    'BUILD_COMPONENTS': str,
    'BUILD_DIR': str,
    'BUILD_ROOT': str,
    'BUILD_STYLE': str,
    'BUILD_VARIANTS': str,
    'BUILT_PRODUCTS_DIR': str,
    'BUNDLE_LOADER': str,
    'CACHE_ROOT': str,
    'CCHROOT': str,
    'CHMOD': str,
    'CHOWN': str,
    'CLANG_ALLOW_NON_MODULAR_INCLUDES_IN_FRAMEWORK_MODULES': bool,
    'CLANG_ANALYZER_DEADCODE_DEADSTORES': bool,
    'CLANG_ANALYZER_GCD': bool,
    'CLANG_ANALYZER_MALLOC': bool,
    'CLANG_ANALYZER_MEMORY_MANAGEMENT': bool,
    'CLANG_ANALYZER_OBJC_ATSYNC': bool,
    'CLANG_ANALYZER_OBJC_COLLECTIONS': bool,
    'CLANG_ANALYZER_OBJC_INCOMP_METHOD_TYPES': bool,
    'CLANG_ANALYZER_OBJC_NSCFERROR': bool,
    'CLANG_ANALYZER_OBJC_RETAIN_COUNT': bool,
    'CLANG_ANALYZER_OBJC_SELF_INIT': bool,
    'CLANG_ANALYZER_OBJC_UNUSED_IVARS': bool,
    'CLANG_ANALYZER_SECURITY_FLOATLOOPCOUNTER': bool,
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_GETPW_GETS': bool,
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_MKSTEMP': bool,
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_RAND': bool,
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_STRCPY': bool,
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_UNCHECKEDRETURN': bool,
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_VFORK': bool,
    'CLANG_ANALYZER_SECURITY_KEYCHAIN_API': bool,
    'CLANG_ARC_MIGRATE_DIR': str,
    'CLANG_ARC_MIGRATE_EMIT_ERROR': bool,
    'CLANG_ARC_MIGRATE_PRECHECK': str,
    'CLANG_ARC_MIGRATE_REPORT_OUTPUT': str,
    'CLANG_COLOR_DIAGNOSTICS': bool,
    'CLANG_CXX_LANGUAGE_STANDARD': str,
    'CLANG_CXX_LIBRARY': str,
    'CLANG_DEBUG_INFORMATION_LEVEL': str,
    'CLANG_ENABLE_APP_EXTENSION': bool,
    'CLANG_ENABLE_MODULES': bool,
    'CLANG_ENABLE_MODULE_IMPLEMENTATION_OF': bool,
    'CLANG_ENABLE_OBJC_ARC': bool,
    'CLANG_INSTRUMENT_FOR_OPTIMIZATION_PROFILING': bool,
    'CLANG_LINK_OBJC_RUNTIME': bool,
    'CLANG_MACRO_BACKTRACE_LIMIT': int,
    'CLANG_MODULES_AUTOLINK': bool,
    'CLANG_MODULES_IGNORE_MACROS': list,
    'CLANG_MODULES_VALIDATE_SYSTEM_HEADERS': bool,
    'CLANG_MODULES_VALIDATION_TIMESTAMP': str,
    'CLANG_MODULE_CACHE_PATH': str,
    'CLANG_OBJC_MIGRATE_DIR': str,
    'CLANG_OPTIMIZATION_PROFILE_FILE': str,
    'CLANG_RETAIN_COMMENTS_FROM_SYSTEM_HEADERS': bool,
    'CLANG_STATIC_ANALYZER_MODE': str,
    'CLANG_STATIC_ANALYZER_MODE_ON_ANALYZE_ACTION': str,
    'CLANG_USE_OPTIMIZATION_PROFILE': bool,
    'CLANG_WARN_ASSIGN_ENUM': bool,
    'CLANG_WARN_BOOL_CONVERSION': bool,
    'CLANG_WARN_CONSTANT_CONVERSION': bool,
    'CLANG_WARN_CXX0X_EXTENSIONS': bool,
    'CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS': bool,
    'CLANG_WARN_DIRECT_OBJC_ISA_USAGE': str,
    'CLANG_WARN_DOCUMENTATION_COMMENTS': bool,
    'CLANG_WARN_EMPTY_BODY': bool,
    'CLANG_WARN_ENUM_CONVERSION': bool,
    'CLANG_WARN_IMPLICIT_SIGN_CONVERSION': bool,
    'CLANG_WARN_INT_CONVERSION': bool,
    'CLANG_WARN_OBJC_EXPLICIT_OWNERSHIP_TYPE': bool,
    'CLANG_WARN_OBJC_IMPLICIT_ATOMIC_PROPERTIES': bool,
    'CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF': bool,
    'CLANG_WARN_OBJC_MISSING_PROPERTY_SYNTHESIS': bool,
    'CLANG_WARN_OBJC_RECEIVER_WEAK': bool,
    'CLANG_WARN_OBJC_REPEATED_USE_OF_WEAK': bool,
    'CLANG_WARN_OBJC_ROOT_CLASS': str,
    'CLANG_WARN_SUSPICIOUS_IMPLICIT_CONVERSION': bool,
    'CLANG_WARN_UNREACHABLE_CODE': bool,
    'CLANG_WARN__ARC_BRIDGE_CAST_NONARC': bool,
    'CLANG_WARN__DUPLICATE_METHOD_MATCH': bool,
    'CLANG_WARN__EXIT_TIME_DESTRUCTORS': bool,
    'CLANG_X86_VECTOR_INSTRUCTIONS': str,
    'CODE_SIGN_ENTITLEMENTS': str,
    'CODE_SIGN_IDENTITY': str,
    'CODE_SIGN_RESOURCE_RULES_PATH': str,
    'COLOR_DIAGNOSTICS': bool,
    'COMBINE_HIDPI_IMAGES': bool,
    'COMPOSITE_SDK_DIRS': list,
    'COMPRESS_PNG_FILES': bool,
    'CONFIGURATION': str,
    'CONFIGURATION_BUILD_DIR': str,
    'CONFIGURATION_TEMP_DIR': str,
    'COPYING_PRESERVES_HFS_DATA': bool,
    'COPY_PHASE_STRIP': bool,
    'CP': str,
    'CPP_HEADERMAP_FILE': str,
    'CPP_HEADERMAP_FILE_FOR_ALL_NON_FRAMEWORK_TARGET_HEADERS': str,
    'CPP_HEADERMAP_FILE_FOR_ALL_TARGET_HEADERS': str,
    'CPP_HEADERMAP_FILE_FOR_GENERATED_FILES': str,
    'CPP_HEADERMAP_FILE_FOR_OWN_TARGET_HEADERS': str,
    'CPP_HEADERMAP_FILE_FOR_PROJECT_FILES': str,
    'CPP_HEADERMAP_PRODUCT_HEADERS_VFS_FILE': str,
    'CPP_HEADER_SYMLINKS_DIR': str,
    'CREATE_INFOPLIST_SECTION_IN_BINARY': bool,
    'CURRENT_ARCH': str,
    'CURRENT_PROJECT_VERSION': str,
    'CURRENT_VARIANT': str,
    'DEAD_CODE_STRIPPING': bool,
    'DEBUG_INFORMATION_FORMAT': str,
    'DEFAULT_COMPILER': str,
    'DEFAULT_KEXT_INSTALL_PATH': str,
    'DEFAULT_SSE_LEVEL_3_NO': str,
    'DEFAULT_SSE_LEVEL_3_YES': str,
    'DEFAULT_SSE_LEVEL_3_SUPPLEMENTAL_NO': str,
    'DEFAULT_SSE_LEVEL_3_SUPPLEMENTAL_YES': str,
    'DEFAULT_SSE_LEVEL_4_1_NO': str,
    'DEFAULT_SSE_LEVEL_4_1_YES': str,
    'DEFAULT_SSE_LEVEL_4_2_NO': str,
    'DEFAULT_SSE_LEVEL_4_2_YES': str,
    'DEFINES_MODULE': bool,
    'DEPLOYMENT_LOCATION': bool,
    'DEPLOYMENT_POSTPROCESSING': bool,
    'DERIVED_FILE_DIR': str,
    'DERIVED_FILES_DIR': str,
    'DERIVED_SOURCES_DIR': str,
    'DEVELOPER_APPLICATIONS_DIR': str,
    'DEVELOPER_BIN_DIR': str,
    'DEVELOPER_DIR': str,
    'DEVELOPER_FRAMEWORKS_DIR': str,
    'DEVELOPER_FRAMEWORKS_DIR_QUOTED': str,
    'DEVELOPER_LIBRARY_DIR': str,
    'DEVELOPER_SDK_DIR': str,
    'DEVELOPER_TOOLS_DIR': str,
    'DEVELOPER_USR_DIR': str,
    'DSTROOT': str,
    'DT_TOOLCHAIN_DIR': str,
    'DYLIB_COMPATIBILITY_VERSION': str,
    'DYLIB_CURRENT_VERSION': str,
    'DYLIB_INSTALL_NAME_BASE': list,
    'EFFECTIVE_PLATFORM_NAME': str,
    'EMBEDDED_CONTENT_CONTAINS_SWIFT': bool,
    'EMBEDDED_PROFILE_NAME': str,
    'ENABLE_APPLE_KEXT_CODE_GENERATION': bool,
    'ENABLE_HEADER_DEPENDENCIES': bool,
    'ENABLE_NS_ASSERTIONS': bool,
    'ENABLE_STRICT_OBJC_MSGSEND': bool,
    'EXCLUDED_INSTALLSRC_SUBDIRECTORY_PATTERNS': list,
    'EXCLUDED_RECURSIVE_SEARCH_PATH_SUBDIRECTORIES': list,
    'EXECUTABLE_EXTENSION': str,
    'EXECUTABLE_PREFIX': str,
    'EXECUTABLE_SUFFIX': str,
    'EXECUTABLE_VARIANT_SUFFIX': str,
    'EXPORTED_SYMBOLS_FILE': str,
    'FILE_LIST': str,
    'FRAMEWORK_SEARCH_PATHS': list,
    'FRAMEWORK_VERSION': str,
    'GCC3_VERSION': str,
    'GCC_CHAR_IS_UNSIGNED_CHAR': bool,
    'GCC_CW_ASM_SYNTAX': bool,
    'GCC_C_LANGUAGE_STANDARD': str,
    'GCC_DEBUG_INFORMATION_FORMAT': str,
    'GCC_DYNAMIC_NO_PIC': bool,
    'GCC_ENABLE_ASM_KEYWORD': bool,
    'GCC_ENABLE_BUILTIN_FUNCTIONS': bool,
    'GCC_ENABLE_CPP_EXCEPTIONS': bool,
    'GCC_ENABLE_CPP_RTTI': bool,
    'GCC_ENABLE_EXCEPTIONS': bool,
    'GCC_ENABLE_FLOATING_POINT_LIBRARY_CALLS': bool,
    'GCC_ENABLE_KERNEL_DEVELOPMENT': bool,
    'GCC_ENABLE_OBJC_EXCEPTIONS': bool,
    'GCC_ENABLE_OBJC_GC': str,
    'GCC_ENABLE_PASCAL_STRINGS': bool,
    'GCC_ENABLE_SSE3_EXTENSIONS': bool,
    'GCC_ENABLE_SSE41_EXTENSIONS': bool,
    'GCC_ENABLE_SSE42_EXTENSIONS': bool,
    'GCC_ENABLE_SUPPLEMENTAL_SSE3_INSTRUCTIONS': bool,
    'GCC_ENABLE_TRIGRAPHS': bool,
    'GCC_FAST_MATH': bool,
    'GCC_GENERATE_DEBUGGING_SYMBOLS': bool,
    'GCC_GENERATE_TEST_COVERAGE_FILES': bool,
    'GCC_INCREASE_PRECOMPILED_HEADER_SHARING': bool,
    'GCC_INLINES_ARE_PRIVATE_EXTERN': bool,
    'GCC_INPUT_FILETYPE': str,
    'GCC_INSTRUMENT_PROGRAM_FLOW_ARCS': bool,
    'GCC_LINK_WITH_DYNAMIC_LIBRARIES': bool,
    'GCC_MACOSX_VERSION_MIN': str,
    'GCC_NO_COMMON_BLOCKS': bool,
    'GCC_OBJC_ABI_VERSION': str,
    'GCC_OBJC_LEGACY_DISPATCH': bool,
    'GCC_OPERATION': str,
    'GCC_OPTIMIZATION_LEVEL': str,
    'GCC_PFE_FILE_C_DIALECTS': list,
    'GCC_PRECOMPILE_PREFIX_HEADER': bool,
    'GCC_PREFIX_HEADER': str,
    'GCC_PREPROCESSOR_DEFINITIONS': list,
    'GCC_PREPROCESSOR_DEFINITIONS_NOT_USED_IN_PRECOMPS': list,
    'GCC_PRODUCT_TYPE_PREPROCESSOR_DEFINITIONS': list,
    'GCC_REUSE_STRINGS': bool,
    'GCC_SHORT_ENUMS': bool,
    'GCC_STRICT_ALIASING': bool,
    'GCC_SYMBOLS_PRIVATE_EXTERN': bool,
    'GCC_THREADSAFE_STATICS': bool,
    'GCC_TREAT_IMPLICIT_FUNCTION_DECLARATIONS_AS_ERRORS': bool,
    'GCC_TREAT_INCOMPATIBLE_POINTER_TYPE_WARNINGS_AS_ERRORS': bool,
    'GCC_TREAT_WARNINGS_AS_ERRORS': bool,
    'GCC_UNROLL_LOOPS': bool,
    'GCC_USE_GCC3_PFE_SUPPORT': bool,
    'GCC_USE_STANDARD_INCLUDE_SEARCHING': bool,
    'GCC_VERSION': str,
    'GCC_WARN_64_TO_32_BIT_CONVERSION': bool,
    'GCC_WARN_ABOUT_DEPRECATED_FUNCTIONS': bool,
    'GCC_WARN_ABOUT_INVALID_OFFSETOF_MACRO': bool,
    'GCC_WARN_ABOUT_MISSING_FIELD_INITIALIZERS': bool,
    'GCC_WARN_ABOUT_MISSING_NEWLINE': bool,
    'GCC_WARN_ABOUT_MISSING_PROTOTYPES': bool,
    'GCC_WARN_ABOUT_POINTER_SIGNEDNESS': bool,
    'GCC_WARN_ABOUT_RETURN_TYPE': str,
    'GCC_WARN_ALLOW_INCOMPLETE_PROTOCOL': bool,
    'GCC_WARN_CHECK_SWITCH_STATEMENTS': bool,
    'GCC_WARN_FOUR_CHARACTER_CONSTANTS': bool,
    'GCC_WARN_HIDDEN_VIRTUAL_FUNCTIONS': bool,
    'GCC_WARN_INHIBIT_ALL_WARNINGS': bool,
    'GCC_WARN_INITIALIZER_NOT_FULLY_BRACKETED': bool,
    'GCC_WARN_MISSING_PARENTHESES': bool,
    'GCC_WARN_MULTIPLE_DEFINITION_TYPES_FOR_SELECTOR': bool,
    'GCC_WARN_NON_VIRTUAL_DESTRUCTOR': bool,
    'GCC_WARN_PEDANTIC': bool,
    'GCC_WARN_SHADOW': bool,
    'GCC_WARN_SIGN_COMPARE': bool,
    'GCC_WARN_STRICT_SELECTOR_MATCH': bool,
    'GCC_WARN_TYPECHECK_CALLS_TO_PRINTF': bool,
    'GCC_WARN_UNDECLARED_SELECTOR': bool,
    'GCC_WARN_UNINITIALIZED_AUTOS': str,
    'GCC_WARN_UNKNOWN_PRAGMAS': bool,
    'GCC_WARN_UNUSED_FUNCTION': bool,
    'GCC_WARN_UNUSED_LABEL': bool,
    'GCC_WARN_UNUSED_PARAMETER': bool,
    'GCC_WARN_UNUSED_VALUE': bool,
    'GCC_WARN_UNUSED_VARIABLE': bool,
    'GENERATE_MASTER_OBJECT_FILE': bool,
    'GENERATE_PKGINFO_FILE': bool,
    'GENERATE_PROFILING_CODE': bool,
    'GID': str,
    'GROUP': str,
    'HEADERMAP_FILE_FORMAT': str,
    'HEADERMAP_INCLUDES_FLAT_ENTRIES_FOR_TARGET_BEING_BUILT': bool,
    'HEADERMAP_INCLUDES_FRAMEWORK_ENTRIES_FOR_ALL_PRODUCT_TYPES': bool,
    'HEADERMAP_INCLUDES_NONPUBLIC_NONPRIVATE_HEADERS': bool,
    'HEADERMAP_INCLUDES_PROJECT_HEADERS': bool,
    'HEADERMAP_USES_FRAMEWORK_PREFIX_ENTRIES': bool,
    'HEADERMAP_USES_VFS': bool,
    'HEADER_SEARCH_PATHS': list,
    'IBC_COMPILER_AUTO_ACTIVATE_CUSTOM_FONTS': bool,
    'IBC_ERRORS': bool,
    'IBC_FLATTEN_NIBS': bool,
    'IBC_NOTICES': bool,
    'IBC_OTHER_FLAGS': list,
    'IBC_WARNINGS': bool,
    'ICONV': str,
    'INCLUDED_RECURSIVE_SEARCH_PATH_SUBDIRECTORIES': list,
    'INFOPLIST_EXPAND_BUILD_SETTINGS': bool,
    'INFOPLIST_FILE': str,
    'INFOPLIST_OTHER_PREPROCESSOR_FLAGS': list,
    'INFOPLIST_OUTPUT_FORMAT': str,
    'INFOPLIST_PREFIX_HEADER': str,
    'INFOPLIST_PREPROCESS': bool,
    'INFOPLIST_PREPROCESSOR_DEFINITIONS': list,
    'INIT_ROUTINE': str,
    'INSTALL_DIR': str,
    'INSTALL_GROUP': str,
    'INSTALL_MODE_FLAG': str,
    'INSTALL_OWNER': str,
    'INSTALL_PATH': str,
    'INSTALL_ROOT': str,
    'IPHONEOS_DEPLOYMENT_TARGET': str,
    'JAVAC_DEFAULT_FLAGS': str,
    'JAVA_APP_STUB': str,
    'JAVA_ARCHIVE_CLASSES': bool,
    'JAVA_ARCHIVE_TYPE': str,
    'JAVA_COMPILER': str,
    'JAVA_FRAMEWORK_RESOURCES_DIRS': list,
    'JAVA_JAR_FLAGS': list,
    'JAVA_SOURCE_SUBDIR': str,
    'JAVA_USE_DEPENDENCIES': bool,
    'JAVA_ZIP_FLAGS': list,
    'KEEP_PRIVATE_EXTERNS': bool,
    'LD_DEPENDENCY_INFO_FILE': str,
    'LD_DYLIB_INSTALL_NAME': str,
    'LD_GENERATE_MAP_FILE': bool,
    'LD_MAP_FILE_PATH': str,
    'LD_NO_PIE': bool,
    'LD_QUOTE_LINKER_ARGUMENTS_FOR_COMPILER_DRIVER': bool,
    'LD_RUNPATH_SEARCH_PATHS': list,
    'LEGACY_DEVELOPER_DIR': str,
    'LEX': str,
    'LEXFLAGS': list,
    'LIBRARY_FLAG_NOSPACE': bool,
    'LIBRARY_FLAG_PREFIX': str,
    'LIBRARY_KEXT_INSTALL_PATH': str,
    'LIBRARY_SEARCH_PATHS': list,
    'LINKER_DISPLAYS_MANGLED_NAMES': bool,
    'LINK_WITH_STANDARD_LIBRARIES': bool,
    'LLVM_IMPLICIT_AGGRESSIVE_OPTIMIZATIONS': bool,
    'LLVM_LTO': bool,
    'LLVM_OPTIMIZATION_LEVEL_VAL_0': bool,
    'LLVM_OPTIMIZATION_LEVEL_VAL_1': bool,
    'LLVM_OPTIMIZATION_LEVEL_VAL_2': bool,
    'LLVM_OPTIMIZATION_LEVEL_VAL_3': bool,
    'LLVM_OPTIMIZATION_LEVEL_VAL_fast': bool,
    'LLVM_OPTIMIZATION_LEVEL_VAL_s': bool,
    'LOCAL_ADMIN_APPS_DIR': str,
    'LOCAL_APPS_DIR': str,
    'LOCAL_DEVELOPER_DIR': str,
    'LOCAL_LIBRARY_DIR': str,
    'MACH_O_TYPE': str,
    'MACOSX_DEPLOYMENT_TARGET': str,
    'MODULEMAP_FILE': str,
    'MODULEMAP_PRIVATE_FILE': str,
    'MODULE_CACHE_DIR': str,
    'MODULE_NAME': str,
    'MODULE_START': str,
    'MODULE_STOP': str,
    'MODULE_VERSION': str,
    'MTL_ENABLE_DEBUG_INFO': bool,
    'NATIVE_ARCH': str,
    'OBJC_ABI_VERSION': str,
    'OBJECT_FILE_DIR': str,
    'OBJECT_FILE_DIR_': str,
    'OBJROOT': str,
    'ONLY_ACTIVE_ARCH': bool,
    'ORDER_FILE': str,
    'OS': str,
    'OSAC': str,
    'OSACOMPILE_EXECUTE_ONLY': bool,
    'OTHER_CFLAGS': list,
    'OTHER_CODE_SIGN_FLAGS': list,
    'OTHER_CPLUSPLUSFLAGS': list,
    'OTHER_LDFLAGS': list,
    'OTHER_LIBTOOLFLAGS': list,
    'OTHER_OSACOMPILEFLAGS': str,
    'PATH_PREFIXES_EXCLUDED_FROM_HEADER_DEPENDENCIES': list,
    'PLATFORM_DEVELOPER_APPLICATIONS_DIR': str,
    'PLATFORM_DEVELOPER_BIN_DIR': str,
    'PLATFORM_DEVELOPER_LIBRARY_DIR': str,
    'PLATFORM_DEVELOPER_SDK_DIR': str,
    'PLATFORM_DEVELOPER_TOOLS_DIR': str,
    'PLATFORM_DEVELOPER_USR_DIR': str,
    'PLATFORM_DIR': str,
    'PLATFORM_NAME': str,
    'PLATFORM_PREFERRED_ARCH': str,
    'PLATFORM_PRODUCT_BUILD_VERSION': str,
    'PLIST_FILE_OUTPUT_FORMAT': str,
    'PRECOMPILE_PREFIX_HEADER': bool,
    'PRECOMPS_INCLUDE_HEADERS_FROM_BUILT_PRODUCTS_DIR': bool,
    'PREFIX_HEADER': str,
    'PRELINK_FLAGS': list,
    'PRELINK_LIBS': list,
    'PRESERVE_DEAD_CODE_INITS_AND_TERMS': bool,
    'PRIVATE_HEADERS_FOLDER_PATH': str,
    'PRODUCT_DEFINITION_PLIST': str,
    'PRODUCT_MODULE_NAME': str,
    'PRODUCT_NAME': str,
    'PROJECT': str,
    'PROJECT_DERIVED_FILE_DIR': str,
    'PROJECT_DIR': str,
    'PROJECT_FILE_PATH': str,
    'PROJECT_NAME': str,
    'PROJECT_TEMP_DIR': str,
    'PROJECT_TEMP_ROOT': str,
    'PROVISIONING_PROFILE': str,
    'PUBLIC_HEADERS_FOLDER_PATH': str,
    'REMOVE_CVS_FROM_RESOURCES': bool,
    'REMOVE_GIT_FROM_RESOURCES': bool,
    'REMOVE_HEADERS_FROM_EMBEDDED_BUNDLES': bool,
    'REMOVE_HG_FROM_RESOURCES': bool,
    'REMOVE_SVN_FROM_RESOURCES': bool,
    'RETAIN_RAW_BINARIES': bool,
    'REZ_COLLECTOR_DIR': str,
    'REZ_OBJECTS_DIR': str,
    'REZ_SEARCH_PATHS': str,
    'RUN_CLANG_STATIC_ANALYZER': bool,
    'SCAN_ALL_SOURCE_FILES_FOR_INCLUDES': bool,
    'SDKROOT': str,
    'SDK_DIR': str,
    'SDK_NAME': str,
    'SDK_PRODUCT_BUILD_VERSION': str,
    'SECTORDER_FLAGS': list,
    'SED': str,
    'SEPARATE_STRIP': bool,
    'SEPARATE_SYMBOL_EDIT': bool,
    'SHARED_PRECOMPS_DIR': str,
    'SKIP_INSTALL': bool,
    'SOURCE_ROOT': str,
    'SRCROOT': str,
    'STRINGS_FILE_OUTPUT_ENCODING': str,
    'STRIPFLAGS': bool,
    'STRIP_INSTALLED_PRODUCT': bool,
    'STRIP_STYLE': str,
    'SUPPORTED_PLATFORMS': list,
    'SWIFT_OPTIMIZATION_LEVEL': str,
    'SYMROOT': str,
    'SYSTEM_ADMIN_APPS_DIR': str,
    'SYSTEM_APPS_DIR': str,
    'SYSTEM_CORE_SERVICES_DIR': str,
    'SYSTEM_DEMOS_DIR': str,
    'SYSTEM_DEVELOPER_APPS_DIR': str,
    'SYSTEM_DEVELOPER_BIN_DIR': str,
    'SYSTEM_DEVELOPER_DEMOS_DIR': str,
    'SYSTEM_DEVELOPER_DIR': str,
    'SYSTEM_DEVELOPER_DOC_DIR': str,
    'SYSTEM_DEVELOPER_GRAPHICS_TOOLS_DIR': str,
    'SYSTEM_DEVELOPER_JAVA_TOOLS_DIR': str,
    'SYSTEM_DEVELOPER_PERFORMANCE_TOOLS_DIR': str,
    'SYSTEM_DEVELOPER_RELEASENOTES_DIR': str,
    'SYSTEM_DEVELOPER_TOOLS': str,
    'SYSTEM_DEVELOPER_TOOLS_DOC_DIR': str,
    'SYSTEM_DEVELOPER_TOOLS_RELEASENOTES_DIR': str,
    'SYSTEM_DEVELOPER_USR_DIR': str,
    'SYSTEM_DEVELOPER_UTILITIES_DIR': str,
    'SYSTEM_DOCUMENTATION_DIR': str,
    'SYSTEM_KEXT_INSTALL_PATH': str,
    'SYSTEM_LIBRARY_DIR': str,
    'TARGETNAME': str,
    'TARGET_BUILD_DIR': str,
    'TARGET_NAME': str,
    'TARGET_TEMP_DIR': str,
    'TARGETED_DEVICE_FAMILY': str,
    'TEMP_DIR': str,
    'TEMP_FILES_DIR': str,
    'TEMP_FILE_DIR': str,
    'TEMP_ROOT': str,
    'TEST_HOST': str,
    'TREAT_MISSING_BASELINES_AS_TEST_FAILURES': bool,
    'UID': str,
    'UNEXPORTED_SYMBOLS_FILE': str,
    'UNSTRIPPED_PRODUCT': bool,
    'USER': str,
    'USER_APPS_DIR': str,
    'USER_HEADER_SEARCH_PATHS': list,
    'USER_LIBRARY_DIR': str,
    'USE_HEADERMAP': bool,
    'USE_HEADER_SYMLINKS': bool,
    'VALIDATE_PRODUCT': bool,
    'VALID_ARCHS': list,
    'VERSIONING_SYSTEM': str,
    'VERSION_INFO_BUILDER': str,
    'VERSION_INFO_EXPORT_DECL': str,
    'VERSION_INFO_FILE': str,
    'VERSION_INFO_PREFIX': str,
    'VERSION_INFO_SUFFIX': str,
    'WARNING_CFLAGS': list,
    'WARNING_LDFLAGS': list,
    'WRAPPER_EXTENSION': str,
    'XCODE_APP_SUPPORT_DIR': str,
    'XCODE_PRODUCT_BUILD_VERSION': str,
    'XCODE_VERSION_ACTUAL': str,
    'XCODE_VERSION_MAJOR': str,
    'XCODE_VERSION_MINOR': str,
    'YACC': str,
    'YACCFLAGS': list,
}
