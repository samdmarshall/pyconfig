#!/usr/bin/python

import pypresenter.slide

class slide18(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('left')
    def content(self, window=None):
        return "\nIntegration with Xcode is easy!"\
                "\n\n"\
                "1. Install pyconfig\n\n"\
                "\t$ brew update\n"\
                "\t$ brew tap samdmarshall/formulae\n"\
                "\t$ brew install samdmarshall/formulae/pyconfig\n"\
                "\n"\
                "2. Add a 'Pre-Build' Script Phase to your scheme\n\n"\
                "3. Invoke 'pyconfig' with the path to your config files\n\n"
    def draw(self, window):
        self.displayText(window, self.content())
    def formatting(self):
        return {
                # title
                "0": ['underline'],
                "31": ['normal']
                }