#!/usr/bin/python

import pypresenter.slide

class slide3(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('center')
    def content(self, window=None):
        return 'pyconfig DSL (Domain Specific Language)'
    def draw(self, window):
        self.displayText(window, self.content())