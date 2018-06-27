from math import log
import pickle

def calsShannonEnt(dataSet):  
	numEntries=len(dataSet)
	labelCounts={}
	for featVec in dataSet:
		currentLable=featVec[-1]
		if currentLable not in labelCounts.keys():
			labelCounts[currentLable]=0
		labelCounts[currentLable]+=1
	shannonEnt=0.0
	for key in labelCounts.keys():
		prob=float(labelCounts[key])/numEntries
		shannonEnt-=prob*log(prob, 2)
	return shannonEnt

def splitDataSet(dataSet,axis,value):
	retDataSet=[]
	for featVec in dataSet:
		if featVec[axis]==value:
			reducedFeatVec=featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet

def chooseBestFeatureToSplit(dataSet):
	numFeatures=len(dataSet[0])-1
	baseEntropy=calsShannonEnt(dataSet)
	bestInfoGain=0.0
	bestFeature=-1
	for i in range(numFeatures):
		featList=[example[i] for example in dataSet]
		uniqueVals=set(featList)
		newEntropy=0.0
		for value in uniqueVals:
			subDataSet=splitDataSet(dataSet, i, value)
			prob=len(subDataSet)/float(len(dataSet))
			newEntropy+=prob*calsShannonEnt(subDataSet)
		infoGain=baseEntropy-newEntropy
		if infoGain>bestInfoGain:
			bestInfoGain=infoGain
			bestFeature=i
	return bestFeature


def createDataSet():
	dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
	labels=['no surfacing','flippers']
	return dataSet,labels

def majorityCnt(classList):
	classsCount={}
	for vote in classList:
		if vote not in classsCount.keys():
			classsCount[vote]=0
		classsCount[vote]+=1
	sortedClassCount=sorted(classsCount.iteritems(),key=lambda x:x[1],reverse=True)
	return sortedClassCount[0][0]

def createTree(dataSet,labels):
	classList=[example[-1] for example in dataSet]
	if classList.count(classList[0])==len(classList):
		return classList[0]
	if len(dataSet[0])==1:
		return majorityCnt(classList)
	bestFeat=chooseBestFeatureToSplit(dataSet)
	bestFeatLabel=labels[bestFeat]
	myTree={bestFeatLabel:{}}
	subLabels=labels[:]
	del subLabels[bestFeat]
	featValues=[example[bestFeat] for example in dataSet]
	uniqueVals=set(featValues)
	for value in uniqueVals:
		myTree[bestFeatLabel][value]=createTree(splitDataSet\
			                         (dataSet,bestFeat,value), subLabels)
	return myTree

def classify(inputTree,featLabels,testVect):
	firstStr=inputTree.keys()[0]
	secondDict=inputTree[firstStr]
	featIndex=featLabels.index(firstStr)
	for key in secondDict.keys():
		if testVect[featIndex]==key:
			if type(secondDict[key]).__name__=='dict':
				classLabel=classify(secondDict[key], featLabels, testVect)
			else:
				classLabel=secondDict[key]
	return classLabel

def storeTree(inputTree,fileName):
	fw=open(fileName,'wb')
	pickle.dump(inputTree, fw)
	fw.close()

def grabTree(fileName):
	fr=open(fileName,'rb')
	return pickle.load(fr)


if __name__=='__main__':	
	dataSet,labels=createDataSet()
	myTree=createTree(dataSet, labels)
	print classify(myTree, labels, [1,1])
	#storeTree(myTree, 'classifierStorage.txt')
	print grabTree('classifierStorage.txt')




