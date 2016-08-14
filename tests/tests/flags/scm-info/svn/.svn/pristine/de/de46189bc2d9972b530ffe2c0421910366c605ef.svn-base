#! /usr/bin/python

import sys
import objc
import Foundation

if len(sys.argv) != 2:
    print "%s /path/to/AbstractClassDefinition.bundle" % sys.argv[0]
    sys.exit(1)

bundlePath = sys.argv[1]

bundle = Foundation.NSBundle.bundleWithPath_(bundlePath)
if not bundle.principalClass():
    print "%s: failed to load bundle." % sys.argv[0]

AbstractClass = objc.lookUpClass("AbstractClass")
class ConcreteClass(AbstractClass):
    _fudgeFactor = 0
    
    @classmethod
    def namedInstance_(self, aName):
        print "creating %s" % aName
        newInstance = ConcreteClass.new()
        newInstance.setName_(aName)
        print "returning new instance %s" % newInstance
        return newInstance

    def fudgeFactor(self):
        return self._fudgeFactor

    def setFudgeFactor_(self, aFactor):
        print "factor will be %s" % aFactor
        self._fudgeFactor = aFactor

    def doItToIt_(self, fastFlag):
        if fastFlag:
            returnValue = 516.295
        else:
            returnValue = 927.3
        print "doing it returning %s" % returnValue
        return returnValue

    def description(self):
        return "<Concrete %s named %s>" % (id(self), self.name())
        

objectiveCCode = objc.lookUpClass("ObjectiveCCallingPython")

print objectiveCCode.callSomePython()
