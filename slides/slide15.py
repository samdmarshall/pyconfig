#!/usr/bin/python

import pypresenter.slide

class slide15(pypresenter.slide):
   def __init__(self):
      super(self.__class__, self).__init__('left')
   def content(self, window=None):
        return "--- HEAD.xcconfig\n"\
               "+++ merge.xcconfig\n"\
               "@@ -1,12 +1,12 @@\n"\
               "-// HEAD.xcconfig\n"\
               "+// merge.xcconfig\n"\
               " PODS_BUILD_DIR = $BUILD_DIR\n\n"\
               " PODS_CONFIGURATION_BUILD_DIR = $PODS_BUILD_DIR/$(CONFIGURATION)$(EFFECTIVE_PLATFORM_NAME)\n\n"\
               " PODS_ROOT = $SRCROOT/Pods\n\n"\
               "-FRAMEWORK_SEARCH_PATHS = $(inherited) \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth\"\n"\
               "+FRAMEWORK_SEARCH_PATHS = $(inherited) \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth\" \"$PODS_CONFIGURATION_BUILD_DIR/AFNetworking\"\n\n"\
               "-OTHER_CFLAGS = $(inherited) -iquote \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth/RZBluetooth.framework/Headers\"\n"\
               "+OTHER_CFLAGS = $(inherited) -iquote \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth/RZBluetooth.framework/Headers\" -iquote \"$PODS_CONFIGURATION_BUILD_DIR/AFNetworking/AFNetworking.framework/Headers\"\n\n"\
               "-OTHER_LDFLAGS = $(inherited) -framework \"RZBluetooth\"\n"\
               "+OTHER_LDFLAGS = $(inherited) -framework \"RZBluetooth\" -framework \"AFNetworking\" -framework \"Security\""
   def draw(self, window):
      text = self.content(window)
      self.displayText(window, text)
   def formatting(self):
      return {
         "52": ['on_red'],
         "53": ['normal'],
         "69": ['on_green'],
         "70": ['normal'],
         "231": ['on_red'],
         "232": ['normal'],
         "313": ['on_green'],
         "314": ['normal'],
         "440": ['on_red'],
         "441": ['normal'],
         "550": ['on_green'],
         "551": ['normal'],
         "744": ['on_red'],
         "745": ['normal'],
         "798": ['on_green'],
         "799": ['normal']
      }