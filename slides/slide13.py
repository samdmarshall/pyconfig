#!/usr/bin/python

import pypresenter.slide

class slide13(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('left')
    def content(self, window=None):
        return "// merge.xcconfig\n"\
               "PODS_BUILD_DIR = $BUILD_DIR\n\n"\
               "PODS_CONFIGURATION_BUILD_DIR = $PODS_BUILD_DIR/$(CONFIGURATION)$(EFFECTIVE_PLATFORM_NAME)\n\n"\
               "PODS_ROOT = $SRCROOT/Pods\n\n"\
               "FRAMEWORK_SEARCH_PATHS = $(inherited) \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth\" \"$PODS_CONFIGURATION_BUILD_DIR/AFNetworking\"\n\n"\
               "OTHER_CFLAGS = $(inherited) -iquote \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth/RZBluetooth.framework/Headers\" -iquote \"$PODS_CONFIGURATION_BUILD_DIR/AFNetworking/AFNetworking.framework/Headers\"\n\n"\
               "OTHER_LDFLAGS = $(inherited) -framework \"RZBluetooth\" -framework \"AFNetworking\" -framework \"Security\"\n\n"
    def draw(self, window):
        text = self.content(window)
        self.displayText(window, text)
    def formatting(self):
        return {}
