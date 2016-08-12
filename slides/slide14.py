#!/usr/bin/python

import pypresenter.slide

class slide14(pypresenter.slide):
   def __init__(self):
      super(self.__class__, self).__init__('left')
   def content(self, window=None):
        return "# merge.pyconfig\n"\
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
               "\t\t""\"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth\",\n"\
               "\t\t""\"$PODS_CONFIGURATION_BUILD_DIR/AFNetworking\"\n"\
               "\t""}\n"\
               "}\n\n"\
               "setting OTHER_CFLAGS ""inherits {\n"\
               "\t""for * {\n"\
               "\t\t""-iquote \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth/RZBluetooth.framework/Headers\",\n"\
               "\t\t""-iquote \"$PODS_CONFIGURATION_BUILD_DIR/AFNetworking/AFNetworking.framework/Headers\"\n"\
               "\t""}\n"\
               "}\n\n"\
               "setting OTHER_LDFLAGS ""inherits {\n"\
               "\t""for * {\n"\
               "\t\t""-framework \"RZBluetooth\",\n"\
               "\t\t""-framework \"AFNetworking\",\n"\
               "\t\t""-framework \"Security\"\n"\
               "\t""}\n"\
               "}"
   def draw(self, window):
      text = self.content(window)
      self.displayText(window, text)
