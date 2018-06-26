import numpy as np 

def createDataSet():
	group=np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels=['A','A','B','B']
	return group,labels

def classify0(inX,dataSet,labels,k):
	dataSetSize=dataSet.shape[0]
	diffMat=np.tile(inX, (dataSetSize,1))-dataSet
	sqDiffMat=diffMat**2
	sqDistance=sqDiffMat.sum(axis=1)
	distances=sqDistance**0.5
	sortedDistIndices=distances.argsort()
	classCount={}
	for i in range(k):
		voteIlabel=labels[sortedDistIndices[i]]
		if voteIlabel not in classCount.keys():
			classCount[voteIlabel]=0
		classCount[voteIlabel]+=1
	sortedClassCount=sorted(classCount.iteritems(),key=lambda x:x[1],reverse=True)
	return sortedClassCount[0][0]

def autoNorm(dataSet):
	minVals=dataSet.min(axis=0)
	maxVals=dataSet.max(axis=0)
	ranges=maxVals-minVals
	normDataSet=np.zeros(dataSet.shape)
	m=dataSet.shape[0]
	normDataSet=dataSet-np.tile(minVals, (m,1))
	normDataSet=normDataSet/np.tile(maxVals, (m,1))
	return normDataSet,ranges,minVals

def file2matrix(fileName):
	fr=open(fileName)
	arrayLines=fr.readlines()
	numberOfLine=len(arrayLines)
	returnMat=np.zeros((numberOfLine,3))
	classLabelVector=[]
	index=0
	for line in arrayLines:
		stripLine=line.strip()
		newLine=stripLine.split('\t')
		returnMat[index,:]=newLine[0:3]
		classLabelVector.append(int(newLine[-1]))
		index+=1
	return returnMat,classLabelVector

def datingClassTest():
	hoRatio=0.10
	datingDataMat,datingDataLabels=file2matrix('datingTestSet2.txt')
	normMat,ranges,minVals=autoNorm(datingDataMat)
	m=normMat.shape[0]
	numTestVecs=int(m*hoRatio)
	errorCount=0.0
	for i in range(numTestVecs):
		classiferResult=classify0(normMat[i,:], normMat[numTestVecs:,:], datingDataLabels[numTestVecs:], 3)
		print "the classifier came back with: %d, the real number is: %d" % (classiferResult,datingDataLabels[i])	
		if classiferResult!=datingDataLabels[i]:
			errorCount+=1
	print "the total error rate is: %f" % (errorCount/numTestVecs)

if __name__=='__main__':
	#datingDataMat,datingDataLabels=file2matrix('datingTestSet2.txt')
	#normDataSet,ranges,minVals=autoNorm(datingDataMat)
	#print normDataSet
	datingClassTest()