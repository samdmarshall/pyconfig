#!/usr/bin/python

import pypresenter.slide

class slide17(pypresenter.slide):
   def __init__(self):
      super(self.__class__, self).__init__('center')
   def content(self, window=None):
        return "Integration"
   def draw(self, window):
        self.displayText(window, self.content(window))
