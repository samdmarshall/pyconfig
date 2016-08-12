#!/usr/bin/python

import pypresenter.slide

class slide5(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('left')
    def content(self, window=None):
        return "\nSpecifying Values\n\n"\
               "Within each build setting definition, you can set value that the setting will be assigned. This is done using the 'for' keyword. This keyword is used for definition how direct assignment as well as compositional assignment works.\n\n"\
               "...\n"\
               "for * {\n"\
               "    ...\n"\
               "}\n"\
               "..."\
               "\n"\
               "...\n"\
               "for Debug {\n"\
               "    ...\n"\
               "}\n"\
               "..."
    def draw(self, window):
        text = self.content(window)
        self.displayText(window, text)
    def formatting(self):
        return {
            # title
            "0": ['underline'],
            "17": ['normal'],
            # first code example
            "249": ['blue'],
            "252": ['normal'],
            "253": ['magenta'],
            "254": ['normal'],
            "270": ['blue'],
            "273": ['normal'],
            "274": ['magenta'],
            "279": ['normal'],
        }