//
//  ObjectiveCCallingPython.m
//  AbstractClassDefinition
//
//  Created by Bill Bumgarner on 11/20/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "ObjectiveCCallingPython.h"
#import "AbstractClass.h"

@implementation ObjectiveCCallingPython
+ (NSString *) callSomePython;
{
    Class concreteClass = NSClassFromString(@"ConcreteClass");
    AbstractClass *concreteInstance = [concreteClass namedInstance: @"Bob"];
    NSLog(@"Created instance: %@", concreteInstance);
    concreteInstance.fudgeFactor = 1000000000;
    NSLog(@"Set the fudge factor. Gonna do it up, now.");
    float value = [concreteInstance doItToIt: NO];
    
    return [NSString stringWithFormat: @"Did it! %llu %f", concreteInstance.fudgeFactor, value];
}
@end
     
