#!/usr/bin/python

import pypresenter.slide

class slide9(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('center')
    def content(self, window=None):
        return "Example"
    def draw(self, window):
        text = self.content(window)
        self.displayText(window, text)