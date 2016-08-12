#!/usr/bin/python

import pypresenter.slide

class slide1(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('center')
    def content(self, window=None):
        return 'pyconfig'
    def draw(self, window):
        self.displayText(window, self.content())
    def formatting(self):
        return {
                   "0": ['bold'],
                   str(len(self.content())): ['normal']
                }