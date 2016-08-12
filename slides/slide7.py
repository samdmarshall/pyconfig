#!/usr/bin/python

import pypresenter.slide

class slide7(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('left')
    def content(self, window=None):
        return "\nIncluding Other Files\n\n"\
               "As with xcconfig files, you can include other files into your pyconfig files. For this the 'include' keyword is used, it is prepended by a exclamation mark or a question mark -- depending on if the included file should be treated as an optional include or not. (Optional includes are a feature that was introduced to xcconfig files in Xcode 8 beta 4)."\
               "\n\n"\
               "!include \"required_settings.xcconfig\""\
               "\n\n"\
               "?include \"optional_settings.xcconfig\""
    def draw(self, window):
        text = self.content(window)
        self.displayText(window, text)
    def formatting(self):
        return {
            "0": ['underline'],
            "21": ['normal'],
        }