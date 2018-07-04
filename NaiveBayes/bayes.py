import numpy as np 
import re
import random

def loadDataSet():
	postingList=[['my','dog','has','flea','problems','help','please'],
	             ['maybe','not','take','him','to','dog','park','stupid'],
	             ['my','dalmation','is','so','cute','I','love','him'],
	             ['stop','posting','stupid','worthless','garbage'],
	             ['mr','licks','ate','my','steak','how','to','stop','him'],
	             ['quit','buying','worthless','dog','food','stupid']
	            ]
	classVec=[0,1,0,1,0,1]
	return postingList,classVec

def createVocabList(dataSet):
	vocabSet=set([])
	for document in dataSet:
		vocabSet=vocabSet | set(document)
	return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
	returnVec=[0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)]=1
		else:
			print "the word: %s is not in my Vocabulary" % word
	return returnVec

def trainNB0(trainMatrix,trainCategory):
	numTrainDocs=len(trainMatrix)
	numWords=len(trainMatrix[0])
	pAbusive=np.sum(trainCategory)/float(numTrainDocs)
	p0Num=np.ones(numWords)
	p1Num=np.ones(numWords)
	p0Denom=2.0
	p1Denom=2.0
	for i in range(numTrainDocs):
		if trainCategory[i]==1:
			p1Num+=trainMatrix[i]
			p1Denom+=np.sum(trainMatrix[i])
		else:
			p0Num+=trainMatrix[i]
			p0Denom+=np.sum(trainMatrix[i])
	p1Vect=np.log(p1Num/p1Denom)
	p0Vect=np.log(p0Num/p0Denom)
	return p0Vect,p1Vect,pAbusive

def testingNB():
	listOPosts,listClasses=loadDataSet()
	myVocabList=createVocabList(listOPosts)
	trainMat=[]
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
	p0V,p1V,pAb=trainNB0(np.array(trainMat), np.array(listClasses))
	testEntry=['love','my','dalmation']
	thisDoc=np.array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry,'classified as: %d' % classifyNB(thisDoc,p0V,p1V,pAb)

def classifyNB(vect2Classfiy,p0Vec,p1Vec,pClass1):
	p1=np.sum(vect2Classfiy*p1Vec)+np.log(pClass1)   #note: log
	p0=np.sum(vect2Classfiy*p0Vec)+np.log(1-pClass1)
	if p1>p0:
		return 1
	else:
		return 0

def textParse(bigString):
	listOfTokens=re.split(r'\W*', bigString)
	return [tok.lower() for tok in listOfTokens if len(tok)>2]

def spamText():
	docList=[];classList=[];fullText=[]
	for i in range(1,26):
		wordList=textParse(open('email/spam/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList=textParse(open('email/ham/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList=createVocabList(docList)
	trainingSet=range(50)
	testSet=[]
	for i in range(10):
		randIndex=int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del trainingSet[randIndex]
	trainMat=[]
	trainClasses=[]
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V,p1V,pSpam=trainNB0(np.array(trainMat), np.array(trainClasses))
	errorCount=0.0
	for docIndex in testSet:
		wordVector=setOfWords2Vec(vocabList, docList[docIndex])
		if classifyNB(np.array(wordVector), p0V, p1V, pSpam)!=classList[docIndex]:
			errorCount+=1
	print 'the error rate is: %f' % (float(errorCount)/len(testSet))

if __name__=='__main__':
	#testingNB()
	spamText()


