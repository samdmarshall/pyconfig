#!/usr/bin/python

import pypresenter.slide

class slide6(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('left')
    def content(self, window=None):
        return "\nSpecifying Conditional Values\n\n"\
               "Sometime composition of values is not enough, and it is necessary to use conditional assignment of values to build settings, to specify architecture or SDK specific values."\
               "\n\n"\
               "...\n"\
               "if arch=arm64 {\n"\
               "    ...\n"\
               "}\n"\
               "..."\
               "\n\n"\
               "...\n"\
               "if arch=i386 and sdk=iphoneos {\n"\
               "    ...\n"\
               "}\n"\
               "..."
    def draw(self, window):
        text = self.content(window)
        self.displayText(window, text)
    def formatting(self):
        return {
            "0": ['underline'],
            "29": ['normal'],
        }