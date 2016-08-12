#!/usr/bin/python

import pypresenter.slide

class slide4(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('left')
    def content(self, window=None):
        return "\nDeclaring Build Settings\n\n"\
               "Build settings are declared using the 'setting' keyword and are given an assignment scope.\n\n"\
               "setting OTHER_LDFLAGS {\n"\
               "    ...\n"\
               "}\n\n"\
               "This keyword comes with two additional modifier keywords, which allow for composition and inheritance.\n\n"\
               "setting OTHER_LDFLAGS use CONFIGURATION\n\n"\
               "setting OTHER_LDFLAGS inherits\n\n"\
               "setting OTHER_LDFLAGS use CONFIGURATION inherits"
    def draw(self, window):
        text = self.content(window)
        self.displayText(window, text)
    def formatting(self):
        return {    # title
                    "0": ['underline'],
                    "25": ['normal'],
                    # first code example
                    "114": ['blue'],
                    "121": ['normal'],
                    "122": ['magenta'],
                    "136": ['normal'],
                    # second code example
                    "247": ['blue'],
                    "254": ['normal'],
                    "255": ['magenta'],
                    "268": ['normal'],
                    "269": ['blue'],
                    "272": ['normal'],
                    "273": ['magenta'],
                    "286": ['normal'],
                    # third code example
                    "286": ['blue'],
                    "293": ['normal'],
                    "294": ['magenta'],
                    "307": ['normal'],
                    "308": ['blue'],
                    "316": ['normal'],
                    # fourth code example
                    "316": ['blue'],
                    "323": ['normal'],
                    "324": ['magenta'],
                    "337": ['normal'],
                    "338": ['blue'],
                    "341": ['normal'],
                    "342": ['magenta'],
                    "355": ['normal'],
                    "356": ['blue'],
                    "364": ['normal'],
                }