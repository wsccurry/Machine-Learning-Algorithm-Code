import kNN
import numpy as np 
import os

def fileMatrix(path):
	dirs=os.listdir(path)
	returnMatrix=np.zeros((len(dirs),32*32))
	classLabelVect=[]
	index=0
	for name in dirs:
		fileName=path+'/'+name
		fr=open(fileName)
		lines=fr.readlines()
		digitVect=[]
		for line in lines:
			stripLine=line.strip()
			for i in stripLine:
				digitVect.append(int(i))
		returnMatrix[index,:]=digitVect
		classLabelVect.append(int(name[0]))
		index+=1
	return returnMatrix,classLabelVect

def calcuteError(train_X,train_y,test_X,test_y):
	testSize=len(test_X)
	errorCount=0.0
	for i in range(testSize):
		preLabel=kNN.classify0(test_X[i],train_X,train_y,3)
		if preLabel!=test_y[i]:
			errorCount+=1
	print "error rate: %f" % (errorCount/testSize)

if __name__=='__main__':
	train_X,train_y=fileMatrix('digits/trainingDigits')
	test_X,test_y=fileMatrix('digits/testDigits')
	calcuteError(train_X, train_y, test_X, test_y)



