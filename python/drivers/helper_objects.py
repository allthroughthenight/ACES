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