#!/usr/bin/python

import pypresenter.slide

class slide2(pypresenter.slide):
    def __init__(self):
        super(self.__class__, self).__init__('center')
    def content(self, window=None):
        return 'pyconfig is a tool that will generate .xcconfig files for you from a simple DSL, allowing you to manage and configure your builds easier.'
    def draw(self, window):
        self.displayText(window, self.content())
