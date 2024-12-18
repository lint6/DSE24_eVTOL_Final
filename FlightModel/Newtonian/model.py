'''
Created by Lintong

Simulation Model file
DO define function
DO define class
DO NOT script

Upstream
misc.py
class.py

Downstream
physics.py

'''
import numpy as np
import classbank
class InnerClass():
    def __init__(self,value):
        self.value = value
    def PrintValue(self):
        print(self.value)
    def UpdateValue(self, value_new):
        self.value = self.value((value_new, 5))
        
class TestClassWrapper():
    def __init__(self, classes):
        self.InnerClass = classes
    def UpdateInnerClass(self):
        sum = 0
        for i in range(len(self.InnerClass)):
            self.InnerClass[i].PrintValue()
            print(self.InnerClass[i])
            self.InnerClass[i].UpdateValue(value_new = 20)
            print(self.InnerClass[i])
            self.InnerClass[i].PrintValue()
            sum += self.InnerClass[i].value
        print(sum)
        
obj1 = InnerClass(value=lambda x: x[0]*1+x[1])
obj2 = InnerClass(value=lambda x: x[0]*2+x[1])
obj3 = InnerClass(value=lambda x: x[0]*3+x[1])

# obj1([0,1])

classes = [obj1,
           obj2,
           obj3]

Wrapper = TestClassWrapper(classes=classes)
Wrapper.UpdateInnerClass()
value=lambda x: x[0]*3+x[1]
print(type(value))
print(type(12))

testlist = list(np.arange(1,10))
print(testlist)
testlist = [i+1 if i<5 else i for i in testlist]
print(testlist)