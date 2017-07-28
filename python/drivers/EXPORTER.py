class EXPORTER(object):
    def __init__(self, filename):
        self.fileRef = open("%s.csv" % filename, 'w')
    # end __init__

    def writeData(self, dataList):
        for i in range(len(dataList)):
            dataStr = str(dataList[i])
            if i == 0:
                self.fileRef.write(dataStr)
            else:
                self.fileRef.write(",%s" % dataStr)
        self.fileRef.write("\n")
    # end writeData

    def close(self):
        self.fileRef.close()
    # end close