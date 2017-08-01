class BaseField(object):
    def __init__(self, desc, min, max):
        self.desc = desc
        self.min = min
        self.max = max

    def __str__(self):
        return "Desc = %s\nMin = %f || Max = %f\n" % (self.desc, self.min, self.max)
# end BaseField

class FileOutputData(object):
    def __init__(self):
        self.saveOutput = False
        self.filename = None
        self.fileDesc = None
# end FileOutputData

class ComplexUtil(object):
    def getCompVal(num):
        if isinstance(num, complex):
            return abs(num)
        else:
            return num
    # end getCompVal
    
    def lessThan(num1, num2):
        compVal1 = ComplexUtil.getCompVal(num1)
        compVal2 = ComplexUtil.getCompVal(num2)
        
        return compVal1 < compVal2
    # end lessThan
    
    def lessThanEqual(num1, num2):
        compVal1 = ComplexUtil.getCompVal(num1)
        compVal2 = ComplexUtil.getCompVal(num2)
        
        return compVal1 <= compVal2
    # end lessThanEqual

    def greaterThan(num1, num2):
        compVal1 = ComplexUtil.getCompVal(num1)
        compVal2 = ComplexUtil.getCompVal(num2)
        
        return compVal1 > compVal2
    # end greaterThan
    
    def greaterThanEqual(num1, num2):
        compVal1 = ComplexUtil.getCompVal(num1)
        compVal2 = ComplexUtil.getCompVal(num2)
        
        return compVal1 >= compVal2
    # end greaterThan
    
    def getDisplayVal(num):
        if not isinstance(num, complex):
            return num
        
        return num.real
