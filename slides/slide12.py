#!/usr/bin/python

import curses
import pypresenter.slide

class slide12(pypresenter.slide):
   def __init__(self):
      super(self.__class__, self).__init__('left')
   def content(self, window=None):
      return   "# HEAD.pyconfig\n"\
               "setting PODS_BUILD_DIR {\n"\
               "\t""for * {\n"\
               "\t\t""$BUILD_DIR\n"\
               "\t""}\n"\
               "}\n\n"\
               "setting PODS_CONFIGURATION_BUILD_DIR {\n"\
               "\t""for * {\n"\
               "\t\t""$PODS_BUILD_DIR/$(CONFIGURATION)$(EFFECTIVE_PLATFORM_NAME)\n"\
               "\t""}\n"\
               "}\n\n"\
               "setting PODS_ROOT {\n"\
               "\t""for * {\n"\
               "\t\t""$SRCROOT/Pods\n"\
               "\t""}\n"\
               "}\n\n"\
               "setting FRAMEWORK_SEARCH_PATHS ""inherits {\n"\
               "\t""for * {\n"\
               "\t\t""$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth\n"\
               "\t""}\n"\
               "}\n\n"\
               "setting OTHER_CFLAGS ""inherits {\n"\
               "\t""for * {\n"\
               "\t\t""-iquote \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth/RZBluetooth.framework/Headers\"\n"\
               "\t""}\n"\
               "}\n\n"\
               "setting OTHER_LDFLAGS ""inherits {\n"\
               "\t""for * {\n"\
               "\t\t""-framework \"RZBluetooth\"\n"\
               "\t""}\n"\
               "}\n\n"
   def draw(self, window):
      text = self.content(window)
      self.displayText(window, text)
