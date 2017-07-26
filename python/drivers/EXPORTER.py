class EXPORTER(object):
	def __init__(self, filename):
		self.fileRef = open(filename, 'w')
	# end __init__

	def writeData(self, dataList):
		for i in dataList:
			if i == dataList[0]:
				self.fileRef.write(str(i))
			else:
				self.fileRef.write(",%s" % str(i))
		self.fileRef.write("\n")
	# end writeData

	def close(self):
		self.fileRef.close()
	# end close