#!/usr/bin/python

import pypresenter.slide

class slide19(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('center')
    def content(self, window=None):
        return  "project\n"\
                "https://github.com/samdmarshall/pyconfig"\
                "\n\n"\
                "website\n"\
                "https://pewpewthespells.com"\
                "\n\n"\
                "twitter\n"\
                "@queersorceress\n"
    def draw(self, window):
        self.displayText(window, self.content(window))
    def formatting(self):
        return {
                # project
                "0": ['underline'],
                "7": ['normal'],
                # website
                "47": ['underline'],
                "54": ['normal'],
                # twitter
                "81": ['underline'],
                "88": ['normal']
                }