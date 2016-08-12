#!/usr/bin/python

import pypresenter.slide

class slide11(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('left')
    def content(self, window=None):
        return "// HEAD.xcconfig\n"\
               "PODS_BUILD_DIR = $BUILD_DIR\n\n"\
               "PODS_CONFIGURATION_BUILD_DIR = $PODS_BUILD_DIR/$(CONFIGURATION)$(EFFECTIVE_PLATFORM_NAME)\n\n"\
               "PODS_ROOT = $SRCROOT/Pods\n\n"\
               "FRAMEWORK_SEARCH_PATHS = $(inherited) \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth\"\n\n"\
               "OTHER_CFLAGS = $(inherited) -iquote \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth/RZBluetooth.framework/Headers\"\n\n"\
               "OTHER_LDFLAGS = $(inherited) -framework \"RZBluetooth\"\n\n"
    def draw(self, window):
        text = self.content(window)
        self.displayText(window, text)