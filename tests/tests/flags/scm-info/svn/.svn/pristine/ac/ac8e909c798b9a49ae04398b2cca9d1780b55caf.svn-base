//
//  AbstractClass.m
//  AbstractClassDefinition
//
//  Created by Bill Bumgarner on 11/20/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "AbstractClass.h"

void SubclassResponsibility(id classOrInstance, SEL _cmd) {
    NSString *reason = [NSString stringWithFormat: @"Must subclass %s and override the method %s.",
                        object_getClassName(classOrInstance), sel_getName(_cmd)];
    @throw [NSException exceptionWithName: @"SubclassResponsibility"
                                   reason: reason
                                 userInfo: nil];
}


@implementation AbstractClass
@synthesize name;

- (void) setFudgeFactor:(unsigned long long) aShort
{
    SubclassResponsibility(self, _cmd);
}

- (unsigned long long) fudgeFactor
{
    SubclassResponsibility(self, _cmd);
    return 0;
}

+ namedInstance: (NSString *) aName
{
    SubclassResponsibility(self, _cmd);
    return nil; // not reaached
}

- (float) doItToIt: (BOOL) fastFlag;
{
    SubclassResponsibility(self, _cmd);
    return 0.0; // not reached
}
@end
