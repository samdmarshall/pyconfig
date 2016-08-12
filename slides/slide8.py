#!/usr/bin/python

import pypresenter.slide

class slide8(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('left')
    def content(self, window=None):
        return "\nExporting to xcconfig\n\n"\
               "One feature that pyconfig files offers is to control the name of the xcconfig file that will be generated. This uses the \"export\" keyword to specify a relative path from the pyconfig file where the exported xcconfig file should be written."\
               "\n\n"\
               "export \"my_settings.xcconfig\""
    def draw(self, window):
        text = self.content(window)
        self.displayText(window, text)

    def formatting(self):
        return {
            "0": ['underline'],
            "21": ['normal'],
            "260": ['blue'],
            "266": ['normal'],
            "267": ['green'],
            "289": ['normal'],
        }