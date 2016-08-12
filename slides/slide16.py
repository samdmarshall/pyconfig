#!/usr/bin/python

import pypresenter.slide

class slide16(pypresenter.slide):
   def __init__(self):
      super(self.__class__, self).__init__('left')
   def content(self, window=None):
        return "--- HEAD.pyconfig\n"\
               "+++ merge.pyconfig\n"\
               "@@ -1,36 +1,40 @@\n"\
               "-# HEAD.pyconfig\n"\
               "+# merge.pyconfig\n"\
               " ""setting PODS_BUILD_DIR {\n"\
               " \t""for * {\n"\
               " \t\t$BUILD_DIR\n"\
               " \t}\n"\
               " }\n\n"\
               " ""setting PODS_CONFIGURATION_BUILD_DIR {\n"\
               " \t""for * {\n"\
               " \t\t$PODS_BUILD_DIR/$(CONFIGURATION)$(EFFECTIVE_PLATFORM_NAME)\n"\
               " \t}\n"\
               " }\n\n"\
               " ""setting PODS_ROOT {\n"\
               " \t""for * {\n"\
               " \t\t${SRCROOT}/Pods\n"\
               " \t}\n"\
               " }\n\n"\
               " ""setting FRAMEWORK_SEARCH_PATHS ""inherits {\n"\
               " \t""for * {\n"\
               "-\t\t\"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth\"\n"\
               "+\t\t\"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth\",\n"\
               "+\t\t\"$PODS_CONFIGURATION_BUILD_DIR/AFNetworking\"\n"\
               " \t}\n"\
               " }\n\n"\
               " ""setting OTHER_CFLAGS ""inherits {\n"\
               " \t""for * {\n"\
               "-\t\t-iquote \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth/RZBluetooth.framework/Headers\"\n"\
               "+\t\t-iquote \"$PODS_CONFIGURATION_BUILD_DIR/RZBluetooth/RZBluetooth.framework/Headers\",\n"\
               "+\t\t-iquote \"$PODS_CONFIGURATION_BUILD_DIR/AFNetworking/AFNetworking.framework/Headers\"\n"\
               " \t}\n"\
               " }\n\n"\
               " ""setting OTHER_LDFLAGS ""inherits {\n"\
               " \t""for * {\n"\
               "-\t\t-framework \"RZBluetooth\"\n"\
               "+\t\t-framework \"RZBluetooth\",\n"\
               "+\t\t-framework \"AFNetworking\",\n"\
               "+\t\t-framework \"Security\"\n"\
               " \t}\n"\
               " }"
   def draw(self, window):
      text = self.content(window)
      self.displayText(window, text)
   def formatting(self):
      return {
         "52": ['on_red'],
         "53": ['normal'],
         "68": ['on_green'],
         "69": ['normal'],
         "354": ['on_red'],
         "355": ['normal'],
         "400": ['on_green'],
         "401": ['normal'],
         "447": ['on_green'],
         "448": ['normal'],
         "540": ['on_red'],
         "541": ['normal'],
         "624": ['on_green'],
         "625": ['normal'],
         "709": ['on_green'],
         "710": ['normal'],
         "842": ['on_red'],
         "843": ['normal'],
         "869": ['on_green'],
         "870": ['normal'],
         "897": ['on_green'],
         "898": ['normal'],
         "926": ['on_green'],
         "927": ['normal'],
      }